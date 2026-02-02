// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/mapping/deckgamepadsdlcontrollerdb.h>
#include <deckshell/deckgamepad/mapping/deckgamepadsdlcontrollerdb_p.h>

#include <QtCore/QFile>
#include <QtCore/QTextStream>
#include <QtCore/QDebug>
#include <QtCore/QDir>
#include <QtCore/QFileInfo>

#include <libudev.h>
#include <linux/input.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

DECKGAMEPAD_BEGIN_NAMESPACE

// ========== DeckGamepadSdlControllerDbPrivate Implementation ==========

bool DeckGamepadSdlControllerDbPrivate::parseMappingLine(const QString &line, SdlRawMapping &out)
{
    // Skip comments and empty lines
    QString trimmed = line.trimmed();
    if (trimmed.isEmpty() || trimmed.startsWith('#')) {
        return false;
    }
    
    QStringList parts = trimmed.split(',');
    if (parts.size() < 3) {
        return false;
    }
    
    out.guid = parts[0].trimmed().toLower();
    out.name = parts[1].trimmed();
    
    // Parse mapping items
    for (int i = 2; i < parts.size(); ++i) {
        QString item = parts[i].trimmed();
        QStringList kv = item.split(':');
        if (kv.size() != 2) {
            continue;
        }
        
        QString key = kv[0].toLower();
        QString value = kv[1];
        
        // Platform identifier
        if (key == "platform") {
            out.platform = value;
            continue;
        }
        
        // Parse button mappings
        if (key == "a") {
            out.buttons[GAMEPAD_BUTTON_A] = parseInputBinding(value);
        } else if (key == "b") {
            out.buttons[GAMEPAD_BUTTON_B] = parseInputBinding(value);
        } else if (key == "x") {
            out.buttons[GAMEPAD_BUTTON_X] = parseInputBinding(value);
        } else if (key == "y") {
            out.buttons[GAMEPAD_BUTTON_Y] = parseInputBinding(value);
        } else if (key == "back") {
            out.buttons[GAMEPAD_BUTTON_SELECT] = parseInputBinding(value);
        } else if (key == "start") {
            out.buttons[GAMEPAD_BUTTON_START] = parseInputBinding(value);
        } else if (key == "guide") {
            out.buttons[GAMEPAD_BUTTON_GUIDE] = parseInputBinding(value);
        } else if (key == "leftshoulder") {
            out.buttons[GAMEPAD_BUTTON_L1] = parseInputBinding(value);
        } else if (key == "rightshoulder") {
            out.buttons[GAMEPAD_BUTTON_R1] = parseInputBinding(value);
        } else if (key == "leftstick") {
            out.buttons[GAMEPAD_BUTTON_L3] = parseInputBinding(value);
        } else if (key == "rightstick") {
            out.buttons[GAMEPAD_BUTTON_R3] = parseInputBinding(value);
        } else if (key == "dpup") {
            out.buttons[GAMEPAD_BUTTON_DPAD_UP] = parseInputBinding(value);
        } else if (key == "dpdown") {
            out.buttons[GAMEPAD_BUTTON_DPAD_DOWN] = parseInputBinding(value);
        } else if (key == "dpleft") {
            out.buttons[GAMEPAD_BUTTON_DPAD_LEFT] = parseInputBinding(value);
        } else if (key == "dpright") {
            out.buttons[GAMEPAD_BUTTON_DPAD_RIGHT] = parseInputBinding(value);
        }
        // Parse axis mappings
        else if (key == "leftx") {
            out.axes[GAMEPAD_AXIS_LEFT_X] = parseInputBinding(value);
        } else if (key == "lefty") {
            out.axes[GAMEPAD_AXIS_LEFT_Y] = parseInputBinding(value);
        } else if (key == "rightx") {
            out.axes[GAMEPAD_AXIS_RIGHT_X] = parseInputBinding(value);
        } else if (key == "righty") {
            out.axes[GAMEPAD_AXIS_RIGHT_Y] = parseInputBinding(value);
        } else if (key == "lefttrigger") {
            out.axes[GAMEPAD_AXIS_TRIGGER_LEFT] = parseInputBinding(value);
        } else if (key == "righttrigger") {
            out.axes[GAMEPAD_AXIS_TRIGGER_RIGHT] = parseInputBinding(value);
        }
    }
    
    return out.isValid();
}

SdlInputBinding DeckGamepadSdlControllerDbPrivate::parseInputBinding(const QString &value)
{
    SdlInputBinding binding;
    
    if (value.isEmpty()) {
        return binding;
    }
    
    if (value.startsWith('b')) {
        // Button: b0, b1, b2, ...
        binding.type = SdlInputBinding::Button;
        binding.index = value.mid(1).toInt();
    }
    else if (value.startsWith('h')) {
        // HAT: h0.1, h0.2, h0.4, h0.8
        binding.type = SdlInputBinding::Hat;
        QStringList hatParts = value.mid(1).split('.');
        if (hatParts.size() == 2) {
            binding.index = hatParts[0].toInt();
            binding.hatMask = hatParts[1].toInt();
        }
    }
    else if (value.startsWith('+')) {
        // Positive half-axis: +a0, +a1
        binding.type = SdlInputBinding::HalfAxisPos;
        binding.index = value.mid(2).toInt();  // skip "+a"
    }
    else if (value.startsWith('-')) {
        // Negative half-axis: -a0, -a1
        binding.type = SdlInputBinding::HalfAxisNeg;
        binding.index = value.mid(2).toInt();  // skip "-a"
    }
    else if (value.startsWith('~')) {
        // Inverted axis: ~a0, ~a1
        binding.type = SdlInputBinding::Axis;
        binding.index = value.mid(2).toInt();  // skip "~a"
        binding.inverted = true;
    }
    else if (value.startsWith('a')) {
        // Normal axis: a0, a1, a2, ...
        binding.type = SdlInputBinding::Axis;
        binding.index = value.mid(1).toInt();
    }
    
    return binding;
}

DeviceMapping DeckGamepadSdlControllerDbPrivate::convertToDeviceMapping(
    const SdlRawMapping &rawMapping,
    const QHash<int, int> &physicalButtonMap,
    const QHash<int, int> &physicalAxisMap) const
{
    DeviceMapping deviceMapping;
    deviceMapping.guid = rawMapping.guid;
    deviceMapping.name = rawMapping.name;
    
    // Convert button mappings: SDL button index → evdev code → GamepadButton
    for (auto it = rawMapping.buttons.constBegin(); it != rawMapping.buttons.constEnd(); ++it) {
        GamepadButton logicalButton = it.key();
        const SdlInputBinding &binding = it.value();
        
        if (!binding.isValid()) {
            continue;
        }
        
        if (binding.type == SdlInputBinding::Button) {
            // Find evdev code that maps to this SDL button index
            int evdevCode = physicalButtonMap.key(binding.index, -1);
            if (evdevCode >= 0) {
                deviceMapping.buttonMap[evdevCode] = logicalButton;
            }
        }
        else if (binding.type == SdlInputBinding::Hat) {
            // HAT mappings: (hatIndex << 8 | hatMask) → D-pad button
            const int hatKey = (binding.index << 8) | (binding.hatMask & 0xFF);
            deviceMapping.hatButtonMap[hatKey] = logicalButton;
        }
        else if (binding.type == SdlInputBinding::HalfAxisPos || 
                 binding.type == SdlInputBinding::HalfAxisNeg) {
            // Half-axis as button (e.g., trigger as button)
            // Find evdev code for this SDL axis index
            int evdevCode = physicalAxisMap.key(binding.index, -1);
            if (evdevCode >= 0) {
                if (binding.type == SdlInputBinding::HalfAxisPos) {
                    deviceMapping.halfAxisPosButtonMap[evdevCode] = logicalButton;
                } else {
                    deviceMapping.halfAxisNegButtonMap[evdevCode] = logicalButton;
                }
            }
        }
    }
    
    // Convert axis mappings: SDL axis index → evdev code → GamepadAxis
    for (auto it = rawMapping.axes.constBegin(); it != rawMapping.axes.constEnd(); ++it) {
        GamepadAxis logicalAxis = it.key();
        const SdlInputBinding &binding = it.value();
        
        if (!binding.isValid() || binding.type != SdlInputBinding::Axis) {
            continue;
        }
        
        // Find evdev code that maps to this SDL axis index
        int evdevCode = physicalAxisMap.key(binding.index, -1);
        if (evdevCode >= 0) {
            deviceMapping.axisMap[evdevCode] = logicalAxis;
            if (binding.inverted) {
                deviceMapping.invertedAxes.insert(evdevCode);
            }
        }
    }
    
    return deviceMapping;
}

// ========== DeckGamepadSdlControllerDb Implementation ==========

DeckGamepadSdlControllerDb::DeckGamepadSdlControllerDb(QObject *parent)
    : QObject(parent)
    , d_ptr(new DeckGamepadSdlControllerDbPrivate())
{
}

DeckGamepadSdlControllerDb::~DeckGamepadSdlControllerDb()
{
}

int DeckGamepadSdlControllerDb::loadDatabase(const QString &filePath)
{
    Q_D(DeckGamepadSdlControllerDb);
    
    // Clear existing mappings
    clear();
    
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "Failed to open SDL GameController DB:" << filePath;
        return -1;
    }
    
    d->databasePath = filePath;
    
    QTextStream in(&file);
    int lineNum = 0;
    int loadedCount = 0;
    
    while (!in.atEnd()) {
        QString line = in.readLine();
        lineNum++;
        
        SdlRawMapping mapping;
        if (d->parseMappingLine(line, mapping)) {
            // Only load Linux mappings
            if (mapping.platform.isEmpty() || 
                mapping.platform.compare("Linux", Qt::CaseInsensitive) == 0) {
                d->mappings[mapping.guid] = mapping;
                loadedCount++;
            }
        }
    }
    
    d->loadedCount = loadedCount;
    
    qInfo() << "Loaded" << loadedCount << "SDL mappings from" << filePath;
    emit databaseLoaded(loadedCount);
    
    return loadedCount;
}

int DeckGamepadSdlControllerDb::appendDatabase(const QString &filePath)
{
    Q_D(DeckGamepadSdlControllerDb);
    
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "Failed to open SDL GameController DB:" << filePath;
        return -1;
    }
    
    QTextStream in(&file);
    int loadedCount = 0;
    
    while (!in.atEnd()) {
        QString line = in.readLine();
        
        SdlRawMapping mapping;
        if (d->parseMappingLine(line, mapping)) {
            if (mapping.platform.isEmpty() || 
                mapping.platform.compare("Linux", Qt::CaseInsensitive) == 0) {
                d->mappings[mapping.guid] = mapping;
                loadedCount++;
            }
        }
    }
    
    d->loadedCount = d->mappings.size();
    
    qInfo() << "Appended" << loadedCount << "SDL mappings from" << filePath;
    emit databaseLoaded(loadedCount);
    
    return loadedCount;
}

void DeckGamepadSdlControllerDb::clear()
{
    Q_D(DeckGamepadSdlControllerDb);
    d->mappings.clear();
    d->loadedCount = 0;
    d->databasePath.clear();
}

int DeckGamepadSdlControllerDb::mappingCount() const
{
    Q_D(const DeckGamepadSdlControllerDb);
    return d->mappings.size();
}

bool DeckGamepadSdlControllerDb::hasMapping(const QString &guid) const
{
    Q_D(const DeckGamepadSdlControllerDb);
    return d->mappings.contains(guid.toLower());
}

QString DeckGamepadSdlControllerDb::getDeviceName(const QString &guid) const
{
    Q_D(const DeckGamepadSdlControllerDb);
    QString lowerGuid = guid.toLower();
    
    if (d->mappings.contains(lowerGuid)) {
        return d->mappings[lowerGuid].name;
    }
    
    return QString();
}

DeviceMapping DeckGamepadSdlControllerDb::createDeviceMapping(
    const QString &guid,
    const QHash<int, int> &physicalButtonMap,
    const QHash<int, int> &physicalAxisMap) const
{
    Q_D(const DeckGamepadSdlControllerDb);
    
    QString lowerGuid = guid.toLower();
    
    if (!d->mappings.contains(lowerGuid)) {
        return DeviceMapping();  // Empty mapping
    }
    
    const SdlRawMapping &rawMapping = d->mappings[lowerGuid];
    return d->convertToDeviceMapping(rawMapping, physicalButtonMap, physicalAxisMap);
}

QString DeckGamepadSdlControllerDb::extractGuid(const QString &devicePath, const QString &deviceName)
{
    Q_UNUSED(deviceName);  // May use for fallback in future

    // Prefer evdev input_id (matches SDL GUID semantics on Linux).
    // Format: 16 bytes (32 hex chars) composed as 8 little-endian uint16 words:
    //   [bustype, 0, vendor, 0, product, 0, version, 0]
    const QByteArray utf8Path = devicePath.toUtf8();
    const int fd = ::open(utf8Path.constData(), O_RDONLY | O_NONBLOCK);
    if (fd >= 0) {
        struct input_id id { };
        if (::ioctl(fd, EVIOCGID, &id) >= 0) {
            QByteArray bytes;
            bytes.reserve(16);

            auto appendLe16 = [&bytes](__u16 v) {
                bytes.append(static_cast<char>(v & 0xff));
                bytes.append(static_cast<char>((v >> 8) & 0xff));
            };

            appendLe16(id.bustype);
            appendLe16(0);
            appendLe16(id.vendor);
            appendLe16(0);
            appendLe16(id.product);
            appendLe16(0);
            appendLe16(id.version);
            appendLe16(0);

            (void)::close(fd);
            return QString::fromLatin1(bytes.toHex());
        }
        (void)::close(fd);
    }

    // Fallback: sysfs exposes the same input_id fields and often works even in restricted environments
    // where EVIOCGID is blocked.
    auto parseHexU16 = [](const QString &hex, bool *ok) -> __u16 {
        bool localOk = false;
        const uint v = hex.trimmed().toUInt(&localOk, 16);
        if (ok) {
            *ok = localOk && v <= 0xffff;
        }
        return static_cast<__u16>(v & 0xffff);
    };

    const QString nodeName = QFileInfo(devicePath).fileName();
    if (!nodeName.isEmpty()) {
        const QString idDir = QDir(QStringLiteral("/sys/class/input"))
                                  .filePath(nodeName + QStringLiteral("/device/id"));

        auto readFileTrimmed = [](const QString &path) -> QString {
            QFile f(path);
            if (!f.open(QIODevice::ReadOnly | QIODevice::Text)) {
                return {};
            }
            return QString::fromLatin1(f.readAll()).trimmed();
        };

        bool okBus = false;
        bool okVid = false;
        bool okPid = false;
        bool okVer = false;
        const __u16 busType = parseHexU16(readFileTrimmed(QDir(idDir).filePath(QStringLiteral("bustype"))), &okBus);
        const __u16 vid = parseHexU16(readFileTrimmed(QDir(idDir).filePath(QStringLiteral("vendor"))), &okVid);
        const __u16 pid = parseHexU16(readFileTrimmed(QDir(idDir).filePath(QStringLiteral("product"))), &okPid);
        const __u16 ver = parseHexU16(readFileTrimmed(QDir(idDir).filePath(QStringLiteral("version"))), &okVer);

        if (okBus && okVid && okPid) {
            QByteArray bytes;
            bytes.reserve(16);

            auto appendLe16 = [&bytes](__u16 v) {
                bytes.append(static_cast<char>(v & 0xff));
                bytes.append(static_cast<char>((v >> 8) & 0xff));
            };

            appendLe16(busType);
            appendLe16(0);
            appendLe16(vid);
            appendLe16(0);
            appendLe16(pid);
            appendLe16(0);
            appendLe16(okVer ? ver : 0);
            appendLe16(0);

            return QString::fromLatin1(bytes.toHex());
        }
    }

    // Fallback: Extract GUID from udev properties (best-effort).
    struct udev *udev = udev_new();
    if (!udev) {
        qWarning() << "Failed to create udev context";
        return QString();
    }
    
    // Get device from devnum
    struct stat st;
    if (stat(devicePath.toUtf8().constData(), &st) < 0) {
        udev_unref(udev);
        return QString();
    }
    
    struct udev_device *dev = udev_device_new_from_devnum(udev, 'c', st.st_rdev);
    if (!dev) {
        udev_unref(udev);
        return QString();
    }
    
    // Walk up to find USB device (preferred, stable for real devices).
    struct udev_device *usbParent = udev_device_get_parent_with_subsystem_devtype(dev, "usb", "usb_device");

    auto toQString = [](const char *value) -> QString {
        if (!value) {
            return {};
        }
        return QString::fromLatin1(value).trimmed();
    };

    QString vendorId;
    QString productId;
    QString version;
    __u16 busType = 0;

    if (usbParent) {
        vendorId = toQString(udev_device_get_sysattr_value(usbParent, "idVendor"));
        productId = toQString(udev_device_get_sysattr_value(usbParent, "idProduct"));
        version = toQString(udev_device_get_sysattr_value(usbParent, "bcdDevice"));
        busType = BUS_USB;
    }

    // Fallback: virtual devices (e.g. uinput) often have no USB parent, but still expose ID_* properties.
    if (vendorId.isEmpty() || productId.isEmpty()) {
        vendorId = toQString(udev_device_get_property_value(dev, "ID_VENDOR_ID"));
        productId = toQString(udev_device_get_property_value(dev, "ID_MODEL_ID"));
        version = toQString(udev_device_get_property_value(dev, "ID_REVISION"));

        const QString bus = toQString(udev_device_get_property_value(dev, "ID_BUS"));
        if (bus == QStringLiteral("usb")) {
            busType = BUS_USB;
        } else if (bus == QStringLiteral("bluetooth")) {
            busType = BUS_BLUETOOTH;
        }
    }

    // Fallback: some input devices only expose vendor/product under the input parent sysattrs.
    if (vendorId.isEmpty() || productId.isEmpty()) {
        struct udev_device *inputParent = udev_device_get_parent_with_subsystem_devtype(dev, "input", nullptr);
        if (inputParent) {
            vendorId = toQString(udev_device_get_sysattr_value(inputParent, "id/vendor"));
            productId = toQString(udev_device_get_sysattr_value(inputParent, "id/product"));
            version = toQString(udev_device_get_sysattr_value(inputParent, "id/version"));
            if (busType == 0) {
                const QString bt = toQString(udev_device_get_sysattr_value(inputParent, "id/bustype"));
                bool ok = false;
                busType = parseHexU16(bt, &ok);
                if (!ok) {
                    busType = 0;
                }
            }
        }
    }

    QString guid;
    if (!vendorId.isEmpty() && !productId.isEmpty()) {
        bool okVid = false;
        bool okPid = false;
        bool okVer = false;
        const __u16 vid = parseHexU16(vendorId, &okVid);
        const __u16 pid = parseHexU16(productId, &okPid);
        const __u16 ver = parseHexU16(version, &okVer);

        if (okVid && okPid) {
            QByteArray bytes;
            bytes.reserve(16);

            auto appendLe16 = [&bytes](__u16 v) {
                bytes.append(static_cast<char>(v & 0xff));
                bytes.append(static_cast<char>((v >> 8) & 0xff));
            };

            appendLe16(busType);
            appendLe16(0);
            appendLe16(vid);
            appendLe16(0);
            appendLe16(pid);
            appendLe16(0);
            appendLe16(okVer ? ver : 0);
            appendLe16(0);

            guid = QString::fromLatin1(bytes.toHex());
        }
    }
    
    udev_device_unref(dev);
    udev_unref(udev);
    
    return guid;
}

QString DeckGamepadSdlControllerDb::formatGuid(const QString &rawGuid)
{
    QString formatted = rawGuid.toLower();
    
    // Ensure it's 32 characters
    if (formatted.length() < 32) {
        formatted = formatted.leftJustified(32, '0');
    } else if (formatted.length() > 32) {
        formatted = formatted.left(32);
    }
    
    return formatted;
}

bool DeckGamepadSdlControllerDb::addMapping(const QString &mappingString)
{
    Q_D(DeckGamepadSdlControllerDb);
    
    SdlRawMapping mapping;
    if (!d->parseMappingLine(mappingString, mapping)) {
        qWarning() << "Failed to parse mapping string:" << mappingString;
        return false;
    }
    
    d->mappings[mapping.guid] = mapping;
    d->loadedCount = d->mappings.size();
    
    emit mappingAdded(mapping.guid);
    return true;
}

void DeckGamepadSdlControllerDb::removeMapping(const QString &guid)
{
    Q_D(DeckGamepadSdlControllerDb);
    
    QString lowerGuid = guid.toLower();
    if (d->mappings.remove(lowerGuid)) {
        d->loadedCount = d->mappings.size();
        emit mappingRemoved(guid);
    }
}

QStringList DeckGamepadSdlControllerDb::exportMappings() const
{
    Q_D(const DeckGamepadSdlControllerDb);
    
    QStringList result;
    
    // This would require reversing the mapping back to SDL format
    // For now, just return GUIDs
    for (const QString &guid : d->mappings.keys()) {
        result.append(guid);
    }
    
    return result;
}

DECKGAMEPAD_END_NAMESPACE
