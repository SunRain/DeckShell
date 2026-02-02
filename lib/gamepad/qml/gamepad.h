// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <array>
#include <QtCore/QObject>
#include <QtCore/QTimer>
#include <QtCore/QString>
#include <QtQml/QQmlParserStatus>
#include <QtQml/qqml.h>

class GamepadManager;

class Gamepad : public QObject, public QQmlParserStatus
{
    Q_OBJECT
    Q_INTERFACES(QQmlParserStatus)
    QML_ELEMENT

    Q_PROPERTY(int deviceId READ deviceId WRITE setDeviceId NOTIFY deviceIdChanged FINAL)
    Q_PROPERTY(bool connected READ connected NOTIFY connectedChanged FINAL)
    Q_PROPERTY(QString name READ name NOTIFY nameChanged FINAL)

    // 高频轴/hat 的属性通知合并（coalesce）配置与可观测性。
    // - coalesceIntervalMs <= 0：不合并，收到事件后立即发出属性通知。
    // - coalesceIntervalMs > 0：按窗口合并，窗口结束时批量发出属性通知（raw event 信号不受影响）。
    Q_PROPERTY(int coalesceIntervalMs READ coalesceIntervalMs WRITE setCoalesceIntervalMs NOTIFY coalesceIntervalMsChanged FINAL)
    Q_PROPERTY(quint64 axisRawEventCount READ axisRawEventCount NOTIFY statsChanged FINAL)
    Q_PROPERTY(quint64 axisNotifyCount READ axisNotifyCount NOTIFY statsChanged FINAL)
    Q_PROPERTY(quint64 axisDroppedEventCount READ axisDroppedEventCount NOTIFY statsChanged FINAL)
    Q_PROPERTY(quint64 hatRawEventCount READ hatRawEventCount NOTIFY statsChanged FINAL)
    Q_PROPERTY(quint64 hatNotifyCount READ hatNotifyCount NOTIFY statsChanged FINAL)
    Q_PROPERTY(quint64 hatDroppedEventCount READ hatDroppedEventCount NOTIFY statsChanged FINAL)
	    Q_PROPERTY(int lastCoalesceLatencyMs READ lastCoalesceLatencyMs NOTIFY statsChanged FINAL)

	    Q_PROPERTY(int hatDirection READ hatDirection NOTIFY hatDirectionChanged FINAL)
	    Q_PROPERTY(int hat1Direction READ hat1Direction NOTIFY hat1DirectionChanged FINAL)
	    Q_PROPERTY(int hat2Direction READ hat2Direction NOTIFY hat2DirectionChanged FINAL)
	    Q_PROPERTY(int hat3Direction READ hat3Direction NOTIFY hat3DirectionChanged FINAL)

    Q_PROPERTY(bool buttonA READ buttonA NOTIFY buttonAChanged FINAL)
    Q_PROPERTY(bool buttonB READ buttonB NOTIFY buttonBChanged FINAL)
    Q_PROPERTY(bool buttonX READ buttonX NOTIFY buttonXChanged FINAL)
    Q_PROPERTY(bool buttonY READ buttonY NOTIFY buttonYChanged FINAL)
    Q_PROPERTY(bool buttonL1 READ buttonL1 NOTIFY buttonL1Changed FINAL)
    Q_PROPERTY(bool buttonR1 READ buttonR1 NOTIFY buttonR1Changed FINAL)
    Q_PROPERTY(bool buttonL2 READ buttonL2 NOTIFY buttonL2Changed FINAL)
    Q_PROPERTY(bool buttonR2 READ buttonR2 NOTIFY buttonR2Changed FINAL)
    Q_PROPERTY(bool buttonSelect READ buttonSelect NOTIFY buttonSelectChanged FINAL)
    Q_PROPERTY(bool buttonStart READ buttonStart NOTIFY buttonStartChanged FINAL)
    Q_PROPERTY(bool buttonL3 READ buttonL3 NOTIFY buttonL3Changed FINAL)
    Q_PROPERTY(bool buttonR3 READ buttonR3 NOTIFY buttonR3Changed FINAL)
    Q_PROPERTY(bool buttonGuide READ buttonGuide NOTIFY buttonGuideChanged FINAL)
    Q_PROPERTY(bool buttonDpadUp READ buttonDpadUp NOTIFY buttonDpadUpChanged FINAL)
    Q_PROPERTY(bool buttonDpadDown READ buttonDpadDown NOTIFY buttonDpadDownChanged FINAL)
    Q_PROPERTY(bool buttonDpadLeft READ buttonDpadLeft NOTIFY buttonDpadLeftChanged FINAL)
    Q_PROPERTY(bool buttonDpadRight READ buttonDpadRight NOTIFY buttonDpadRightChanged FINAL)

    Q_PROPERTY(double axisLeftX READ axisLeftX NOTIFY axisLeftXChanged FINAL)
    Q_PROPERTY(double axisLeftY READ axisLeftY NOTIFY axisLeftYChanged FINAL)
    Q_PROPERTY(double axisRightX READ axisRightX NOTIFY axisRightXChanged FINAL)
    Q_PROPERTY(double axisRightY READ axisRightY NOTIFY axisRightYChanged FINAL)
    Q_PROPERTY(double axisTriggerLeft READ axisTriggerLeft NOTIFY axisTriggerLeftChanged FINAL)
    Q_PROPERTY(double axisTriggerRight READ axisTriggerRight NOTIFY axisTriggerRightChanged FINAL)

public:
    explicit Gamepad(QObject *parent = nullptr);
    ~Gamepad() override;

    void classBegin() override;
    void componentComplete() override;

    int deviceId() const;
    void setDeviceId(int deviceId);

    bool connected() const;
    QString name() const;

    int coalesceIntervalMs() const;
    void setCoalesceIntervalMs(int intervalMs);

    quint64 axisRawEventCount() const;
    quint64 axisNotifyCount() const;
    quint64 axisDroppedEventCount() const;
    quint64 hatRawEventCount() const;
    quint64 hatNotifyCount() const;
    quint64 hatDroppedEventCount() const;
	    int lastCoalesceLatencyMs() const;

	    int hatDirection() const;
	    int hat1Direction() const;
	    int hat2Direction() const;
	    int hat3Direction() const;

    bool buttonA() const;
    bool buttonB() const;
    bool buttonX() const;
    bool buttonY() const;
    bool buttonL1() const;
    bool buttonR1() const;
    bool buttonL2() const;
    bool buttonR2() const;
    bool buttonSelect() const;
    bool buttonStart() const;
    bool buttonL3() const;
    bool buttonR3() const;
    bool buttonGuide() const;
    bool buttonDpadUp() const;
    bool buttonDpadDown() const;
    bool buttonDpadLeft() const;
    bool buttonDpadRight() const;

    double axisLeftX() const;
    double axisLeftY() const;
    double axisRightX() const;
    double axisRightY() const;
    double axisTriggerLeft() const;
    double axisTriggerRight() const;

Q_SIGNALS:
    void deviceIdChanged();
    void connectedChanged();
    void nameChanged();

    void coalesceIntervalMsChanged();
	    void statsChanged();

	    void hatDirectionChanged();
	    void hat1DirectionChanged();
	    void hat2DirectionChanged();
	    void hat3DirectionChanged();

    void buttonAChanged();
    void buttonBChanged();
    void buttonXChanged();
    void buttonYChanged();
    void buttonL1Changed();
    void buttonR1Changed();
    void buttonL2Changed();
    void buttonR2Changed();
    void buttonSelectChanged();
    void buttonStartChanged();
    void buttonL3Changed();
    void buttonR3Changed();
    void buttonGuideChanged();
    void buttonDpadUpChanged();
    void buttonDpadDownChanged();
    void buttonDpadLeftChanged();
    void buttonDpadRightChanged();

    void axisLeftXChanged();
    void axisLeftYChanged();
    void axisRightXChanged();
    void axisRightYChanged();
    void axisTriggerLeftChanged();
    void axisTriggerRightChanged();

    // Coalesced state change signals
    void buttonChanged(int button, bool pressed);
    void axisChanged(int axis, double value);
    void hatChanged(int hat, int value);

    // Raw events
    void buttonEvent(int button, bool pressed, int timeMs);
    void axisEvent(int axis, double value, int timeMs);
    void hatEvent(int hat, int value, int timeMs);

private:
    void ensureManagerResolved();
    void rebuildSubscriptions(GamepadManager *mgr);

    void handleDeviceConnected(int deviceId);
    void handleDeviceDisconnected(int deviceId);

    void handleButtonEvent(deckshell::deckgamepad::DeckGamepadButtonEvent event);
    void handleAxisEvent(deckshell::deckgamepad::DeckGamepadAxisEvent event);
    void handleHatEvent(deckshell::deckgamepad::DeckGamepadHatEvent event);

    void flushPendingChanges();

    bool buttonState(deckshell::deckgamepad::GamepadButton button) const;
    void setButtonState(deckshell::deckgamepad::GamepadButton button, bool pressed);
    void emitButtonNotify(deckshell::deckgamepad::GamepadButton button);

    double axisValue(deckshell::deckgamepad::GamepadAxis axis) const;
    void setAxisValue(deckshell::deckgamepad::GamepadAxis axis, double value);
    void emitAxisNotify(deckshell::deckgamepad::GamepadAxis axis);

    void resetState();
    void syncDeviceInfo();

    GamepadManager *m_manager = nullptr;

    int m_deviceId = -1;
    bool m_connected = false;
    QString m_name;

	    std::array<bool, deckshell::deckgamepad::GAMEPAD_BUTTON_MAX> m_buttonStates{};
	    std::array<double, deckshell::deckgamepad::GAMEPAD_AXIS_MAX> m_axisValues{};
	    std::array<int, 4> m_hatDirectionByHat{ { deckshell::deckgamepad::GAMEPAD_HAT_CENTER,
	                                              deckshell::deckgamepad::GAMEPAD_HAT_CENTER,
	                                              deckshell::deckgamepad::GAMEPAD_HAT_CENTER,
	                                              deckshell::deckgamepad::GAMEPAD_HAT_CENTER } };

	    uint32_t m_pendingAxisMask = 0;
	    uint8_t m_pendingHatMask = 0;
	    std::array<int, 4> m_pendingHatDirectionByHat{ { deckshell::deckgamepad::GAMEPAD_HAT_CENTER,
	                                                     deckshell::deckgamepad::GAMEPAD_HAT_CENTER,
	                                                     deckshell::deckgamepad::GAMEPAD_HAT_CENTER,
	                                                     deckshell::deckgamepad::GAMEPAD_HAT_CENTER } };

    int m_coalesceIntervalMs = 16;
    QTimer m_coalesceTimer;
    qint64 m_pendingCoalesceStartWallclockMs = -1;

    quint64 m_axisRawEventCount = 0;
    quint64 m_axisNotifyCount = 0;
    quint64 m_hatRawEventCount = 0;
    quint64 m_hatNotifyCount = 0;
    int m_lastCoalesceLatencyMs = 0;
};
