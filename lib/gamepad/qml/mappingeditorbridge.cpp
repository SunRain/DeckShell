// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "mappingeditorbridge.h"

#include "gamepadmanager.h"

#include <deckshell/deckgamepad/core/deckgamepad.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcustommappingmanager.h>

#include <QtCore/QDebug>
#include <QtCore/QMetaObject>
#include <QtCore/QRegularExpression>
#include <QtCore/QThread>
#include <QtGui/QClipboard>
#include <QtGui/QGuiApplication>

#include <type_traits>
#include <utility>

extern "C" {
#include <linux/input.h>
}

using namespace deckshell::deckgamepad;

namespace {
template <typename Func>
auto invokeBlocking(DeckGamepadCustomMappingManager *manager, Func &&func)
{
    using Ret = std::invoke_result_t<Func>;

    if (!manager) {
        if constexpr (!std::is_void_v<Ret>) {
            return Ret{};
        } else {
            return;
        }
    }

    if (QThread::currentThread() == manager->thread()) {
        if constexpr (!std::is_void_v<Ret>) {
            return func();
        } else {
            func();
            return;
        }
    }

    if constexpr (std::is_void_v<Ret>) {
        QMetaObject::invokeMethod(manager, std::forward<Func>(func), Qt::BlockingQueuedConnection);
        return;
    } else {
        Ret result{};
        QMetaObject::invokeMethod(manager, [&] { result = func(); }, Qt::BlockingQueuedConnection);
        return result;
    }
}
}

MappingEditorBridge::MappingEditorBridge(QObject *parent)
    : QObject(parent)
    , m_captureTimer(new QTimer(this))
{
    m_captureTimer->setSingleShot(true);
    m_captureTimer->setInterval(CAPTURE_TIMEOUT_MS);
    connect(m_captureTimer, &QTimer::timeout, this, &MappingEditorBridge::onCaptureTimerTimeout);

    qDebug() << "MappingEditorBridge initialized";
}

MappingEditorBridge::~MappingEditorBridge()
{
    stopCapture();
}

GamepadManager *MappingEditorBridge::resolveManager() const
{
    if (m_manager) {
        return m_manager;
    }

    // Prefer the QML singleton instance bound to the current engine to avoid creating a second
    // GamepadManager (which would lead to "supported=true" but MappingEditorBridge using a different service).
    if (auto *engine = qmlEngine(const_cast<MappingEditorBridge *>(this))) {
        auto *singleton = engine->singletonInstance<GamepadManager *>(QStringLiteral("DeckShell.DeckGamepad"),
                                                                      QStringLiteral("GamepadManager"));
        if (singleton) {
            m_manager = singleton;
            return singleton;
        }

        // Ensure the manager is created through the QML singleton factory, so `_deckGamepadService` injection
        // (if present) is applied consistently.
        m_manager = GamepadManager::create(engine, nullptr);
        return m_manager;
    }

    // Fallback for non-QML usage.
    m_manager = GamepadManager::instance();
    return m_manager;
}

DeckGamepadCustomMappingManager *MappingEditorBridge::mappingManager() const
{
    auto *mgr = resolveManager();
    if (!mgr || !mgr->service()) {
        return nullptr;
    }
    return mgr->service()->customMappingManager();
}

void MappingEditorBridge::setDeviceId(int deviceId)
{
    if (m_deviceId == deviceId) {
        return;
    }

    m_deviceId = deviceId;
    Q_EMIT deviceIdChanged();
    Q_EMIT deviceNameChanged();
    Q_EMIT deviceGuidChanged();
    Q_EMIT mappingChanged();

    qDebug() << "MappingEditorBridge: Device ID set to" << deviceId;
}

QString MappingEditorBridge::deviceName() const
{
    auto *mgr = resolveManager();
    if (!mgr || !mgr->service() || m_deviceId < 0) {
        return QString();
    }

    return mgr->service()->deviceName(m_deviceId);
}

QString MappingEditorBridge::deviceGuid() const
{
    auto *mgr = resolveManager();
    if (!mgr || !mgr->service() || m_deviceId < 0) {
        return QString();
    }

    return mgr->service()->deviceGuid(m_deviceId);
}

bool MappingEditorBridge::hasCustomMapping() const
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return false;
    }

    return invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->hasCustomMapping(deviceId); });
}

bool MappingEditorBridge::isMappingComplete() const
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return false;
    }

    return invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->isMappingComplete(deviceId); });
}

void MappingEditorBridge::createMapping()
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        Q_EMIT captureFailed(QStringLiteral("No mapping manager or invalid device"));
        return;
    }

    const QString guid = invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->createCustomMapping(deviceId); });
    if (guid.isEmpty()) {
        Q_EMIT captureFailed(QStringLiteral("Failed to create mapping"));
        return;
    }

    Q_EMIT mappingChanged();
    qDebug() << "Created custom mapping for device" << m_deviceId;
}

bool MappingEditorBridge::saveMapping()
{
    auto *mgr = mappingManager();
    if (!mgr) {
        Q_EMIT mappingSaveFailed(QStringLiteral("Mapping manager not available"));
        return false;
    }

    if (invokeBlocking(mgr, [mgr] { return mgr->saveToFile(); })) {
        if (m_deviceId >= 0) {
            invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->applyMapping(deviceId); });
        }
        Q_EMIT mappingSaved();
        qDebug() << "Saved custom mappings";
        return true;
    }

    Q_EMIT mappingSaveFailed(QStringLiteral("Failed to write file"));
    return false;
}

void MappingEditorBridge::removeMapping()
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return;
    }

    invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { mgr->removeCustomMapping(deviceId); });
    Q_EMIT mappingChanged();
    qDebug() << "Removed custom mapping for device" << m_deviceId;
}

bool MappingEditorBridge::loadPreset(const QString &presetName)
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return false;
    }

    if (invokeBlocking(mgr, [mgr, deviceId = m_deviceId, presetName] { return mgr->loadPreset(deviceId, presetName); })) {
        Q_EMIT mappingChanged();
        qDebug() << "Loaded preset" << presetName << "for device" << m_deviceId;
        return true;
    }

    return false;
}

QStringList MappingEditorBridge::availablePresets()
{
    auto *mgr = mappingManager();
    if (!mgr) {
        return QStringList();
    }

    return invokeBlocking(mgr, [mgr] { return mgr->availablePresets(); });
}

QString MappingEditorBridge::getButtonMapping(int logicalButton)
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0 || !hasCustomMapping()) {
        return QString();
    }

    const DeviceMapping mapping =
        invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->getCustomMapping(deviceId); });

    for (auto it = mapping.buttonMap.constBegin(); it != mapping.buttonMap.constEnd(); ++it) {
        if (it.value() == static_cast<GamepadButton>(logicalButton)) {
            return buttonCodeToName(it.key());
        }
    }

    return QString();
}

QString MappingEditorBridge::getAxisMapping(int logicalAxis)
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0 || !hasCustomMapping()) {
        return QString();
    }

    const DeviceMapping mapping =
        invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->getCustomMapping(deviceId); });

    for (auto it = mapping.axisMap.constBegin(); it != mapping.axisMap.constEnd(); ++it) {
        if (it.value() == static_cast<GamepadAxis>(logicalAxis)) {
            const int evdevCode = it.key();
            const bool inverted = mapping.invertedAxes.contains(evdevCode);
            QString name = axisCodeToName(evdevCode);
            return inverted ? name + QStringLiteral(" (Inverted)") : name;
        }
    }

    return QString();
}

void MappingEditorBridge::clearButtonMapping(int logicalButton)
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return;
    }

    invokeBlocking(mgr, [mgr, deviceId = m_deviceId, logicalButton] {
        mgr->clearButtonMapping(deviceId, static_cast<GamepadButton>(logicalButton));
    });
    Q_EMIT mappingChanged();
}

void MappingEditorBridge::clearAxisMapping(int logicalAxis)
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return;
    }

    invokeBlocking(mgr, [mgr, deviceId = m_deviceId, logicalAxis] {
        mgr->clearAxisMapping(deviceId, static_cast<GamepadAxis>(logicalAxis));
    });
    Q_EMIT mappingChanged();
}

void MappingEditorBridge::startCapture(const QString &inputType)
{
    if (m_deviceId < 0) {
        Q_EMIT captureFailed(QStringLiteral("No device selected"));
        return;
    }

    auto *mgr = resolveManager();
    if (!mgr) {
        Q_EMIT captureFailed(QStringLiteral("GamepadManager not available"));
        return;
    }

    if (!hasCustomMapping()) {
        createMapping();
        if (!hasCustomMapping()) {
            return;
        }
    }

    m_isListening = true;
    m_captureType = inputType;
    Q_EMIT listeningChanged();

    m_captureTimer->start();

    if (inputType == QLatin1StringView("button")) {
        connect(mgr,
                &GamepadManager::buttonPressed,
                this,
                &MappingEditorBridge::onButtonPressed,
                Qt::UniqueConnection);
    } else if (inputType == QLatin1StringView("axis")) {
        m_lastAxisValues.clear();
        connect(mgr, &GamepadManager::axisChanged, this, &MappingEditorBridge::onAxisChanged, Qt::UniqueConnection);
    }

    qDebug() << "Started input capture for" << inputType << "on device" << m_deviceId;
}

void MappingEditorBridge::stopCapture()
{
    if (!m_isListening) {
        return;
    }

    m_isListening = false;
    Q_EMIT listeningChanged();

    m_captureTimer->stop();

    if (m_manager) {
        disconnect(m_manager, &GamepadManager::buttonPressed, this, &MappingEditorBridge::onButtonPressed);
        disconnect(m_manager, &GamepadManager::axisChanged, this, &MappingEditorBridge::onAxisChanged);
    }

    m_lastAxisValues.clear();

    qDebug() << "Stopped input capture";
}

void MappingEditorBridge::setCaptureTarget(int logicalButton, int logicalAxis)
{
    m_captureLogicalButton = logicalButton;
    m_captureLogicalAxis = logicalAxis;
}

QStringList MappingEditorBridge::getMissingMappings()
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return QStringList();
    }

    return invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->getMissingMappings(deviceId); });
}

QString MappingEditorBridge::exportToSdl()
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return QString();
    }

    return invokeBlocking(mgr, [mgr, deviceId = m_deviceId] { return mgr->exportToSdlString(deviceId); });
}

bool MappingEditorBridge::importFromSdl(const QString &sdlString)
{
    auto *mgr = mappingManager();
    if (!mgr || m_deviceId < 0) {
        return false;
    }

    if (invokeBlocking(mgr, [mgr, deviceId = m_deviceId, sdlString] { return mgr->importFromSdlString(deviceId, sdlString); })) {
        Q_EMIT mappingChanged();
        return true;
    }

    return false;
}

void MappingEditorBridge::copyToClipboard(const QString &text)
{
    QClipboard *clipboard = QGuiApplication::clipboard();
    if (!clipboard) {
        qWarning() << "MappingEditorBridge: Clipboard not available";
        Q_EMIT clipboardOperationCompleted(false, tr("Clipboard not available"));
        return;
    }

    clipboard->setText(text, QClipboard::Clipboard);
    qDebug() << "MappingEditorBridge: Copied to clipboard:" << text.length() << "characters";
    Q_EMIT clipboardOperationCompleted(true, tr("SDL string copied to clipboard"));
}

QString MappingEditorBridge::pasteFromClipboard()
{
    QClipboard *clipboard = QGuiApplication::clipboard();
    if (!clipboard) {
        qWarning() << "MappingEditorBridge: Clipboard not available";
        return QString();
    }

    const QString text = clipboard->text(QClipboard::Clipboard).trimmed();
    qDebug() << "MappingEditorBridge: Pasted from clipboard:" << text.length() << "characters";
    return text;
}

bool MappingEditorBridge::validateSdlString(const QString &sdlString)
{
    if (sdlString.isEmpty()) {
        qDebug() << "MappingEditorBridge: SDL string is empty";
        return false;
    }

    const QStringList parts = sdlString.split(QLatin1Char(','));
    if (parts.size() < 3) {
        qDebug() << "MappingEditorBridge: SDL string has too few parts:" << parts.size();
        return false;
    }

    const QString guid = parts[0];
    if (guid.length() != 32) {
        qDebug() << "MappingEditorBridge: GUID length invalid:" << guid.length();
        return false;
    }

    const QRegularExpression hexPattern(QStringLiteral("^[0-9a-fA-F]{32}$"));
    if (!hexPattern.match(guid).hasMatch()) {
        qDebug() << "MappingEditorBridge: GUID format invalid (not hex)";
        return false;
    }

    const QString name = parts[1].trimmed();
    if (name.isEmpty()) {
        qDebug() << "MappingEditorBridge: Device name is empty";
        return false;
    }

    bool hasMappings = false;
    for (int i = 2; i < parts.size(); ++i) {
        const QString mapping = parts[i].trimmed();
        if (!mapping.isEmpty() && mapping.contains(QLatin1Char(':'))) {
            hasMappings = true;
            break;
        }
    }

    if (!hasMappings) {
        qDebug() << "MappingEditorBridge: No valid mappings found";
        return false;
    }

    qDebug() << "MappingEditorBridge: SDL string validation passed";
    return true;
}

void MappingEditorBridge::onButtonPressed(int deviceId, int button)
{
    if (!m_isListening || deviceId != m_deviceId || m_captureType != QLatin1StringView("button")) {
        return;
    }

    stopCapture();

    auto *mgr = mappingManager();
    if (!mgr || m_captureLogicalButton < 0) {
        Q_EMIT captureFailed(QStringLiteral("Mapping manager not available"));
        return;
    }

    const int evdevCode = resolvePhysicalButtonCode(deviceId, button);
    if (evdevCode < 0) {
        Q_EMIT captureFailed(QStringLiteral("Failed to resolve physical button code"));
        return;
    }

    invokeBlocking(mgr, [mgr, deviceId = m_deviceId, logicalButton = m_captureLogicalButton, evdevCode] {
        mgr->setButtonMapping(deviceId, static_cast<GamepadButton>(logicalButton), evdevCode);
    });

    const QString inputName = buttonCodeToName(evdevCode);
    Q_EMIT inputCaptured(evdevCode, inputName);
    Q_EMIT mappingChanged();

    qDebug() << "Captured button:" << inputName << "for logical button" << m_captureLogicalButton;
}

void MappingEditorBridge::onAxisChanged(int deviceId, int axis, double value)
{
    if (!m_isListening || deviceId != m_deviceId || m_captureType != QLatin1StringView("axis")) {
        return;
    }

    const double lastValue = m_lastAxisValues.value(axis, 0.0);
    const double delta = qAbs(value - lastValue);
    m_lastAxisValues[axis] = value;

    if (delta < AXIS_THRESHOLD) {
        return;
    }

    stopCapture();

    auto *mgr = mappingManager();
    if (!mgr || m_captureLogicalAxis < 0) {
        Q_EMIT captureFailed(QStringLiteral("Mapping manager not available"));
        return;
    }

    const int evdevCode = resolvePhysicalAxisCode(deviceId, axis);
    if (evdevCode < 0) {
        Q_EMIT captureFailed(QStringLiteral("Failed to resolve physical axis code"));
        return;
    }

    const bool inverted = (value < -0.5);

    invokeBlocking(mgr, [mgr, deviceId = m_deviceId, logicalAxis = m_captureLogicalAxis, evdevCode, inverted] {
        mgr->setAxisMapping(deviceId, static_cast<GamepadAxis>(logicalAxis), evdevCode, inverted);
    });

    QString inputName = axisCodeToName(evdevCode);
    if (inverted) {
        inputName += QStringLiteral(" (Inverted)");
    }

    Q_EMIT inputCaptured(evdevCode, inputName);
    Q_EMIT mappingChanged();

    qDebug() << "Captured axis:" << inputName << "for logical axis" << m_captureLogicalAxis;
}

void MappingEditorBridge::onCaptureTimerTimeout()
{
    if (!m_isListening) {
        return;
    }

    stopCapture();
    Q_EMIT captureTimeout();
    qWarning() << "Input capture timed out";
}

int MappingEditorBridge::resolvePhysicalButtonCode(int deviceId, int logicalButton) const
{
    auto *mgr = mappingManager();
    if (!mgr) {
        return -1;
    }

    const DeviceMapping mapping =
        invokeBlocking(mgr, [mgr, deviceId] { return mgr->getCustomMapping(deviceId); });
    const auto logical = static_cast<GamepadButton>(logicalButton);
    for (auto it = mapping.buttonMap.constBegin(); it != mapping.buttonMap.constEnd(); ++it) {
        if (it.value() == logical) {
            return it.key();
        }
    }

    // 兜底：若当前 mapping 无法反查，尝试按通用 Xbox 语义回退（与 backend 默认映射一致）。
    switch (logical) {
    case GAMEPAD_BUTTON_A:
        return BTN_SOUTH;
    case GAMEPAD_BUTTON_B:
        return BTN_EAST;
    case GAMEPAD_BUTTON_X:
        return BTN_NORTH;
    case GAMEPAD_BUTTON_Y:
        return BTN_WEST;
    case GAMEPAD_BUTTON_L1:
        return BTN_TL;
    case GAMEPAD_BUTTON_R1:
        return BTN_TR;
    case GAMEPAD_BUTTON_L2:
        return BTN_TL2;
    case GAMEPAD_BUTTON_R2:
        return BTN_TR2;
    case GAMEPAD_BUTTON_SELECT:
        return BTN_SELECT;
    case GAMEPAD_BUTTON_START:
        return BTN_START;
    case GAMEPAD_BUTTON_L3:
        return BTN_THUMBL;
    case GAMEPAD_BUTTON_R3:
        return BTN_THUMBR;
    case GAMEPAD_BUTTON_GUIDE:
        return BTN_MODE;
    default:
        return -1;
    }
}

int MappingEditorBridge::resolvePhysicalAxisCode(int deviceId, int logicalAxis) const
{
    auto *mgr = mappingManager();
    if (!mgr) {
        return -1;
    }

    const DeviceMapping mapping =
        invokeBlocking(mgr, [mgr, deviceId] { return mgr->getCustomMapping(deviceId); });
    const auto logical = static_cast<GamepadAxis>(logicalAxis);
    for (auto it = mapping.axisMap.constBegin(); it != mapping.axisMap.constEnd(); ++it) {
        if (it.value() == logical) {
            return it.key();
        }
    }

    switch (logical) {
    case GAMEPAD_AXIS_LEFT_X:
        return ABS_X;
    case GAMEPAD_AXIS_LEFT_Y:
        return ABS_Y;
    case GAMEPAD_AXIS_RIGHT_X:
        return ABS_RX;
    case GAMEPAD_AXIS_RIGHT_Y:
        return ABS_RY;
    case GAMEPAD_AXIS_TRIGGER_LEFT:
        return ABS_Z;
    case GAMEPAD_AXIS_TRIGGER_RIGHT:
        return ABS_RZ;
    default:
        return -1;
    }
}

QString MappingEditorBridge::buttonCodeToName(int evdevCode) const
{
    switch (evdevCode) {
    case BTN_SOUTH:
        return QStringLiteral("BTN_SOUTH (A)");
    case BTN_EAST:
        return QStringLiteral("BTN_EAST (B)");
    case BTN_NORTH:
        return QStringLiteral("BTN_NORTH (X)");
    case BTN_WEST:
        return QStringLiteral("BTN_WEST (Y)");
    case BTN_TL:
        return QStringLiteral("BTN_TL (LB)");
    case BTN_TR:
        return QStringLiteral("BTN_TR (RB)");
    case BTN_TL2:
        return QStringLiteral("BTN_TL2 (LT Button)");
    case BTN_TR2:
        return QStringLiteral("BTN_TR2 (RT Button)");
    case BTN_SELECT:
        return QStringLiteral("BTN_SELECT (Back)");
    case BTN_START:
        return QStringLiteral("BTN_START");
    case BTN_MODE:
        return QStringLiteral("BTN_MODE (Guide)");
    case BTN_THUMBL:
        return QStringLiteral("BTN_THUMBL (L3)");
    case BTN_THUMBR:
        return QStringLiteral("BTN_THUMBR (R3)");
    default:
        if (evdevCode >= BTN_JOYSTICK) {
            return QStringLiteral("Button %1").arg(evdevCode - BTN_JOYSTICK);
        }
        return QStringLiteral("BTN_%1").arg(evdevCode);
    }
}

QString MappingEditorBridge::axisCodeToName(int evdevCode) const
{
    switch (evdevCode) {
    case ABS_X:
        return QStringLiteral("ABS_X (Left Stick X)");
    case ABS_Y:
        return QStringLiteral("ABS_Y (Left Stick Y)");
    case ABS_Z:
        return QStringLiteral("ABS_Z (Left Trigger)");
    case ABS_RX:
        return QStringLiteral("ABS_RX (Right Stick X)");
    case ABS_RY:
        return QStringLiteral("ABS_RY (Right Stick Y)");
    case ABS_RZ:
        return QStringLiteral("ABS_RZ (Right Trigger)");
    case ABS_HAT0X:
        return QStringLiteral("ABS_HAT0X (D-Pad X)");
    case ABS_HAT0Y:
        return QStringLiteral("ABS_HAT0Y (D-Pad Y)");
    default:
        return QStringLiteral("ABS_%1 (Axis %1)").arg(evdevCode);
    }
}

QString MappingEditorBridge::logicalButtonToName(int logicalButton) const
{
    switch (logicalButton) {
    case GAMEPAD_BUTTON_A:
        return QStringLiteral("A");
    case GAMEPAD_BUTTON_B:
        return QStringLiteral("B");
    case GAMEPAD_BUTTON_X:
        return QStringLiteral("X");
    case GAMEPAD_BUTTON_Y:
        return QStringLiteral("Y");
    case GAMEPAD_BUTTON_L1:
        return QStringLiteral("LB");
    case GAMEPAD_BUTTON_R1:
        return QStringLiteral("RB");
    case GAMEPAD_BUTTON_L2:
        return QStringLiteral("LT");
    case GAMEPAD_BUTTON_R2:
        return QStringLiteral("RT");
    case GAMEPAD_BUTTON_SELECT:
        return QStringLiteral("Select");
    case GAMEPAD_BUTTON_START:
        return QStringLiteral("Start");
    case GAMEPAD_BUTTON_L3:
        return QStringLiteral("L3");
    case GAMEPAD_BUTTON_R3:
        return QStringLiteral("R3");
    case GAMEPAD_BUTTON_GUIDE:
        return QStringLiteral("Guide");
    case GAMEPAD_BUTTON_DPAD_UP:
        return QStringLiteral("D-Pad Up");
    case GAMEPAD_BUTTON_DPAD_DOWN:
        return QStringLiteral("D-Pad Down");
    case GAMEPAD_BUTTON_DPAD_LEFT:
        return QStringLiteral("D-Pad Left");
    case GAMEPAD_BUTTON_DPAD_RIGHT:
        return QStringLiteral("D-Pad Right");
    default:
        return QStringLiteral("Button %1").arg(logicalButton);
    }
}

QString MappingEditorBridge::logicalAxisToName(int logicalAxis) const
{
    switch (logicalAxis) {
    case GAMEPAD_AXIS_LEFT_X:
        return QStringLiteral("Left Stick X");
    case GAMEPAD_AXIS_LEFT_Y:
        return QStringLiteral("Left Stick Y");
    case GAMEPAD_AXIS_RIGHT_X:
        return QStringLiteral("Right Stick X");
    case GAMEPAD_AXIS_RIGHT_Y:
        return QStringLiteral("Right Stick Y");
    case GAMEPAD_AXIS_TRIGGER_LEFT:
        return QStringLiteral("Left Trigger");
    case GAMEPAD_AXIS_TRIGGER_RIGHT:
        return QStringLiteral("Right Trigger");
    default:
        return QStringLiteral("Axis %1").arg(logicalAxis);
    }
}
