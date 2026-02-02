// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadkeynavigation.h"

#include "gamepad.h"
#include "gamepadactionrouter.h"
#include "gamepadmanager.h"

#include <deckshell/deckgamepad/extras/deckgamepadactionkeymapping.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QCoreApplication>
#include <QtGui/QGuiApplication>
#include <QtGui/QInputMethod>
#include <QtGui/QKeyEvent>
#include <QtGui/QWindow>
#include <QtQml/QQmlEngine>

GamepadKeyNavigation::GamepadKeyNavigation(QObject *parent)
    : QObject(parent)
    , m_mapper(this)
{
    m_mapper.setEnabled(false);
    m_mapper.applyNavigationPreset();

    connect(&m_mapper, &deckshell::deckgamepad::DeckGamepadActionMapper::actionTriggered, this, &GamepadKeyNavigation::onActionTriggered);

    // focus/IME 状态变化可能影响门控：变化时释放已按下键，避免“卡键”。
    if (auto *app = qobject_cast<QGuiApplication *>(QCoreApplication::instance())) {
        connect(app, &QGuiApplication::focusObjectChanged, this, [this]() {
            QString reason;
            if (shouldSuppress(resolveTarget(), &reason)) {
                updateSuppressionReason(reason);
                releaseAll();
            } else {
                updateSuppressionReason(QString{});
            }
        });
        connect(app, &QGuiApplication::focusWindowChanged, this, [this]() {
            QString reason;
            if (shouldSuppress(resolveTarget(), &reason)) {
                updateSuppressionReason(reason);
                releaseAll();
            } else {
                updateSuppressionReason(QString{});
            }
        });
    }
}

GamepadKeyNavigation::~GamepadKeyNavigation() = default;

void GamepadKeyNavigation::classBegin()
{
}

void GamepadKeyNavigation::componentComplete()
{
    updateSubscriptions();
}

bool GamepadKeyNavigation::active() const
{
    return m_active;
}

void GamepadKeyNavigation::setActive(bool active)
{
    if (m_active == active) {
        return;
    }
    m_active = active;
    updateSubscriptions();
    Q_EMIT activeChanged();
}

Gamepad *GamepadKeyNavigation::gamepad() const
{
    return m_gamepad;
}

void GamepadKeyNavigation::setGamepad(Gamepad *gamepad)
{
    if (m_gamepad == gamepad) {
        return;
    }
    releaseAll();
    m_gamepad = gamepad;
    updateSubscriptions();
    Q_EMIT gamepadChanged();
}

GamepadActionRouter *GamepadKeyNavigation::actionRouter() const
{
    return m_actionRouter;
}

void GamepadKeyNavigation::setActionRouter(GamepadActionRouter *router)
{
    if (m_actionRouter == router) {
        return;
    }
    releaseAll();
    m_actionRouter = router;
    updateSubscriptions();
    Q_EMIT actionRouterChanged();
}

AbstractGamepadActionSource *GamepadKeyNavigation::actionSource() const
{
    return m_actionSource;
}

void GamepadKeyNavigation::setActionSource(AbstractGamepadActionSource *source)
{
    if (m_actionSource == source) {
        return;
    }
    releaseAll();
    m_actionSource = source;
    updateSubscriptions();
    Q_EMIT actionSourceChanged();
}

bool GamepadKeyNavigation::useLegacyMapper() const
{
    return m_useLegacyMapper;
}

void GamepadKeyNavigation::setUseLegacyMapper(bool enabled)
{
    if (m_useLegacyMapper == enabled) {
        return;
    }
    releaseAll();
    m_useLegacyMapper = enabled;
    updateSubscriptions();
    Q_EMIT useLegacyMapperChanged();
}

QObject *GamepadKeyNavigation::target() const
{
    return m_target.data();
}

void GamepadKeyNavigation::setTarget(QObject *target)
{
    if (m_target.data() == target) {
        return;
    }
    releaseAll();
    m_target = target;
    updateSubscriptions();
    Q_EMIT targetChanged();
}

QString GamepadKeyNavigation::suppressionReason() const
{
    return m_suppressionReason;
}

quint64 GamepadKeyNavigation::keyCombo(int qtKey, int modifiers)
{
    return (static_cast<quint64>(static_cast<uint32_t>(modifiers)) << 32)
        | static_cast<quint64>(static_cast<uint32_t>(qtKey));
}

void GamepadKeyNavigation::onActionTriggered(const QString &actionId, bool pressed, bool repeated)
{
    handleAction(actionId, pressed, repeated);
}

void GamepadKeyNavigation::updateSubscriptions()
{
    for (const auto &c : m_connections) {
        disconnect(c);
    }
    m_connections.clear();

    if (!m_active) {
        m_mapper.setEnabled(false);
        updateSuppressionReason(QString{});
        releaseAll();
        return;
    }

    auto resolveManager = [this]() -> GamepadManager * {
        auto *engine = qmlEngine(this);
        if (!engine) {
            // QML 引擎尚未关联：避免抢先创建全局单例，防止错过 _deckGamepadService 注入并产生“双实例”。
            return nullptr;
        }
        if (auto *mgr = engine->singletonInstance<GamepadManager *>(QStringLiteral("DeckShell.DeckGamepad"),
                                                                    QStringLiteral("GamepadManager"))) {
            return mgr;
        }
        return GamepadManager::create(engine, nullptr);
    };

    AbstractGamepadActionSource *source = m_actionSource ? m_actionSource : m_actionRouter;

    // 优先消费外部 action 源（ServiceActionRouter / GamepadActionRouter 等）。
    if (source) {
        m_mapper.setEnabled(false);
        updateSuppressionReason(QString{});

        if (m_gamepad) {
            m_connections.append(connect(m_gamepad, &QObject::destroyed, this, [this]() {
                releaseAll();
                m_gamepad = nullptr;
            }));

            m_connections.append(connect(m_gamepad, &Gamepad::deviceIdChanged, this, [this]() {
                releaseAll();
            }));

            m_connections.append(connect(m_gamepad, &Gamepad::connectedChanged, this, [this]() {
                if (m_gamepad && !m_gamepad->connected()) {
                    releaseAll();
                }
            }));
        }

        AbstractGamepadActionSource *destroyedSource = source;
        m_connections.append(connect(source, &QObject::destroyed, this, [this, destroyedSource]() {
            releaseAll();
            if (m_actionSource == destroyedSource) {
                m_actionSource = nullptr;
            }
            if (m_actionRouter == destroyedSource) {
                m_actionRouter = nullptr;
            }
            updateSubscriptions();
        }));

        m_connections.append(connect(source,
                                     &AbstractGamepadActionSource::actionTriggered,
                                     this,
                                     &GamepadKeyNavigation::onActionTriggered));

        // backend 切换时清理按键状态，避免残留。
        if (auto *mgr = resolveManager()) {
            m_connections.append(connect(mgr,
                                         &GamepadManager::activeBackendChanged,
                                         this,
                                         [this]() { releaseAll(); }));
        }
        return;
    }

    if (!m_gamepad) {
        m_mapper.setEnabled(false);
        updateSuppressionReason(QStringLiteral("noGamepad"));
        releaseAll();
        return;
    }

    m_connections.append(connect(m_gamepad, &QObject::destroyed, this, [this]() {
        releaseAll();
        m_gamepad = nullptr;
        updateSubscriptions();
    }));

    m_connections.append(connect(m_gamepad, &Gamepad::deviceIdChanged, this, [this]() {
        releaseAll();
    }));

    m_connections.append(connect(m_gamepad, &Gamepad::connectedChanged, this, [this]() {
        if (m_gamepad && !m_gamepad->connected()) {
            releaseAll();
        }
    }));

    // 默认走 Service action（actionId SSOT），仅在需要时通过开关回退到 QML 内置 mapper。
    if (!m_useLegacyMapper) {
        m_mapper.setEnabled(false);

        auto *mgr = resolveManager();
        auto *svc = mgr ? mgr->service() : nullptr;
        if (!svc) {
            updateSuppressionReason(QStringLiteral("noService"));
            releaseAll();
            return;
        }

        updateSuppressionReason(QString{});

        m_connections.append(connect(svc, &QObject::destroyed, this, [this]() {
            releaseAll();
            updateSubscriptions();
        }));

        m_connections.append(connect(svc,
                                     &deckshell::deckgamepad::DeckGamepadService::actionTriggered,
                                     this,
                                     [this](int deviceId, const QString &actionId, bool pressed, bool repeated) {
                                         if (!m_active || !m_gamepad) {
                                             return;
                                         }
                                         if (deviceId != m_gamepad->deviceId()) {
                                             return;
                                         }
                                         onActionTriggered(actionId, pressed, repeated);
                                     }));

        if (mgr) {
            m_connections.append(connect(mgr, &GamepadManager::activeBackendChanged, this, [this]() {
                releaseAll();
            }));
        }
        return;
    }

    m_mapper.setEnabled(true);
    updateSuppressionReason(QString{});

    m_connections.append(connect(m_gamepad, &Gamepad::buttonChanged, this, [this](int button, bool pressed) {
        if (!m_active) {
            return;
        }
        if (button < 0 || button >= deckshell::deckgamepad::GAMEPAD_BUTTON_MAX) {
            return;
        }
        m_mapper.processButton(static_cast<deckshell::deckgamepad::GamepadButton>(button), pressed);
    }));

    m_connections.append(connect(m_gamepad, &Gamepad::axisChanged, this, [this](int axis, double value) {
        if (!m_active) {
            return;
        }
        if (axis < 0 || axis >= deckshell::deckgamepad::GAMEPAD_AXIS_MAX) {
            return;
        }
        m_mapper.processAxis(static_cast<deckshell::deckgamepad::GamepadAxis>(axis), value);
    }));

    if (auto *mgr = resolveManager()) {
        m_connections.append(connect(mgr, &GamepadManager::activeBackendChanged, this, [this]() {
            releaseAll();
        }));
    }
}

void GamepadKeyNavigation::releaseAll()
{
    QObject *fallbackTarget = resolveTarget();

    for (auto it = m_pressedTargets.constBegin(); it != m_pressedTargets.constEnd(); ++it) {
        QObject *target = it.value() ? it.value().data() : fallbackTarget;
        if (!target) {
            continue;
        }

        const quint64 combo = it.key();
        const int qtKey = static_cast<int>(combo & 0xffffffffu);
        const int modifiers = static_cast<int>((combo >> 32) & 0xffffffffu);
        QKeyEvent event(QEvent::KeyRelease,
                        qtKey,
                        static_cast<Qt::KeyboardModifiers>(modifiers));
        QCoreApplication::sendEvent(target, &event);
    }

    m_pressedTargets.clear();
}

QObject *GamepadKeyNavigation::resolveTarget() const
{
    if (m_target) {
        return m_target.data();
    }

    if (auto *obj = QGuiApplication::focusObject()) {
        return obj;
    }
    return QGuiApplication::focusWindow();
}

static bool looksLikeTextInput(const QObject *obj)
{
    if (!obj) {
        return false;
    }
    const QByteArray cls = obj->metaObject() ? QByteArray(obj->metaObject()->className()) : QByteArray{};
    if (cls.contains("TextInput") || cls.contains("TextField") || cls.contains("TextArea")
        || cls.contains("LineEdit")) {
        return true;
    }
    // QML TextInput 等通常具备这些属性。
    if (obj->property("inputMethodComposing").isValid()) {
        return true;
    }
    if (obj->property("cursorPosition").isValid()) {
        return true;
    }
    return false;
}

bool GamepadKeyNavigation::shouldSuppress(QObject *resolvedTarget, QString *reason) const
{
    if (!resolvedTarget) {
        if (reason) {
            *reason = QStringLiteral("noTarget");
        }
        return true;
    }

    if (auto *win = QGuiApplication::focusWindow()) {
        if (!win->isActive()) {
            if (reason) {
                *reason = QStringLiteral("windowInactive");
            }
            return true;
        }
    }

    if (auto *im = QGuiApplication::inputMethod()) {
        if (im->isVisible()) {
            if (reason) {
                *reason = QStringLiteral("inputMethodVisible");
            }
            return true;
        }
    }

    if (looksLikeTextInput(QGuiApplication::focusObject())) {
        if (reason) {
            *reason = QStringLiteral("textInputFocused");
        }
        return true;
    }

    if (reason) {
        reason->clear();
    }
    return false;
}

void GamepadKeyNavigation::updateSuppressionReason(const QString &reason)
{
    if (m_suppressionReason == reason) {
        return;
    }
    m_suppressionReason = reason;
    Q_EMIT suppressionReasonChanged();
}

void GamepadKeyNavigation::handleAction(const QString &actionId, bool pressed, bool repeated)
{
    if (!m_active) {
        return;
    }

    const auto mapping = deckshell::deckgamepad::deckGamepadQtKeyMappingForActionId(actionId);
    if (!mapping.isValid()) {
        return;
    }

    QString reason;
    QObject *target = resolveTarget();
    if (shouldSuppress(target, &reason)) {
        updateSuppressionReason(reason);
        releaseAll();
        return;
    }
    updateSuppressionReason(QString{});

    const int qtKey = mapping.qtKey;
    const int modifiers = mapping.modifiers;
    const quint64 combo = keyCombo(qtKey, modifiers);
    if (pressed) {
        if (!m_pressedTargets.contains(combo)) {
            m_pressedTargets.insert(combo, target);
        }

        QKeyEvent event(QEvent::KeyPress,
                        qtKey,
                        static_cast<Qt::KeyboardModifiers>(modifiers),
                        QString{},
                        repeated);
        QCoreApplication::sendEvent(target, &event);
        return;
    }

    QObject *releaseTarget = nullptr;
    if (const auto it = m_pressedTargets.constFind(combo); it != m_pressedTargets.constEnd()) {
        releaseTarget = it.value();
    }
    if (!releaseTarget) {
        releaseTarget = target;
    }

    m_pressedTargets.remove(combo);

    if (!releaseTarget) {
        return;
    }

    QKeyEvent event(QEvent::KeyRelease,
                    qtKey,
                    static_cast<Qt::KeyboardModifiers>(modifiers));
    QCoreApplication::sendEvent(releaseTarget, &event);
}
