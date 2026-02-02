// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "deckgamepadactionmapper.h"

#include <QtCore/qmath.h>

DECKGAMEPAD_BEGIN_NAMESPACE

static double clamp01(double v)
{
    if (v < 0.0) {
        return 0.0;
    }
    if (v > 1.0) {
        return 1.0;
    }
    return v;
}

DeckGamepadActionMapper::DeckGamepadActionMapper(QObject *parent)
    : QObject(parent)
{
    m_repeatDelayTimer.setSingleShot(true);
    m_repeatDelayTimer.setTimerType(Qt::PreciseTimer);
    m_repeatIntervalTimer.setSingleShot(false);
    m_repeatIntervalTimer.setTimerType(Qt::PreciseTimer);

    connect(&m_repeatDelayTimer, &QTimer::timeout, this, [this]() {
        emitRepeatTick();
        if (m_repeatEnabled && m_repeatIntervalMs > 0 && !m_repeatActiveDirections.isEmpty()) {
            m_repeatIntervalTimer.setInterval(qMax(1, m_repeatIntervalMs));
            m_repeatIntervalTimer.start();
        }
    });

    connect(&m_repeatIntervalTimer, &QTimer::timeout, this, [this]() { emitRepeatTick(); });

    applyNavigationPreset();
}

bool DeckGamepadActionMapper::enabled() const
{
    return m_enabled;
}

void DeckGamepadActionMapper::setEnabled(bool enabled)
{
    if (m_enabled == enabled) {
        return;
    }
    m_enabled = enabled;
    if (!m_enabled) {
        reset();
    }
    Q_EMIT enabledChanged();
}

double DeckGamepadActionMapper::deadzone() const
{
    return m_deadzone;
}

void DeckGamepadActionMapper::setDeadzone(double deadzone)
{
    deadzone = clamp01(deadzone);
    if (qFuzzyCompare(m_deadzone, deadzone)) {
        return;
    }
    m_deadzone = deadzone;
    updateFromLeftStick(0);
}

double DeckGamepadActionMapper::hysteresis() const
{
    return m_hysteresis;
}

void DeckGamepadActionMapper::setHysteresis(double hysteresis)
{
    hysteresis = clamp01(hysteresis);
    if (qFuzzyCompare(m_hysteresis, hysteresis)) {
        return;
    }
    m_hysteresis = hysteresis;
    updateFromLeftStick(0);
}

DeckGamepadActionMapper::DiagonalPolicy DeckGamepadActionMapper::diagonalPolicy() const
{
    return m_diagonalPolicy;
}

void DeckGamepadActionMapper::setDiagonalPolicy(DiagonalPolicy policy)
{
    if (m_diagonalPolicy == policy) {
        return;
    }
    m_diagonalPolicy = policy;
    // 切换策略时释放锁，避免状态卡住。
    m_stickLock = StickLockAxis::None;
    updateFromLeftStick(0);
}

bool DeckGamepadActionMapper::releaseOnCenter() const
{
    return m_releaseOnCenter;
}

void DeckGamepadActionMapper::setReleaseOnCenter(bool enabled)
{
    if (m_releaseOnCenter == enabled) {
        return;
    }
    m_releaseOnCenter = enabled;
    updateFromLeftStick(0);
}

bool DeckGamepadActionMapper::repeatEnabled() const
{
    return m_repeatEnabled;
}

void DeckGamepadActionMapper::setRepeatEnabled(bool enabled)
{
    if (m_repeatEnabled == enabled) {
        return;
    }

    m_repeatEnabled = enabled;

    stopRepeat();
    startRepeatIfConfigured();
}

int DeckGamepadActionMapper::repeatDelayMs() const
{
    return m_repeatDelayMs;
}

void DeckGamepadActionMapper::setRepeatDelayMs(int delayMs)
{
    delayMs = qMax(0, delayMs);
    if (m_repeatDelayMs == delayMs) {
        return;
    }
    m_repeatDelayMs = delayMs;

    stopRepeat();
    startRepeatIfConfigured();
}

int DeckGamepadActionMapper::repeatIntervalMs() const
{
    return m_repeatIntervalMs;
}

void DeckGamepadActionMapper::setRepeatIntervalMs(int intervalMs)
{
    if (intervalMs < 0) {
        intervalMs = 0;
    }
    if (m_repeatIntervalMs == intervalMs) {
        return;
    }
    m_repeatIntervalMs = intervalMs;

    stopRepeat();
    startRepeatIfConfigured();
}

void DeckGamepadActionMapper::reset()
{
    stopRepeat();
    m_repeatActiveDirections.clear();
    m_outUp = DirectionOutput{};
    m_outDown = DirectionOutput{};
    m_outLeft = DirectionOutput{};
    m_outRight = DirectionOutput{};
    m_axisState.clear();

    // release all merged actions
    const auto keys = m_actionPressed.keys();
    for (const QString &k : keys) {
        if (m_actionPressed.value(k)) {
            setActionPressed(k, false, false, 0);
        }
    }

    m_dpadUp = false;
    m_dpadDown = false;
    m_dpadLeft = false;
    m_dpadRight = false;

    m_leftX = 0.0;
    m_leftY = 0.0;
    m_stickUp = false;
    m_stickDown = false;
    m_stickLeft = false;
    m_stickRight = false;
    m_stickLock = StickLockAxis::None;
}

void DeckGamepadActionMapper::applyNavigationPreset()
{
    applyActionMappingProfile(ActionMappingProfile::createNavigationPreset());
}

void DeckGamepadActionMapper::applyActionMappingProfile(const ActionMappingProfile &profile)
{
    reset();

    if (profile.hasNavigationPriority) {
        m_navigationPriority = profile.navigationPriority;
    }

    if (profile.hasRepeatConfig) {
        setRepeatDelayMs(profile.repeat.delayMs);
        setRepeatIntervalMs(profile.repeat.intervalMs);
        setRepeatEnabled(profile.repeat.enabled);
    }

    m_buttonBindings.clear();
    for (auto it = profile.buttonBindings.constBegin(); it != profile.buttonBindings.constEnd(); ++it) {
        if (it.value().actionId.isEmpty()) {
            continue;
        }
        m_buttonBindings.insert(it.key(), it.value().actionId);
    }

    m_axisBindings.clear();
    for (auto it = profile.axisBindings.constBegin(); it != profile.axisBindings.constEnd(); ++it) {
        AxisBinding dst;
        dst.hasThreshold = it.value().hasThreshold;
        dst.threshold = it.value().threshold;

        if (it.value().hasNegative && !it.value().negative.actionId.isEmpty()) {
            dst.hasNegative = true;
            dst.negativeActionId = it.value().negative.actionId;
        }
        if (it.value().hasPositive && !it.value().positive.actionId.isEmpty()) {
            dst.hasPositive = true;
            dst.positiveActionId = it.value().positive.actionId;
        }

        if (dst.hasThreshold || dst.hasNegative || dst.hasPositive) {
            m_axisBindings.insert(it.key(), dst);
        }
    }

    // 预置：初始化输出集合（便于 reset 时统一 release）
    // 注意：此处仅初始化常用 actionId；动态 actionId 会在首次触发时自动加入。
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavUp), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavDown), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavLeft), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavRight), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavAccept), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavBack), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavMenu), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavTabNext), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavTabPrev), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavPageNext), false);
    m_actionPressed.insert(QString::fromLatin1(DeckGamepadActionId::NavPagePrev), false);
}

void DeckGamepadActionMapper::processButton(GamepadButton button, bool pressed, int timeMs)
{
    if (!m_enabled) {
        return;
    }

    const bool repeated = false;

    switch (button) {
    case GAMEPAD_BUTTON_DPAD_UP:
        m_dpadUp = pressed;
        updateFromDpad(timeMs);
        return;
    case GAMEPAD_BUTTON_DPAD_DOWN:
        m_dpadDown = pressed;
        updateFromDpad(timeMs);
        return;
    case GAMEPAD_BUTTON_DPAD_LEFT:
        m_dpadLeft = pressed;
        updateFromDpad(timeMs);
        return;
    case GAMEPAD_BUTTON_DPAD_RIGHT:
        m_dpadRight = pressed;
        updateFromDpad(timeMs);
        return;
    default:
        break;
    }

    const QString actionId = m_buttonBindings.value(button);
    if (actionId.isEmpty()) {
        return;
    }
    setActionPressed(actionId, pressed, repeated, timeMs);
}

void DeckGamepadActionMapper::processAxis(GamepadAxis axis, double value, int timeMs)
{
    if (!m_enabled) {
        return;
    }

    switch (axis) {
    case GAMEPAD_AXIS_LEFT_X:
        m_leftX = qBound(-1.0, value, 1.0);
        updateFromLeftStick(timeMs);
        return;
    case GAMEPAD_AXIS_LEFT_Y:
        m_leftY = qBound(-1.0, value, 1.0);
        updateFromLeftStick(timeMs);
        return;
    default:
        break;
    }

    const AxisBinding binding = m_axisBindings.value(axis);
    if (!binding.hasNegative && !binding.hasPositive) {
        return;
    }

    const double releaseThreshold = clamp01(binding.hasThreshold ? binding.threshold : m_deadzone);
    const double pressThreshold = clamp01(releaseThreshold + m_hysteresis);

    AxisState &state = m_axisState[axis];

    const double v = qBound(-1.0, value, 1.0);

    bool nextNegative = state.negativeActive;
    if (state.negativeActive) {
        if (v > -releaseThreshold) {
            nextNegative = false;
        }
    } else {
        if (v < -pressThreshold) {
            nextNegative = true;
        }
    }

    bool nextPositive = state.positiveActive;
    if (state.positiveActive) {
        if (v < releaseThreshold) {
            nextPositive = false;
        }
    } else {
        if (v > pressThreshold) {
            nextPositive = true;
        }
    }

    if (binding.hasNegative && !binding.negativeActionId.isEmpty() && nextNegative != state.negativeActive) {
        state.negativeActive = nextNegative;
        setActionPressed(binding.negativeActionId, nextNegative, false, timeMs);
    } else {
        state.negativeActive = nextNegative;
    }

    if (binding.hasPositive && !binding.positiveActionId.isEmpty() && nextPositive != state.positiveActive) {
        state.positiveActive = nextPositive;
        setActionPressed(binding.positiveActionId, nextPositive, false, timeMs);
    } else {
        state.positiveActive = nextPositive;
    }
}

void DeckGamepadActionMapper::setActionPressed(const QString &actionId, bool pressed, bool repeated, int timeMs)
{
    const bool prev = m_actionPressed.value(actionId, false);
    if (prev == pressed && !repeated) {
        return;
    }

    m_actionPressed.insert(actionId, pressed);

    DeckGamepadActionEvent ev;
    ev.actionId = actionId;
    ev.pressed = pressed;
    ev.repeated = repeated;
    ev.timeMs = timeMs;
    Q_EMIT actionEvent(ev);
    Q_EMIT actionTriggered(actionId, pressed, repeated);
}

void DeckGamepadActionMapper::stopRepeat()
{
    m_repeatDelayTimer.stop();
    m_repeatIntervalTimer.stop();
}

void DeckGamepadActionMapper::startRepeatIfConfigured()
{
    if (!m_repeatEnabled) {
        return;
    }
    if (m_repeatIntervalMs <= 0) {
        return;
    }
    if (m_repeatActiveDirections.isEmpty()) {
        return;
    }

    m_repeatDelayTimer.setInterval(qMax(0, m_repeatDelayMs));
    m_repeatIntervalTimer.setInterval(qMax(1, m_repeatIntervalMs));

    if (m_repeatDelayTimer.interval() == 0) {
        emitRepeatTick();
        m_repeatIntervalTimer.start();
        return;
    }

    m_repeatDelayTimer.start();
}

void DeckGamepadActionMapper::emitRepeatTick()
{
    if (!m_repeatEnabled) {
        return;
    }
    if (m_repeatActiveDirections.isEmpty()) {
        return;
    }
    if (m_repeatIntervalMs <= 0) {
        return;
    }

    const bool pressed = true;
    const bool repeated = true;
    const int timeMs = 0;

    for (const QString &actionId : m_repeatActiveDirections) {
        setActionPressed(actionId, pressed, repeated, timeMs);
    }
}

void DeckGamepadActionMapper::updateFromDpad(int timeMs)
{
    updateMergedNavigation(timeMs);
}

void DeckGamepadActionMapper::updateFromLeftStick(int timeMs)
{
    const AxisBinding xBinding = m_axisBindings.value(GAMEPAD_AXIS_LEFT_X);
    const AxisBinding yBinding = m_axisBindings.value(GAMEPAD_AXIS_LEFT_Y);

    const double releaseThresholdX = clamp01(xBinding.hasThreshold ? xBinding.threshold : m_deadzone);
    const double releaseThresholdY = clamp01(yBinding.hasThreshold ? yBinding.threshold : m_deadzone);
    const double pressThresholdX = clamp01(releaseThresholdX + m_hysteresis);
    const double pressThresholdY = clamp01(releaseThresholdY + m_hysteresis);

    const double absX = qAbs(m_leftX);
    const double absY = qAbs(m_leftY);

    if (m_releaseOnCenter && absX <= releaseThresholdX && absY <= releaseThresholdY) {
        m_stickUp = m_stickDown = m_stickLeft = m_stickRight = false;
        m_stickLock = StickLockAxis::None;
        updateMergedNavigation(timeMs);
        return;
    }

    // candidate directions based on thresholds
    bool candLeft = false;
    bool candRight = false;
    bool candUp = false;
    bool candDown = false;

    // horizontal
    if (m_stickLeft || m_stickRight) {
        if (absX <= releaseThresholdX) {
            m_stickLeft = false;
            m_stickRight = false;
            if (m_stickLock == StickLockAxis::Horizontal) {
                m_stickLock = StickLockAxis::None;
            }
        }
    } else {
        if (absX >= pressThresholdX) {
            candLeft = (m_leftX < 0.0);
            candRight = (m_leftX > 0.0);
        }
    }

    // vertical (注意：Y 轴向上通常为负)
    if (m_stickUp || m_stickDown) {
        if (absY <= releaseThresholdY) {
            m_stickUp = false;
            m_stickDown = false;
            if (m_stickLock == StickLockAxis::Vertical) {
                m_stickLock = StickLockAxis::None;
            }
        }
    } else {
        if (absY >= pressThresholdY) {
            candUp = (m_leftY < 0.0);
            candDown = (m_leftY > 0.0);
        }
    }

    if (m_diagonalPolicy == DiagonalPolicy::AllowDiagonal) {
        if (!(m_stickLeft || m_stickRight)) {
            m_stickLeft = candLeft;
            m_stickRight = candRight;
        }
        if (!(m_stickUp || m_stickDown)) {
            m_stickUp = candUp;
            m_stickDown = candDown;
        }
        updateMergedNavigation(timeMs);
        return;
    }

    // PreferCardinal: lock to one axis to avoid jitter flipping.
    if (m_stickLock == StickLockAxis::None) {
        const bool candH = candLeft || candRight;
        const bool candV = candUp || candDown;
        if (candH && candV) {
            m_stickLock = (absX >= absY) ? StickLockAxis::Horizontal : StickLockAxis::Vertical;
        } else if (candH) {
            m_stickLock = StickLockAxis::Horizontal;
        } else if (candV) {
            m_stickLock = StickLockAxis::Vertical;
        }
    }

    if (m_stickLock == StickLockAxis::Horizontal) {
        if (!(m_stickLeft || m_stickRight)) {
            m_stickLeft = candLeft;
            m_stickRight = candRight;
        } else {
            // allow sign flip within lock
            if (absX >= pressThresholdX) {
                const bool nextLeft = (m_leftX < 0.0);
                const bool nextRight = (m_leftX > 0.0);
                m_stickLeft = nextLeft;
                m_stickRight = nextRight;
            }
        }
        m_stickUp = false;
        m_stickDown = false;
    } else if (m_stickLock == StickLockAxis::Vertical) {
        if (!(m_stickUp || m_stickDown)) {
            m_stickUp = candUp;
            m_stickDown = candDown;
        } else {
            if (absY >= pressThresholdY) {
                const bool nextUp = (m_leftY < 0.0);
                const bool nextDown = (m_leftY > 0.0);
                m_stickUp = nextUp;
                m_stickDown = nextDown;
            }
        }
        m_stickLeft = false;
        m_stickRight = false;
    }

    updateMergedNavigation(timeMs);
}

void DeckGamepadActionMapper::updateMergedNavigation(int timeMs)
{
    const QString dpadUpId = m_buttonBindings.value(GAMEPAD_BUTTON_DPAD_UP);
    const QString dpadDownId = m_buttonBindings.value(GAMEPAD_BUTTON_DPAD_DOWN);
    const QString dpadLeftId = m_buttonBindings.value(GAMEPAD_BUTTON_DPAD_LEFT);
    const QString dpadRightId = m_buttonBindings.value(GAMEPAD_BUTTON_DPAD_RIGHT);

    const AxisBinding stickX = m_axisBindings.value(GAMEPAD_AXIS_LEFT_X);
    const AxisBinding stickY = m_axisBindings.value(GAMEPAD_AXIS_LEFT_Y);

    const QString stickLeftId = stickX.hasNegative ? stickX.negativeActionId : QString{};
    const QString stickRightId = stickX.hasPositive ? stickX.positiveActionId : QString{};
    const QString stickUpId = stickY.hasNegative ? stickY.negativeActionId : QString{};
    const QString stickDownId = stickY.hasPositive ? stickY.positiveActionId : QString{};

    const bool dpadActive =
        (m_dpadUp && !dpadUpId.isEmpty()) || (m_dpadDown && !dpadDownId.isEmpty())
        || (m_dpadLeft && !dpadLeftId.isEmpty()) || (m_dpadRight && !dpadRightId.isEmpty());
    const bool stickActive =
        (m_stickUp && !stickUpId.isEmpty()) || (m_stickDown && !stickDownId.isEmpty())
        || (m_stickLeft && !stickLeftId.isEmpty()) || (m_stickRight && !stickRightId.isEmpty());

    bool useDpad = false;
    if (m_navigationPriority == ActionMappingProfile::NavigationPriority::LeftStickOverDpad) {
        useDpad = (!stickActive && dpadActive);
    } else {
        useDpad = dpadActive;
    }

    const bool nextUpPressed = useDpad ? (m_dpadUp && !dpadUpId.isEmpty()) : (m_stickUp && !stickUpId.isEmpty());
    const bool nextDownPressed = useDpad ? (m_dpadDown && !dpadDownId.isEmpty()) : (m_stickDown && !stickDownId.isEmpty());
    const bool nextLeftPressed = useDpad ? (m_dpadLeft && !dpadLeftId.isEmpty()) : (m_stickLeft && !stickLeftId.isEmpty());
    const bool nextRightPressed = useDpad ? (m_dpadRight && !dpadRightId.isEmpty()) : (m_stickRight && !stickRightId.isEmpty());

    const QString nextUpId = useDpad ? dpadUpId : stickUpId;
    const QString nextDownId = useDpad ? dpadDownId : stickDownId;
    const QString nextLeftId = useDpad ? dpadLeftId : stickLeftId;
    const QString nextRightId = useDpad ? dpadRightId : stickRightId;

    auto updateDirection = [this](DirectionOutput &out, const QString &nextId, bool pressed, int timeMs) {
        if (out.actionId != nextId) {
            if (out.pressed && !out.actionId.isEmpty()) {
                setActionPressed(out.actionId, false, false, timeMs);
            }
            out.actionId = nextId;
            out.pressed = false;
        }

        if (out.pressed == pressed) {
            return;
        }

        out.pressed = pressed;
        if (!out.actionId.isEmpty()) {
            setActionPressed(out.actionId, pressed, false, timeMs);
        }
    };

    updateDirection(m_outUp, nextUpId, nextUpPressed, timeMs);
    updateDirection(m_outDown, nextDownId, nextDownPressed, timeMs);
    updateDirection(m_outLeft, nextLeftId, nextLeftPressed, timeMs);
    updateDirection(m_outRight, nextRightId, nextRightPressed, timeMs);

    QSet<QString> nextRepeatDirections;
    if (m_outUp.pressed && !m_outUp.actionId.isEmpty()) {
        nextRepeatDirections.insert(m_outUp.actionId);
    }
    if (m_outDown.pressed && !m_outDown.actionId.isEmpty()) {
        nextRepeatDirections.insert(m_outDown.actionId);
    }
    if (m_outLeft.pressed && !m_outLeft.actionId.isEmpty()) {
        nextRepeatDirections.insert(m_outLeft.actionId);
    }
    if (m_outRight.pressed && !m_outRight.actionId.isEmpty()) {
        nextRepeatDirections.insert(m_outRight.actionId);
    }

    if (m_repeatActiveDirections != nextRepeatDirections) {
        m_repeatActiveDirections = nextRepeatDirections;
        stopRepeat();
        startRepeatIfConfigured();
    }
}

DECKGAMEPAD_END_NAMESPACE
