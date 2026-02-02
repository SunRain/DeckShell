// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// Action/Intent 映射器：把 button/dpad/axis 状态映射为稳定 actionId（press/release/repeat）。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/core/deckgamepad.h>
#include <deckshell/deckgamepad/extras/actionmappingprofile.h>

#include <QtCore/QHash>
#include <QtCore/QObject>
#include <QtCore/QSet>
#include <QtCore/QString>
#include <QtCore/QTimer>

DECKGAMEPAD_BEGIN_NAMESPACE

class DECKGAMEPAD_EXPORT DeckGamepadActionMapper final : public QObject
{
    Q_OBJECT

public:
    enum class DiagonalPolicy {
        PreferCardinal = 0, // 默认：只输出一个方向，并对轴做锁定避免抖动翻转
        AllowDiagonal,
    };
    Q_ENUM(DiagonalPolicy)

    explicit DeckGamepadActionMapper(QObject *parent = nullptr);

    bool enabled() const;
    void setEnabled(bool enabled);

    double deadzone() const;
    void setDeadzone(double deadzone);

    double hysteresis() const;
    void setHysteresis(double hysteresis);

    DiagonalPolicy diagonalPolicy() const;
    void setDiagonalPolicy(DiagonalPolicy policy);

    bool releaseOnCenter() const;
    void setReleaseOnCenter(bool enabled);

    // repeat 默认关闭：仅针对“方向动作”（DPad/LeftStick 的方向映射）输出 repeated=true 的定时事件。
    bool repeatEnabled() const;
    void setRepeatEnabled(bool enabled);

    int repeatDelayMs() const;
    void setRepeatDelayMs(int delayMs);

    int repeatIntervalMs() const;
    void setRepeatIntervalMs(int intervalMs);

    void reset();
    void applyNavigationPreset();
    void applyActionMappingProfile(const ActionMappingProfile &profile);

    void processButton(GamepadButton button, bool pressed, int timeMs = 0);
    void processAxis(GamepadAxis axis, double value, int timeMs = 0);

Q_SIGNALS:
    void enabledChanged();

    void actionEvent(DeckGamepadActionEvent event);
    void actionTriggered(const QString &actionId, bool pressed, bool repeated);

private:
    enum class StickLockAxis {
        None = 0,
        Horizontal,
        Vertical,
    };

    void setActionPressed(const QString &actionId, bool pressed, bool repeated, int timeMs);

    void updateFromDpad(int timeMs);
    void updateFromLeftStick(int timeMs);
    void updateMergedNavigation(int timeMs);

    void stopRepeat();
    void startRepeatIfConfigured();
    void emitRepeatTick();

    bool m_enabled = true;

    double m_deadzone = 0.25;
    double m_hysteresis = 0.05;
    DiagonalPolicy m_diagonalPolicy = DiagonalPolicy::PreferCardinal;
    bool m_releaseOnCenter = true;
    bool m_repeatEnabled = false;
    int m_repeatDelayMs = 350;
    int m_repeatIntervalMs = 80;

    ActionMappingProfile::NavigationPriority m_navigationPriority = ActionMappingProfile::NavigationPriority::DpadOverLeftStick;

    struct AxisBinding {
        QString negativeActionId;
        QString positiveActionId;
        float threshold = 0.0f;
        bool hasNegative = false;
        bool hasPositive = false;
        bool hasThreshold = false;
    };

    QHash<GamepadButton, QString> m_buttonBindings;
    QHash<GamepadAxis, AxisBinding> m_axisBindings;

    struct DirectionOutput {
        QString actionId;
        bool pressed = false;
    };

    DirectionOutput m_outUp;
    DirectionOutput m_outDown;
    DirectionOutput m_outLeft;
    DirectionOutput m_outRight;

    struct AxisState {
        bool negativeActive = false;
        bool positiveActive = false;
    };
    QHash<GamepadAxis, AxisState> m_axisState;

    QTimer m_repeatDelayTimer;
    QTimer m_repeatIntervalTimer;
    QSet<QString> m_repeatActiveDirections; // 当前处于“方向激活”的 actionId 集合（repeat tick 的目标）

    // sources
    bool m_dpadUp = false;
    bool m_dpadDown = false;
    bool m_dpadLeft = false;
    bool m_dpadRight = false;

    double m_leftX = 0.0;
    double m_leftY = 0.0;
    bool m_stickUp = false;
    bool m_stickDown = false;
    bool m_stickLeft = false;
    bool m_stickRight = false;
    StickLockAxis m_stickLock = StickLockAxis::None;

    // merged output state
    QHash<QString, bool> m_actionPressed;
};

DECKGAMEPAD_END_NAMESPACE
