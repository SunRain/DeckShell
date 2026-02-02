// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

/*
 * 参考 qtgamepad 的 linux 实现
 * 以及 Godot 4.0 的 joypad_linux
 */

#include "deviceaccessbroker.h"
#include "deviceuidgenerator.h"
#include "sessiongate.h"

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcalibrationstore.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcustommappingmanager.h>
#include <deckshell/deckgamepad/mapping/deckgamepadsdlcontrollerdb.h>

#include <QtCore/QDateTime>
#include <QtCore/QDebug>
#include <QtCore/QDir>
#include <QtCore/QFile>
#include <QtCore/QMetaType>

extern "C" {
#include <libudev.h>
#include <linux/input.h>

#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
}

DECKGAMEPAD_BEGIN_NAMESPACE

#define LONG_BITS (sizeof(long) * 8)
#define NBITS(x) ((((x) - 1) / LONG_BITS) + 1)
#define test_bit(nr, addr) (((1UL << ((nr) % LONG_BITS)) & ((addr)[(nr) / LONG_BITS])) != 0)

static void registerGamepadEventMetaTypes()
{
    static bool registered = false;
    if (registered) {
        return;
    }
    registered = true;

    (void)qRegisterMetaType<DeckGamepadButtonEvent>();
    (void)qRegisterMetaType<DeckGamepadAxisEvent>();
    (void)qRegisterMetaType<DeckGamepadHatEvent>();
    (void)qRegisterMetaType<DeckGamepadRuntimeConfig>();
    (void)qRegisterMetaType<DeckGamepadError>();
    (void)qRegisterMetaType<DeckGamepadErrorCode>();
    (void)qRegisterMetaType<DeckGamepadDeviceAvailability>();
}

DeckGamepadDevice::DeckGamepadDevice(int id,
                                     const QString &devpath,
                                     DeckGamepadSdlControllerDb *sdlDb,
                                     QObject *parent)
	    : QObject(parent)
	    , m_id(id)
	    , m_devpath(devpath)
	    , m_fd(-1)
	    , m_notifier(nullptr)
	    , m_sdlDb(sdlDb)
	    , m_hasFF(false)
	    , m_ffEffectId(-1)
	{
	    memset(m_keyMap, 0, sizeof(m_keyMap));
    memset(m_absInfo, 0, sizeof(m_absInfo));
}

DeckGamepadDevice::~DeckGamepadDevice()
{
    close();
}

bool DeckGamepadDevice::open()
{
    if (m_fd != -1) {
        return true;
    }

    const int fd = ::open(m_devpath.toUtf8().constData(), O_RDWR | O_NONBLOCK);
    if (fd == -1) {
        qWarning() << "Failed to open gamepad device:" << m_devpath << strerror(errno);
        return false;
    }

    return openWithFd(fd);
}

bool DeckGamepadDevice::openWithFd(int fd, std::function<void()> releaseDevice)
{
    if (fd < 0) {
        return false;
    }
    if (m_fd != -1) {
        close();
    }

    m_fd = fd;
    m_releaseDevice = std::move(releaseDevice);

    setupDevice();

    m_notifier = new QSocketNotifier(m_fd, QSocketNotifier::Read, this);
    connect(m_notifier, &QSocketNotifier::activated, this, &DeckGamepadDevice::handleReadyRead);

    qDebug() << "Opened gamepad device:" << m_name << "at" << m_devpath;
    return true;
}

static void closeDeviceFd(int &fd)
{
    if (fd < 0) {
        return;
    }
    ::close(fd);
    fd = -1;
}

void DeckGamepadDevice::close()
{
    if (m_fd == -1) {
        return;
    }

    // 关闭前停止振动
    if (m_ffEffectId != -1) {
        stopVibration();
    }

    if (m_notifier) {
        m_notifier->setEnabled(false);
        m_notifier->deleteLater();
        m_notifier = nullptr;
    }

    closeDeviceFd(m_fd);

    if (m_releaseDevice) {
        m_releaseDevice();
        m_releaseDevice = {};
    }
}

void DeckGamepadDevice::closeForIoError()
{
    if (m_fd == -1) {
        return;
    }

    close();
    emit disconnected(m_id);
}

void DeckGamepadDevice::setupDevice()
{
    char namebuf[128] = { 0 };
    if (ioctl(m_fd, EVIOCGNAME(sizeof(namebuf)), namebuf) >= 0) {
        m_name = QString::fromUtf8(namebuf);
    } else {
        m_name = "Unknown Gamepad";
    }

    if (m_sdlDb) {
        m_guid = DeckGamepadSdlControllerDb::extractGuid(m_devpath, m_name);
        qDebug() << "Device GUID:" << m_guid << "Name:" << m_name;
    }

    unsigned long keybit[NBITS(KEY_MAX)] = { 0 };
    if (ioctl(m_fd, EVIOCGBIT(EV_KEY, sizeof(keybit)), keybit) >= 0) {
        int num_buttons = 0;
        int sdlButtonIndex = 0;

        for (int i = BTN_JOYSTICK; i < KEY_MAX; ++i) {
            if (test_bit(i, keybit)) {
                m_keyMap[i] = num_buttons++;
                m_physicalButtonMap[i] = sdlButtonIndex++; // SDL button index
            }
        }

        for (int i = BTN_MISC; i < BTN_JOYSTICK; ++i) {
            if (test_bit(i, keybit)) {
                m_keyMap[i] = num_buttons++;
                m_physicalButtonMap[i] = sdlButtonIndex++; // SDL button index
            }
        }

        qDebug() << "Detected" << sdlButtonIndex << "physical buttons";
    }

    unsigned long absbit[NBITS(ABS_MAX)] = { 0 };
    if (ioctl(m_fd, EVIOCGBIT(EV_ABS, sizeof(absbit)), absbit) >= 0) {
        int sdlAxisIndex = 0;

        for (int i = 0; i < ABS_MISC; ++i) {
            if (i == ABS_HAT0X) {
                i = ABS_HAT3Y;
                continue;
            }

            if (test_bit(i, absbit)) {
                struct input_absinfo absInfo;
                if (ioctl(m_fd, EVIOCGABS(i), &absInfo) >= 0) {
                    m_absInfo[i].min = absInfo.minimum;
                    m_absInfo[i].max = absInfo.maximum;
                    m_absInfo[i].flat = absInfo.flat;
                }
                m_physicalAxisMap[i] = sdlAxisIndex++; // SDL axis index
            }
        }

        qDebug() << "Detected" << sdlAxisIndex << "physical axes";
    }

    unsigned long ffbit[NBITS(FF_CNT)] = { 0 };
    if (ioctl(m_fd, EVIOCGBIT(EV_FF, sizeof(ffbit)), ffbit) >= 0) {
        m_hasFF = test_bit(FF_RUMBLE, ffbit);
    }

    setupSdlMapping();
}

void DeckGamepadDevice::reloadMapping()
{
    if (m_fd == -1) {
        qWarning() << "Cannot reload mapping: device not open";
        return;
    }

    m_deviceMapping = DeviceMapping();
    m_halfAxisStateByCode.clear();

    setupSdlMapping();

    qDebug() << "Reloaded mapping for device" << m_id << m_name;
}

void DeckGamepadDevice::setupSdlMapping()
{
    if (!m_sdlDb || m_guid.isEmpty()) {
        qDebug() << "SDL DB not available or no GUID, using default mapping";
        return;
    }

    if (!m_sdlDb->hasMapping(m_guid)) {
        qWarning() << "No SDL mapping found for" << m_name << "GUID:" << m_guid;
        qWarning() << "Will use generic mapping. Consider adding to SDL DB.";
        return;
    }

    m_deviceMapping = m_sdlDb->createDeviceMapping(m_guid, m_physicalButtonMap, m_physicalAxisMap);

    if (m_deviceMapping.isValid()) {
        qInfo() << "Applied SDL mapping for" << m_name;
        qInfo() << "  Mapped buttons:" << m_deviceMapping.buttonMap.size();
        qInfo() << "  Mapped axes:" << m_deviceMapping.axisMap.size();
    }
}

void DeckGamepadDevice::handleReadyRead()
{
    processEvents();
}

void DeckGamepadDevice::processEvents()
{
    struct input_event events[32];

    while (true) {
        ssize_t rd = read(m_fd, events, sizeof(events));

        if (rd < (ssize_t)sizeof(struct input_event)) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                break;
            } else {
                qWarning() << "Gamepad device read error:" << strerror(errno);
                closeForIoError();
                break;
            }
        }

        const int count = static_cast<int>(rd / static_cast<ssize_t>(sizeof(struct input_event)));
        for (int i = 0; i < count; i++) {
            const struct input_event &ev = events[i];

            uint32_t time_msec = ev.time.tv_sec * 1000 + ev.time.tv_usec / 1000;

            switch (ev.type) {
            case EV_KEY: {
                if (ev.code >= MAX_KEY) {
                    qDebug() << "Button code out of range:" << ev.code;
                    continue;
                }

                DeckGamepadButtonEvent event;
                event.time_msec = time_msec;
                event.button = mapButton(ev.code);
                event.pressed = (ev.value != 0);

                if (event.button != GAMEPAD_BUTTON_INVALID) {
                    emit buttonEvent(m_id, event);
                }
                break;
            }

	            case EV_ABS: {
	                int hatIndex = -1;
	                bool isHatX = false;
	                bool isHatY = false;
	                switch (ev.code) {
	                case ABS_HAT0X:
	                    hatIndex = 0;
	                    isHatX = true;
	                    break;
	                case ABS_HAT0Y:
	                    hatIndex = 0;
	                    isHatY = true;
	                    break;
	                case ABS_HAT1X:
	                    hatIndex = 1;
	                    isHatX = true;
	                    break;
	                case ABS_HAT1Y:
	                    hatIndex = 1;
	                    isHatY = true;
	                    break;
	                case ABS_HAT2X:
	                    hatIndex = 2;
	                    isHatX = true;
	                    break;
	                case ABS_HAT2Y:
	                    hatIndex = 2;
	                    isHatY = true;
	                    break;
	                case ABS_HAT3X:
	                    hatIndex = 3;
	                    isHatX = true;
	                    break;
	                case ABS_HAT3Y:
	                    hatIndex = 3;
	                    isHatY = true;
	                    break;
	                default:
	                    break;
	                }

	                if (hatIndex >= 0) {
	                    if (isHatX) {
	                        m_hatXByHat[static_cast<size_t>(hatIndex)] = ev.value;
	                    } else if (isHatY) {
	                        m_hatYByHat[static_cast<size_t>(hatIndex)] = ev.value;
	                    }

	                    const int hatX = m_hatXByHat[static_cast<size_t>(hatIndex)];
	                    const int hatY = m_hatYByHat[static_cast<size_t>(hatIndex)];

	                    DeckGamepadHatEvent event;
	                    event.time_msec = time_msec;
	                    event.hat = static_cast<uint32_t>(hatIndex);
	                    event.value = GAMEPAD_HAT_CENTER;

	                    if (hatX < 0) {
	                        event.value |= GAMEPAD_HAT_LEFT;
	                    } else if (hatX > 0) {
	                        event.value |= GAMEPAD_HAT_RIGHT;
	                    }

	                    if (hatY < 0) {
	                        event.value |= GAMEPAD_HAT_UP;
	                    } else if (hatY > 0) {
	                        event.value |= GAMEPAD_HAT_DOWN;
	                    }

	                    emit hatEvent(m_id, event);

                } else if (ev.code < MAX_ABS) {
                    const bool halfAxisMapped = m_deviceMapping.isValid()
                        && (m_deviceMapping.halfAxisPosButtonMap.contains(ev.code)
                            || m_deviceMapping.halfAxisNegButtonMap.contains(ev.code));

                    DeckGamepadAxisEvent event;
                    event.time_msec = time_msec;
                    event.axis = mapAxis(ev.code);
                    event.value = normalizeAxisValue(ev.code, ev.value);

                    if (halfAxisMapped && !m_deviceMapping.axisMap.contains(ev.code)) {
                        event.axis = GAMEPAD_AXIS_INVALID;
                    }

                    if (halfAxisMapped) {
                        static constexpr double kHalfAxisButtonThreshold = 0.5;
                        int nextState = 0;
                        if (event.value > kHalfAxisButtonThreshold) {
                            nextState = 1;
                        } else if (event.value < -kHalfAxisButtonThreshold) {
                            nextState = -1;
                        }

                        const int prevState = m_halfAxisStateByCode.value(ev.code, 0);
                        if (prevState != nextState) {
                            auto emitMappedButton = [&](int state, bool pressed) {
                                GamepadButton button = GAMEPAD_BUTTON_INVALID;
                                if (state > 0) {
                                    button = m_deviceMapping.halfAxisPosButtonMap.value(ev.code, GAMEPAD_BUTTON_INVALID);
                                } else if (state < 0) {
                                    button = m_deviceMapping.halfAxisNegButtonMap.value(ev.code, GAMEPAD_BUTTON_INVALID);
                                }

                                if (button == GAMEPAD_BUTTON_INVALID) {
                                    return;
                                }

                                DeckGamepadButtonEvent btnEvent;
                                btnEvent.time_msec = time_msec;
                                btnEvent.button = button;
                                btnEvent.pressed = pressed;
                                emit buttonEvent(m_id, btnEvent);
                            };

                            if (prevState != 0) {
                                emitMappedButton(prevState, false);
                            }
                            if (nextState != 0) {
                                emitMappedButton(nextState, true);
                            }

                            m_halfAxisStateByCode.insert(ev.code, nextState);
                        }
                    }

                    if (event.axis != GAMEPAD_AXIS_INVALID) {
                        emit axisEvent(m_id, event);
                    }
                }
                break;
            }
            default:
                break;
            }
        }
    }
}

static double applyAxisCalibrationValue(const AxisCalibration &cal, double value)
{
    const double min = qBound(-1.0, double(cal.min), 1.0);
    const double max = qBound(-1.0, double(cal.max), 1.0);
    if (max <= min) {
        return value;
    }

    switch (cal.mode) {
    case AxisCalibrationMode::MinMax: {
        const double out = 2.0 * (value - min) / (max - min) - 1.0;
        return qBound(-1.0, out, 1.0);
    }
    case AxisCalibrationMode::CenterMinMax: {
        const double center = qBound(min, double(cal.centerOffset), max);
        if (value >= center) {
            const double denom = max - center;
            if (denom <= 0.0) {
                return 0.0;
            }
            return qBound(0.0, (value - center) / denom, 1.0);
        }

        const double denom = center - min;
        if (denom <= 0.0) {
            return 0.0;
        }
        return qBound(-1.0, (value - center) / denom, 0.0);
    }
    }
    return value;
}

double DeckGamepadDevice::normalizeAxisValue(int code, int value)
{
    const AxisInfo &info = m_absInfo[code];

    if (info.max == info.min) {
        return 0.0;
    }

    double normalized = 2.0 * (value - info.min) / (info.max - info.min) - 1.0;

    if (isAxisInverted(code)) {
        normalized = -normalized;
    }

    GamepadAxis axis = mapAxis(code);
    if (axis != GAMEPAD_AXIS_INVALID && m_calibrationData && !m_guid.isEmpty()) {
        const auto devIt = m_calibrationData->devices.constFind(m_guid);
        if (devIt != m_calibrationData->devices.constEnd()) {
            const auto axisIt = devIt->axes.constFind(axis);
            if (axisIt != devIt->axes.constEnd()) {
                normalized = applyAxisCalibrationValue(axisIt.value(), normalized);
            }
        }
    }

    if (info.flat > 0) {
        double flat_threshold = std::abs(info.flat / double(info.max - info.min));
        if (std::abs(normalized) <= flat_threshold) {
            normalized = 0.0;
        }
    }

    if (axis != GAMEPAD_AXIS_INVALID && m_customDeadzones.contains(axis)) {
        float customDeadzone = m_customDeadzones.value(axis);
        if (std::abs(normalized) <= customDeadzone) {
            normalized = 0.0;
        } else {
            double sign = (normalized > 0) ? 1.0 : -1.0;
            normalized = sign * (std::abs(normalized) - customDeadzone) / (1.0 - customDeadzone);
        }
    }

    if (axis != GAMEPAD_AXIS_INVALID && m_axisSensitivity.contains(axis)) {
        float sensitivity = m_axisSensitivity.value(axis);
        normalized *= sensitivity;
        normalized = qBound(-1.0, normalized, 1.0);
    }

    return normalized;
}

GamepadButton DeckGamepadDevice::mapButton(int evdev_code) const
{
    if (m_deviceMapping.isValid() && m_deviceMapping.buttonMap.contains(evdev_code)) {
        return m_deviceMapping.buttonMap.value(evdev_code);
    }

    switch (evdev_code) {
    case BTN_SOUTH:
        return GAMEPAD_BUTTON_A; // BTN_A / BTN_GAMEPAD
    case BTN_EAST:
        return GAMEPAD_BUTTON_B; // BTN_B
    case BTN_NORTH:
        return GAMEPAD_BUTTON_X; // BTN_X
    case BTN_WEST:
        return GAMEPAD_BUTTON_Y; // BTN_Y
    case BTN_C:
        return GAMEPAD_BUTTON_X;
    case BTN_TL:
        return GAMEPAD_BUTTON_L1;
    case BTN_TR:
        return GAMEPAD_BUTTON_R1;
    case BTN_TL2:
        return GAMEPAD_BUTTON_L2;
    case BTN_TR2:
        return GAMEPAD_BUTTON_R2;
    case BTN_SELECT:
        return GAMEPAD_BUTTON_SELECT;
    case BTN_START:
        return GAMEPAD_BUTTON_START;
    case BTN_THUMBL:
        return GAMEPAD_BUTTON_L3;
    case BTN_THUMBR:
        return GAMEPAD_BUTTON_R3;
    case BTN_MODE:
        return GAMEPAD_BUTTON_GUIDE;
    case BTN_DPAD_UP:
        return GAMEPAD_BUTTON_DPAD_UP;
    case BTN_DPAD_DOWN:
        return GAMEPAD_BUTTON_DPAD_DOWN;
    case BTN_DPAD_LEFT:
        return GAMEPAD_BUTTON_DPAD_LEFT;
    case BTN_DPAD_RIGHT:
        return GAMEPAD_BUTTON_DPAD_RIGHT;
    default:
        return GAMEPAD_BUTTON_INVALID;
    }
}

GamepadAxis DeckGamepadDevice::mapAxis(int evdev_code) const
{
    if (m_deviceMapping.isValid() && m_deviceMapping.axisMap.contains(evdev_code)) {
        return m_deviceMapping.axisMap.value(evdev_code);
    }

    switch (evdev_code) {
    case ABS_X:
        return GAMEPAD_AXIS_LEFT_X;
    case ABS_Y:
        return GAMEPAD_AXIS_LEFT_Y;
    case ABS_RX:
        return GAMEPAD_AXIS_RIGHT_X;
    case ABS_RY:
        return GAMEPAD_AXIS_RIGHT_Y;
    case ABS_Z:
        return GAMEPAD_AXIS_TRIGGER_LEFT;
    case ABS_RZ:
        return GAMEPAD_AXIS_TRIGGER_RIGHT;
    default:
        return GAMEPAD_AXIS_INVALID;
    }
}

bool DeckGamepadDevice::isAxisInverted(int evdev_code) const
{
    return m_deviceMapping.invertedAxes.contains(evdev_code);
}

bool DeckGamepadDevice::startVibration(float weakMagnitude, float strongMagnitude, int duration_ms)
{
    if (!m_hasFF || m_fd == -1) {
        return false;
    }

    if (weakMagnitude < 0.0f || weakMagnitude > 1.0f || strongMagnitude < 0.0f
        || strongMagnitude > 1.0f) {
        qWarning() << "Vibration magnitudes must be between 0.0 and 1.0";
        return false;
    }

    if (m_ffEffectId != -1) {
        stopVibration();
    }

    struct ff_effect effect;
    memset(&effect, 0, sizeof(effect));
    effect.type = FF_RUMBLE;
    effect.id = -1; // -1 means create new effect
    effect.u.rumble.weak_magnitude = static_cast<uint16_t>(weakMagnitude * 0xFFFF);
    effect.u.rumble.strong_magnitude = static_cast<uint16_t>(strongMagnitude * 0xFFFF);
    effect.replay.length = duration_ms; // Duration in milliseconds
    effect.replay.delay = 0;

    if (ioctl(m_fd, EVIOCSFF, &effect) < 0) {
        qWarning() << "Failed to upload vibration effect:" << strerror(errno);
        return false;
    }

    struct input_event play;
    memset(&play, 0, sizeof(play));
    play.type = EV_FF;
    play.code = effect.id;
    play.value = 1; // Play once

    if (write(m_fd, &play, sizeof(play)) == -1) {
        qWarning() << "Failed to play vibration effect:" << strerror(errno);
        ioctl(m_fd, EVIOCRMFF, effect.id);
        return false;
    }

    m_ffEffectId = effect.id;
    qDebug() << "Started vibration on device" << m_id << "weak:" << weakMagnitude
             << "strong:" << strongMagnitude << "duration:" << duration_ms << "ms";
    return true;
}

void DeckGamepadDevice::stopVibration()
{
    if (!m_hasFF || m_fd == -1 || m_ffEffectId == -1) {
        return;
    }

    if (ioctl(m_fd, EVIOCRMFF, m_ffEffectId) < 0) {
        qWarning() << "Failed to remove vibration effect:" << strerror(errno);
        return;
    }

    qDebug() << "Stopped vibration on device" << m_id;
    m_ffEffectId = -1;
}

DeckGamepadBackend *DeckGamepadBackend::s_instance = nullptr;

DeckGamepadBackend *DeckGamepadBackend::instance()
{
    if (!s_instance) {
        s_instance = new DeckGamepadBackend();
    }
    return s_instance;
}

DeckGamepadBackend::DeckGamepadBackend(QObject *parent)
    : QObject(parent)
    , m_udev(nullptr)
    , m_udevMonitor(nullptr)
    , m_udevNotifier(nullptr)
    , m_nextDeviceId(0)
    , m_sdlDb(new DeckGamepadSdlControllerDb(this))
    , m_customMappingMgr(new DeckGamepadCustomMappingManager(this, this))
{
    registerGamepadEventMetaTypes();

    m_accessBroker = std::make_unique<DeviceAccessBroker>();
    m_sessionGate = std::make_unique<SessionGate>();

    qDebug() << "DeckGamepadBackend initialized";
}

DeckGamepadBackend::~DeckGamepadBackend()
{
    stop();

    if (s_instance == this) {
        s_instance = nullptr;
    }
}

void DeckGamepadBackend::setRuntimeConfig(const DeckGamepadRuntimeConfig &config)
{
    if (m_running) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::InvalidConfig;
        err.message =
            QStringLiteral("setRuntimeConfig is only allowed when backend is not running");
        err.context = QStringLiteral("DeckGamepadBackend::setRuntimeConfig");
        err.recoverable = true;
        setError(err);
        return;
    }

    m_runtimeConfig = config;

    if (m_accessBroker) {
        m_accessBroker->setRuntimeConfig(m_runtimeConfig);
    }
    if (m_sessionGate) {
        m_sessionGate->setEnabled(m_runtimeConfig.capturePolicy
                                  == DeckGamepadCapturePolicy::ActiveSessionOnly);
    }

    if (m_customMappingMgr) {
        m_customMappingMgr->setLegacyDirName(m_runtimeConfig.legacyDataDirName);
        m_customMappingMgr->setLegacyFallbackEnabled(m_runtimeConfig.enableLegacyDeckShellPaths);
        m_customMappingMgr->setDefaultConfigPath(m_runtimeConfig.customMappingPathOverride);
    }
}

DeckGamepadRuntimeConfig DeckGamepadBackend::runtimeConfig() const
{
    return m_runtimeConfig;
}

DeckGamepadError DeckGamepadBackend::lastError() const
{
    return m_lastError;
}

bool DeckGamepadBackend::start()
{
    if (m_running) {
        return true;
    }

    setError(DeckGamepadError{});

    if (m_sessionGate) {
        m_sessionGate->setEnabled(m_runtimeConfig.capturePolicy
                                  == DeckGamepadCapturePolicy::ActiveSessionOnly);
        connect(m_sessionGate.get(),
                &SessionGate::activeChanged,
                this,
                &DeckGamepadBackend::handleSessionGateActiveChanged,
                Qt::UniqueConnection);
    }

    m_udev = udev_new();
    if (!m_udev) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::BackendStartFailed;
        err.message = QStringLiteral("Failed to initialize udev for gamepad detection");
        err.context = QStringLiteral("udev_new");
        err.recoverable = false;
        setError(err);
        return false;
    }

    m_udevMonitor = udev_monitor_new_from_netlink(m_udev, "udev");
    if (!m_udevMonitor) {
        // udev monitor may be unavailable in restricted environments (e.g. containers with netlink blocked).
        // Degrade gracefully: keep udev enumeration working and rely on periodic rescan for hotplug.
        qWarning() << "Failed to create udev monitor, falling back to periodic rescan";
    } else {
        udev_monitor_filter_add_match_subsystem_devtype(m_udevMonitor, "input", nullptr);
        udev_monitor_enable_receiving(m_udevMonitor);

        int monitor_fd = udev_monitor_get_fd(m_udevMonitor);
        m_udevNotifier = new QSocketNotifier(monitor_fd, QSocketNotifier::Read, this);
        connect(m_udevNotifier,
                &QSocketNotifier::activated,
                this,
                &DeckGamepadBackend::handleUdevEvent);
    }

    reloadSdlDb(findDefaultSdlDatabase());
    if (m_customMappingMgr) {
        (void)m_customMappingMgr->loadFromFile();
    }
    loadCalibration();

    probeGamepads();

    if (m_runtimeConfig.enableAutoRetryOpen) {
        if (!m_retryTimer) {
            m_retryTimer = new QTimer(this);
            m_retryTimer->setSingleShot(true);
            connect(m_retryTimer,
                    &QTimer::timeout,
                    this,
                    &DeckGamepadBackend::retryUnavailableDevices);
        }
        scheduleNextRetry();
    }

    m_running = true;
    qDebug() << "Gamepad backend started, found" << m_devices.count() << "gamepads";
    return true;
}

void DeckGamepadBackend::stop()
{
    m_running = false;

    // 关闭所有设备
    for (auto it = m_devices.begin(); it != m_devices.end(); ++it) {
        if (it.value()) {
            it.value()->close();
            it.value()->deleteLater();
        }
    }
    m_devices.clear();
    m_devicePaths.clear();
    m_knownDevices.clear();

    if (m_udevNotifier) {
        m_udevNotifier->setEnabled(false);
        m_udevNotifier->deleteLater();
        m_udevNotifier = nullptr;
    }

    if (m_udevMonitor) {
        udev_monitor_unref(m_udevMonitor);
        m_udevMonitor = nullptr;
    }

    if (m_udev) {
        udev_unref(m_udev);
        m_udev = nullptr;
    }

    if (m_retryTimer) {
        m_retryTimer->stop();
    }
}

void DeckGamepadBackend::probeGamepads()
{
    if (!m_udev) {
        return;
    }

    struct udev_enumerate *enumerate = udev_enumerate_new(m_udev);
    udev_enumerate_add_match_subsystem(enumerate, "input");
    udev_enumerate_scan_devices(enumerate);

    struct udev_list_entry *devices = udev_enumerate_get_list_entry(enumerate);
    struct udev_list_entry *entry = nullptr;

	    udev_list_entry_foreach(entry, devices)
	    {
	        const char *path = udev_list_entry_get_name(entry);
	        struct udev_device *dev = udev_device_new_from_syspath(m_udev, path);
	        if (!dev) {
	            continue;
	        }
	        const char *devnode = udev_device_get_devnode(dev);

	        if (devnode) {
	            QString devpath(devnode);

	            if (!devpath.contains("/js")) {
	                const char *isJoystick = udev_device_get_property_value(dev, "ID_INPUT_JOYSTICK");
	                const char *isGamepad = udev_device_get_property_value(dev, "ID_INPUT_GAMEPAD");
	                const bool hasGamepadHint = (isJoystick != nullptr) || (isGamepad != nullptr);
	                const bool udevCandidate = (isJoystick && strcmp(isJoystick, "1") == 0)
	                    || (isGamepad && strcmp(isGamepad, "1") == 0);

	                bool candidate = udevCandidate;
	                int probeErrno = 0;
	                if (!candidate) {
	                    candidate = isGamepadDevice(devpath, &probeErrno);
	                    if (!candidate && (probeErrno == EACCES || probeErrno == EPERM) && !hasGamepadHint) {
	                        candidate = true;
	                    }
	                }

	                if (candidate) {
	                    openGamepad(dev, devpath);
	                }
	            }
	        }

        udev_device_unref(dev);
    }

    udev_enumerate_unref(enumerate);
}

	bool DeckGamepadBackend::isGamepadDevice(const QString &devpath, int *openErrno)
	{
	    if (openErrno) {
	        *openErrno = 0;
	    }

	    errno = 0;
	    int fd = ::open(devpath.toUtf8().constData(), O_RDONLY | O_NONBLOCK);
	    if (fd == -1) {
	        if (openErrno) {
	            *openErrno = errno;
	        }
	        return false;
	    }

    unsigned long evbit[NBITS(EV_MAX)] = { 0 };
    unsigned long absbit[NBITS(ABS_MAX)] = { 0 };

    bool result = false;

    if (ioctl(fd, EVIOCGBIT(0, sizeof(evbit)), evbit) >= 0
        && ioctl(fd, EVIOCGBIT(EV_ABS, sizeof(absbit)), absbit) >= 0) {

        if (test_bit(EV_KEY, evbit) && test_bit(EV_ABS, evbit)) {
            bool has_left = test_bit(ABS_X, absbit) && test_bit(ABS_Y, absbit);
            bool has_right = test_bit(ABS_RX, absbit) && test_bit(ABS_RY, absbit);
            result = (has_left || has_right);
        }
    }

    ::close(fd);
    return result;
}

bool DeckGamepadBackend::isGamepadUdevDevice(struct udev_device *dev) const
{
    if (!dev) {
        return false;
    }

    const char *isJoystick = udev_device_get_property_value(dev, "ID_INPUT_JOYSTICK");
    if (isJoystick && strcmp(isJoystick, "1") == 0) {
        return true;
    }

    const char *isGamepad = udev_device_get_property_value(dev, "ID_INPUT_GAMEPAD");
    if (isGamepad && strcmp(isGamepad, "1") == 0) {
        return true;
    }

    return false;
}

QString DeckGamepadBackend::udevDeviceName(struct udev_device *dev) const
{
    if (!dev) {
        return QString{};
    }

    const char *name = udev_device_get_sysattr_value(dev, "name");
    if (name && *name) {
        return QString::fromUtf8(name);
    }

    const char *model = udev_device_get_property_value(dev, "ID_MODEL_FROM_DATABASE");
    if (model && *model) {
        return QString::fromUtf8(model);
    }

    model = udev_device_get_property_value(dev, "ID_MODEL");
    if (model && *model) {
        return QString::fromUtf8(model);
    }

    return QString{};
}

void DeckGamepadBackend::openGamepad(struct udev_device *dev, const QString &devpath)
{
    int id = m_devicePaths.value(devpath, -1);
    if (id == -1) {
        id = getUnusedDeviceId();
        if (id == -1) {
            qWarning() << "Maximum number of gamepads reached";
            return;
        }

        KnownDevice known;
        known.devpath = devpath;
        known.info.name = udevDeviceName(dev);
        if (dev) {
            QHash<QString, QString> props;
            const char *keys[] = { "ID_VENDOR_ID", "ID_MODEL_ID", "ID_BUS", "ID_SERIAL_SHORT",
                                   "ID_SERIAL",    "ID_PATH",     "DEVPATH" };
            for (const char *k : keys) {
                const char *v = udev_device_get_property_value(dev, k);
                if (v && *v) {
                    props.insert(QString::fromLatin1(k), QString::fromUtf8(v));
                }
            }

            const QString vendorIdHex = props.value(QStringLiteral("ID_VENDOR_ID"));
            const QString productIdHex = props.value(QStringLiteral("ID_MODEL_ID"));
            bool okVid = false;
            bool okPid = false;
            const uint16_t vid = vendorIdHex.toUShort(&okVid, 16);
            const uint16_t pid = productIdHex.toUShort(&okPid, 16);
            if (okVid) {
                known.info.vendorId = vid;
            }
            if (okPid) {
                known.info.productId = pid;
            }
            known.info.transport = props.value(QStringLiteral("ID_BUS"));
            known.info.deviceUid = DeckGamepadDeviceUidGenerator::generateFromUdevProperties(props);
        }
        known.availability = DeckGamepadDeviceAvailability::Unavailable;
        m_knownDevices.insert(id, known);
        m_devicePaths.insert(devpath, id);

        Q_EMIT deviceInfoChanged(id, known.info);
        Q_EMIT deviceAvailabilityChanged(id, DeckGamepadDeviceAvailability::Unavailable);
    }

    (void)tryOpenGamepad(id, devpath);
}

bool DeckGamepadBackend::tryOpenGamepad(int deviceId, const QString &devpath)
{
    if (m_devices.contains(deviceId)) {
        return true;
    }

    auto itKnown = m_knownDevices.find(deviceId);
    if (itKnown == m_knownDevices.end()) {
        return false;
    }

    if (m_sessionGate && m_sessionGate->enabled() && !m_sessionGate->isActive()) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::Io;
        err.message = QStringLiteral("Session inactive (input gated)");
        err.context = QStringLiteral("SessionGate");
        err.recoverable = true;
        itKnown->availability = DeckGamepadDeviceAvailability::Unavailable;
        setDeviceAvailability(deviceId, DeckGamepadDeviceAvailability::Unavailable);
        setDeviceError(deviceId, err);
        return false;
    }

    DeckGamepadDeviceOpenResult openResult;
    if (m_accessBroker) {
        openResult = m_accessBroker->openDevice(devpath);
    } else {
        DeviceAccessBroker fallback;
        fallback.setRuntimeConfig(m_runtimeConfig);
        openResult = fallback.openDevice(devpath);
    }

    if (!openResult.ok()) {
        DeckGamepadError err = openResult.error;
        if (err.isOk()) {
            err.code = DeckGamepadErrorCode::Io;
            err.message = QStringLiteral("Failed to open gamepad device");
            err.context = QStringLiteral("open(%1)").arg(devpath);
            err.recoverable = m_runtimeConfig.enableAutoRetryOpen;
        }

        itKnown->availability = DeckGamepadDeviceAvailability::Unavailable;
        setDeviceAvailability(deviceId, DeckGamepadDeviceAvailability::Unavailable);
        setDeviceError(deviceId, err);

        if (m_runtimeConfig.enableAutoRetryOpen && err.recoverable) {
            const qint64 nowMs = QDateTime::currentMSecsSinceEpoch();
            const int attempt = qMax(0, itKnown->retryAttempt);
            const int base = qMax(0, m_runtimeConfig.retryBackoffMinMs);
            const int maxDelay = qMax(base, m_runtimeConfig.retryBackoffMaxMs);
            const int delay = qMin(maxDelay, base * (1 << qMin(attempt, 10)));
            itKnown->nextRetryWallclockMs = nowMs + delay;
            itKnown->retryAttempt = attempt + 1;
            scheduleNextRetry();
        }

        return false;
    }

    int fd = openResult.fd;

    bool autoGrabFailed = false;
    DeckGamepadError autoGrabError;

    if (m_runtimeConfig.grabMode == DeckGamepadEvdevGrabMode::Exclusive
        || m_runtimeConfig.grabMode == DeckGamepadEvdevGrabMode::Auto) {
        errno = 0;
        if (ioctl(fd, EVIOCGRAB, 1) < 0) {
            const int grabErrno = errno;
            if (m_runtimeConfig.grabMode == DeckGamepadEvdevGrabMode::Exclusive) {
                if (openResult.releaseDevice) {
                    openResult.releaseDevice();
                    openResult.releaseDevice = {};
                }
                ::close(fd);

                DeckGamepadError err;
                err.code = DeckGamepadErrorCode::Io;
                err.sysErrno = grabErrno;
                err.message = QStringLiteral("Failed to grab gamepad device (EVIOCGRAB)");
                err.context = QStringLiteral("EVIOCGRAB");
                err.recoverable = m_runtimeConfig.enableAutoRetryOpen;

                itKnown->availability = DeckGamepadDeviceAvailability::Unavailable;
                setDeviceAvailability(deviceId, DeckGamepadDeviceAvailability::Unavailable);
                setDeviceError(deviceId, err);
                scheduleNextRetry();
                return false;
            }

            // grabMode=Auto: prefer exclusive grab, but fall back to shared mode if grabbing fails.
            autoGrabFailed = true;
            autoGrabError.code = DeckGamepadErrorCode::Io;
            autoGrabError.sysErrno = grabErrno;
            autoGrabError.message = QStringLiteral("Failed to grab gamepad device (EVIOCGRAB), falling back to shared");
            autoGrabError.context = QStringLiteral("EVIOCGRAB");
            autoGrabError.hint = QStringLiteral("running in shared mode (grabMode=Auto fallback)");
            autoGrabError.recoverable = false;
        }
    }

    DeckGamepadDevice *device = new DeckGamepadDevice(deviceId, devpath, m_sdlDb, this);
    device->m_calibrationData = m_calibrationData.get();
    if (!device->openWithFd(fd, std::move(openResult.releaseDevice))) {
        if (openResult.releaseDevice) {
            openResult.releaseDevice();
        }
        ::close(fd);
        device->deleteLater();

        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::Io;
        err.message = QStringLiteral("Failed to initialize gamepad device");
        err.context = QStringLiteral("DeckGamepadDevice::openWithFd(%1)").arg(devpath);
        err.recoverable = m_runtimeConfig.enableAutoRetryOpen;

        itKnown->availability = DeckGamepadDeviceAvailability::Unavailable;
        setDeviceAvailability(deviceId, DeckGamepadDeviceAvailability::Unavailable);
        setDeviceError(deviceId, err);
        scheduleNextRetry();
        return false;
    }

    m_devices.insert(deviceId, device);

    itKnown->availability = DeckGamepadDeviceAvailability::Available;
    itKnown->info.name = device->name();
    itKnown->info.guid = device->guid();
    itKnown->info.supportsRumble = device->supportsRumble();
    itKnown->retryAttempt = 0;
    itKnown->nextRetryWallclockMs = 0;
    setDeviceAvailability(deviceId, DeckGamepadDeviceAvailability::Available);
    if (autoGrabFailed) {
        setDeviceError(deviceId, autoGrabError);
    } else {
        setDeviceError(deviceId, DeckGamepadError{});
    }
    Q_EMIT deviceInfoChanged(deviceId, itKnown->info);

    connect(device, &DeckGamepadDevice::buttonEvent, this, &DeckGamepadBackend::buttonEvent);
    connect(device, &DeckGamepadDevice::axisEvent, this, &DeckGamepadBackend::axisEvent);
    connect(device, &DeckGamepadDevice::hatEvent, this, &DeckGamepadBackend::hatEvent);
    connect(device, &DeckGamepadDevice::disconnected, this, [this, deviceId, devpath]() {
        auto it = m_devices.find(deviceId);
        if (it != m_devices.end()) {
            it.value()->deleteLater();
            m_devices.erase(it);
        }

        auto itKnown = m_knownDevices.find(deviceId);
        if (itKnown != m_knownDevices.end()) {
            itKnown->availability = DeckGamepadDeviceAvailability::Unavailable;
            DeckGamepadError err;
            err.code = DeckGamepadErrorCode::Io;
            err.message = QStringLiteral("Gamepad device disconnected");
            err.context = QStringLiteral("read(%1)").arg(devpath);
            err.recoverable = m_runtimeConfig.enableAutoRetryOpen;
            setDeviceAvailability(deviceId, DeckGamepadDeviceAvailability::Unavailable);
            setDeviceError(deviceId, err);
        }

        emit gamepadDisconnected(deviceId);
        scheduleNextRetry();
    });

    emit gamepadConnected(deviceId, device->name());
    return true;
}

void DeckGamepadBackend::closeGamepad(int deviceId)
{
    auto it = m_devices.find(deviceId);
    if (it != m_devices.end()) {
        it.value()->close();
        it.value()->deleteLater();
        m_devices.erase(it);
        emit gamepadDisconnected(deviceId);
    }
}

int DeckGamepadBackend::getUnusedDeviceId()
{
    for (int i = 0; i < MAX_GAMEPADS; i++) {
        if (!m_knownDevices.contains(i) && !m_devices.contains(i)) {
            return i;
        }
    }
    return -1;
}

void DeckGamepadBackend::handleUdevEvent()
{
    struct udev_device *dev = udev_monitor_receive_device(m_udevMonitor);
    if (!dev) {
        return;
    }

	    const char *action = udev_device_get_action(dev);
	    const char *devnode = udev_device_get_devnode(dev);

	    if (!action || !devnode) {
	        udev_device_unref(dev);
	        return;
	    }

	    QString devpath(devnode);
	    if (!devpath.contains("/js")) {
	        if (strcmp(action, "add") == 0) {
	            const char *isJoystick = udev_device_get_property_value(dev, "ID_INPUT_JOYSTICK");
	            const char *isGamepad = udev_device_get_property_value(dev, "ID_INPUT_GAMEPAD");
	            const bool hasGamepadHint = (isJoystick != nullptr) || (isGamepad != nullptr);
	            const bool udevCandidate = (isJoystick && strcmp(isJoystick, "1") == 0)
	                || (isGamepad && strcmp(isGamepad, "1") == 0);

	            bool candidate = udevCandidate;
	            int probeErrno = 0;
	            if (!candidate) {
	                candidate = isGamepadDevice(devpath, &probeErrno);
	                if (!candidate && (probeErrno == EACCES || probeErrno == EPERM) && !hasGamepadHint) {
	                    candidate = true;
	                }
	            }

	            if (candidate) {
	                openGamepad(dev, devpath);
	            }
	        } else if (strcmp(action, "remove") == 0) {
	            auto it = m_devicePaths.find(devpath);
	            if (it != m_devicePaths.end()) {
	                const int deviceId = it.value();

	                if (m_devices.contains(deviceId)) {
	                    closeGamepad(deviceId);
	                }

	                setDeviceAvailability(deviceId, DeckGamepadDeviceAvailability::Removed);
	                setDeviceError(deviceId, DeckGamepadError{});

	                m_knownDevices.remove(deviceId);
	                m_devicePaths.remove(devpath);
	                scheduleNextRetry();
	            }
	        }
	    }

	    udev_device_unref(dev);
	}

void DeckGamepadBackend::handleSessionGateActiveChanged(bool active)
{
    if (!m_running) {
        return;
    }

    if (!active) {
        const QList<int> connectedIds = m_devices.keys();
        for (int id : connectedIds) {
            closeGamepad(id);

            DeckGamepadError err;
            err.code = DeckGamepadErrorCode::Io;
            err.message = QStringLiteral("Session inactive (input gated)");
            err.context = QStringLiteral("SessionGate");
            err.recoverable = true;
            setDeviceAvailability(id, DeckGamepadDeviceAvailability::Unavailable);
            setDeviceError(id, err);
        }
        return;
    }

    // 会话恢复：触发一次重试（退避由现有逻辑控制）。
    retryUnavailableDevices();
}

void DeckGamepadBackend::retryUnavailableDevices()
{
    if (!m_runtimeConfig.enableAutoRetryOpen) {
        return;
    }
    if (m_sessionGate && m_sessionGate->enabled() && !m_sessionGate->isActive()) {
        return;
    }

    // udev hotplug may be unavailable; rescan periodically to discover newly added devices.
    if (!m_udevMonitor) {
        probeGamepads();
    }

    const qint64 nowMs = QDateTime::currentMSecsSinceEpoch();
    for (auto it = m_knownDevices.begin(); it != m_knownDevices.end(); ++it) {
        if (it.value().availability != DeckGamepadDeviceAvailability::Unavailable) {
            continue;
        }
        if (!it.value().lastError.recoverable) {
            continue;
        }

        const qint64 nextMs = it.value().nextRetryWallclockMs;
        if (nextMs > 0 && nowMs < nextMs) {
            continue;
        }

        (void)tryOpenGamepad(it.key(), it.value().devpath);
    }

    scheduleNextRetry();
}

void DeckGamepadBackend::scheduleNextRetry()
{
    if (!m_runtimeConfig.enableAutoRetryOpen || !m_retryTimer) {
        return;
    }
    if (m_sessionGate && m_sessionGate->enabled() && !m_sessionGate->isActive()) {
        return;
    }

    bool hasRecoverableUnavailable = false;
    qint64 nextWallclockMs = 0;
    for (auto it = m_knownDevices.constBegin(); it != m_knownDevices.constEnd(); ++it) {
        if (it.value().availability != DeckGamepadDeviceAvailability::Unavailable) {
            continue;
        }
        if (!it.value().lastError.recoverable) {
            continue;
        }
        hasRecoverableUnavailable = true;
        if (it.value().nextRetryWallclockMs <= 0) {
            nextWallclockMs = 0;
            break;
        }

        if (nextWallclockMs == 0 || it.value().nextRetryWallclockMs < nextWallclockMs) {
            nextWallclockMs = it.value().nextRetryWallclockMs;
        }
    }

    // If udev monitor is unavailable, keep a slow poll running to detect hotplug without netlink uevents.
    if (!m_udevMonitor) {
        const qint64 nowMs = QDateTime::currentMSecsSinceEpoch();
        const int pollIntervalMs = qMax(2000, qMax(0, m_runtimeConfig.retryBackoffMinMs));
        const qint64 pollNextMs = nowMs + pollIntervalMs;

        if (!hasRecoverableUnavailable) {
            hasRecoverableUnavailable = true;
            nextWallclockMs = pollNextMs;
        } else if (nextWallclockMs == 0 || pollNextMs < nextWallclockMs) {
            nextWallclockMs = pollNextMs;
        }
    }

    if (!hasRecoverableUnavailable) {
        m_retryTimer->stop();
        return;
    }

    const qint64 nowMs = QDateTime::currentMSecsSinceEpoch();
    const int delayMs = (nextWallclockMs <= 0) ? 0 : int(qMax<qint64>(0, nextWallclockMs - nowMs));
    if (m_retryTimer->isActive()) {
        if (m_retryTimer->remainingTime() <= delayMs) {
            return;
        }
        m_retryTimer->stop();
    }
    m_retryTimer->start(delayMs);
}

void DeckGamepadBackend::setError(DeckGamepadError error)
{
    m_lastError = std::move(error);
    Q_EMIT lastErrorChanged(m_lastError);
}

void DeckGamepadBackend::setDeviceAvailability(int deviceId,
                                               DeckGamepadDeviceAvailability availability)
{
    auto it = m_knownDevices.find(deviceId);
    if (it == m_knownDevices.end()) {
        return;
    }

    if (it.value().availability == availability) {
        return;
    }

    it.value().availability = availability;
    Q_EMIT deviceAvailabilityChanged(deviceId, availability);
}

void DeckGamepadBackend::setDeviceError(int deviceId, DeckGamepadError error)
{
    auto it = m_knownDevices.find(deviceId);
    if (it == m_knownDevices.end()) {
        return;
    }

    it.value().lastError = std::move(error);
    Q_EMIT deviceErrorChanged(deviceId, it.value().lastError);
}

QList<int> DeckGamepadBackend::knownGamepads() const
{
    return m_knownDevices.keys();
}

QList<int> DeckGamepadBackend::connectedGamepads() const
{
    return m_devices.keys();
}

DeckGamepadDevice *DeckGamepadBackend::device(int id) const
{
    return m_devices.value(id, nullptr);
}

DeckGamepadDeviceInfo DeckGamepadBackend::deviceInfo(int deviceId) const
{
    auto it = m_knownDevices.find(deviceId);
    if (it == m_knownDevices.end()) {
        return DeckGamepadDeviceInfo{};
    }
    return it.value().info;
}

QString DeckGamepadBackend::deviceUid(int deviceId) const
{
    return deviceInfo(deviceId).deviceUid;
}

DeckGamepadDeviceAvailability DeckGamepadBackend::deviceAvailability(int deviceId) const
{
    auto it = m_knownDevices.find(deviceId);
    if (it == m_knownDevices.end()) {
        return DeckGamepadDeviceAvailability::Removed;
    }
    return it.value().availability;
}

DeckGamepadError DeckGamepadBackend::deviceLastError(int deviceId) const
{
    auto it = m_knownDevices.find(deviceId);
    if (it == m_knownDevices.end()) {
        return DeckGamepadError{};
    }
    return it.value().lastError;
}

void DeckGamepadBackend::setAxisDeadzone(int deviceId, uint32_t axis, float deadzone)
{
    DeckGamepadDevice *dev = m_devices.value(deviceId, nullptr);
    if (!dev) {
        qWarning() << "Cannot set axis deadzone: device" << deviceId << "not found";
        return;
    }

    deadzone = qBound(0.0f, deadzone, 1.0f);

    dev->m_customDeadzones[axis] = deadzone;
    qDebug() << "Set axis" << axis << "deadzone to" << deadzone << "for device" << deviceId;
}

void DeckGamepadBackend::setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity)
{
    DeckGamepadDevice *dev = m_devices.value(deviceId, nullptr);
    if (!dev) {
        qWarning() << "Cannot set axis sensitivity: device" << deviceId << "not found";
        return;
    }

    sensitivity = qBound(0.1f, sensitivity, 5.0f);

    dev->m_axisSensitivity[axis] = sensitivity;
    qDebug() << "Set axis" << axis << "sensitivity to" << sensitivity << "for device" << deviceId;
}

void DeckGamepadBackend::resetAxisSettings(int deviceId, uint32_t axis)
{
    DeckGamepadDevice *dev = m_devices.value(deviceId, nullptr);
    if (!dev) {
        qWarning() << "Cannot reset axis settings: device" << deviceId << "not found";
        return;
    }

    dev->m_customDeadzones.remove(axis);
    dev->m_axisSensitivity.remove(axis);
    qDebug() << "Reset axis" << axis << "settings for device" << deviceId;
}

bool DeckGamepadBackend::startVibration(int deviceId,
                                        float weakMagnitude,
                                        float strongMagnitude,
                                        int duration_ms)
{
    DeckGamepadDevice *dev = m_devices.value(deviceId, nullptr);
    if (!dev) {
        qWarning() << "Cannot start vibration: device" << deviceId << "not found";
        return false;
    }

    return dev->startVibration(weakMagnitude, strongMagnitude, duration_ms);
}

void DeckGamepadBackend::stopVibration(int deviceId)
{
    DeckGamepadDevice *dev = m_devices.value(deviceId, nullptr);
    if (!dev) {
        qWarning() << "Cannot stop vibration: device" << deviceId << "not found";
        return;
    }

    dev->stopVibration();
}

void DeckGamepadBackend::loadCalibration()
{
    const QString path = m_runtimeConfig.resolveCalibrationPath();
    if (!m_calibrationStore) {
        m_calibrationStore = std::make_unique<JsonCalibrationStore>(path);
    } else {
        m_calibrationStore->setFilePath(path);
    }

    CalibrationData data;
    if (!m_calibrationStore->load(data)) {
        qWarning() << "Failed to load calibration store:" << m_calibrationStore->errorString();
        data = CalibrationData{};
    }

    if (!m_calibrationData) {
        m_calibrationData = std::make_unique<CalibrationData>();
    }
    *m_calibrationData = data;
}

int DeckGamepadBackend::reloadSdlDb(const QString &path)
{
    QString dbPath = path;
    if (dbPath.isEmpty()) {
        dbPath = findDefaultSdlDatabase();
    }

    if (dbPath.isEmpty()) {
        qWarning() << "SDL GameController DB not found";
        return -1;
    }

    int count = m_sdlDb->loadDatabase(dbPath);
    if (count > 0) {
        qInfo() << "Reloaded SDL GameController DB:" << count << "devices from" << dbPath;
        emit sdlDatabaseLoaded(count);
    }

    return count;
}

int DeckGamepadBackend::sdlMappingCount() const
{
    return m_sdlDb ? m_sdlDb->mappingCount() : 0;
}

QString DeckGamepadBackend::findDefaultSdlDatabase()
{
    return m_runtimeConfig.resolveSdlDbPath();
}

DECKGAMEPAD_END_NAMESPACE
