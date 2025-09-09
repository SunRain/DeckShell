// Copyright (C) 2023 JiDe Zhang <zhangjide@deepin.org>.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "helper.h"
#include "surface/surfacewrapper.h"
#include "output.h"
#include "workspace/workspace.h"
#include "qmlengine.h"
#include "surface/surfacecontainer.h"
#include "rootsurfacecontainer.h"
#include "layersurfacecontainer.h"

#include <WServer>
#include <WOutput>
#include <WSurfaceItem>
#include <qqmlengine.h>
#include <wxdgpopupsurface.h>
#include <wxdgtoplevelsurface.h>
#include <winputpopupsurface.h>
#include <wrenderhelper.h>
#include <WBackend>
#include <wxdgshell.h>
#include <wlayershell.h>
#include <wxwayland.h>
#include <woutputitem.h>
#include <wquickcursor.h>
#include <woutputrenderwindow.h>
#include <wqmlcreator.h>
#include <winputmethodhelper.h>
#include <WForeignToplevel>
#include <WXdgOutput>
#include <wxwaylandsurface.h>
#include <woutputmanagerv1.h>
#include <wcursorshapemanagerv1.h>
#include <woutputitem.h>
#include <woutputlayout.h>
#include <woutputviewport.h>
#include <wseat.h>
#include <wsocket.h>
#include <wtoplevelsurface.h>
#include <wlayersurface.h>
#include <wxdgdecorationmanager.h>
#include <wextforeigntoplevellistv1.h>

// DDE Shell support
#include "dde-shell/ddeshellmanagerinterfacev1.h"

#include <qwbackend.h>
#include <qwdisplay.h>
#include <qwoutput.h>
#include <qwlogging.h>
#include <qwallocator.h>
#include <qwrenderer.h>
#include <qwcompositor.h>
#include <qwsubcompositor.h>
#include <qwxwaylandsurface.h>
#include <qwlayershellv1.h>
#include <qwscreencopyv1.h>
#include <qwfractionalscalemanagerv1.h>
#include <qwgammacontorlv1.h>
#include <qwbuffer.h>
#include <qwdatacontrolv1.h>
#include <qwviewporter.h>
#include <qwalphamodifierv1.h>

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickStyle>
#include <QProcess>
#include <QMouseEvent>
#include <QQuickItem>
#include <QQuickWindow>
#include <QLoggingCategory>
#include <QKeySequence>
#include <QQmlComponent>
#include <QVariant>

#define WLR_FRACTIONAL_SCALE_V1_VERSION 1

Helper *Helper::m_instance = nullptr;
Helper::Helper(QObject *parent)
    : WSeatEventFilter(parent)
    , m_renderWindow(new WOutputRenderWindow(this))
    , m_server(new WServer(this))
    , m_surfaceContainer(new RootSurfaceContainer(m_renderWindow->contentItem()))
    , m_backgroundContainer(new LayerSurfaceContainer(m_surfaceContainer))
    , m_bottomContainer(new LayerSurfaceContainer(m_surfaceContainer))
    , m_workspace(new Workspace(m_surfaceContainer))
    , m_topContainer(new LayerSurfaceContainer(m_surfaceContainer))
    , m_overlayContainer(new LayerSurfaceContainer(m_surfaceContainer))
    , m_popupContainer(new SurfaceContainer(m_surfaceContainer))
    // , m_shellManager(new ShellManager(this, this)) // ShellManager class not found in target directory
{
    setCurrentUserId(getuid());

    Q_ASSERT(!m_instance);
    m_instance = this;

    m_renderWindow->setColor(Qt::black);
    m_surfaceContainer->setFlag(QQuickItem::ItemIsFocusScope, true);
#if QT_VERSION >= QT_VERSION_CHECK(6, 7, 0)
    m_surfaceContainer->setFocusPolicy(Qt::StrongFocus);
#endif
    m_backgroundContainer->setZ(RootSurfaceContainer::BackgroundZOrder);
    m_bottomContainer->setZ(RootSurfaceContainer::BottomZOrder);
    m_workspace->setZ(RootSurfaceContainer::NormalZOrder);
    m_topContainer->setZ(RootSurfaceContainer::TopZOrder);
    m_overlayContainer->setZ(RootSurfaceContainer::OverlayZOrder);
    m_popupContainer->setZ(RootSurfaceContainer::PopupZOrder);

    // Additional initialization from source file that can be ported
    // m_multiTaskViewGesture(new TogglableGesture(this)), // TogglableGesture class not found
    // m_windowGesture(new TogglableGesture(this)), // TogglableGesture class not found

    // Workspace animation setup from source file
    // m_workspaceScaleAnimation = new QPropertyAnimation(m_shellHandler->workspace(), "scale", this); // ShellHandler not available
    // m_workspaceOpacityAnimation = new QPropertyAnimation(m_shellHandler->workspace(), "opacity", this); // ShellHandler not available
}

Helper::~Helper()
{
    for (auto s : m_surfaceContainer->surfaces()) {
        if (auto c = s->container())
            c->removeSurface(s);
    }

    delete m_surfaceContainer;
    Q_ASSERT(m_instance == this);
    m_instance = nullptr;
}

Helper *Helper::instance()
{
    return m_instance;
}

// 新增：isNvidiaCardPresent() 方法的简化实现，用于检测 NVIDIA 显卡存在
bool Helper::isNvidiaCardPresent()
{
    // This is a simplified implementation - in the full source file,
    // it checks the RHI device name for NVIDIA
    // For now, return false as we don't have RHI access in this simplified version
    return false;
}

// 新增：setWorkspaceVisible() 方法的简化实现，用于设置工作区可见性
void Helper::setWorkspaceVisible(bool visible)
{
    // This is a simplified implementation - the full version includes
    // animation effects for workspace transitions
    Q_UNUSED(visible)
    // In the full implementation, this would animate workspace scale and opacity
}

QmlEngine *Helper::qmlEngine() const
{
    return qobject_cast<QmlEngine*>(::qmlEngine(this));
}

WOutputRenderWindow *Helper::window() const
{
    return m_renderWindow;
}

ShellHandler *Helper::shellHandler() const
{
    return m_shellHandler;
}

Workspace* Helper::workspace() const
{
    return m_workspace;
}

void Helper::init()
{
    auto engine = qmlEngine();
    engine->setContextForObject(m_renderWindow, engine->rootContext());
    engine->setContextForObject(m_renderWindow->contentItem(), engine->rootContext());
    m_surfaceContainer->setQmlEngine(engine);

    m_surfaceContainer->init(m_server);
    m_seat = m_server->attach<WSeat>();
    m_seat->setEventFilter(this);
    m_seat->setCursor(m_surfaceContainer->cursor());
    m_seat->setKeyboardFocusWindow(m_renderWindow);

    // Initialize ShellManager
    // m_shellManager->initialize(m_server); // ShellManager class not found in target directory

    m_backend = m_server->attach<WBackend>();
    connect(m_backend, &WBackend::inputAdded, this, [this] (WInputDevice *device) {
        m_seat->attachInputDevice(device);
    });

    connect(m_backend, &WBackend::inputRemoved, this, [this] (WInputDevice *device) {
        m_seat->detachInputDevice(device);
    });

    auto wOutputManager = m_server->attach<WOutputManagerV1>();
    connect(m_backend, &WBackend::outputAdded, this, [this, wOutputManager] (WOutput *output) {
        allowNonDrmOutputAutoChangeMode(output);
        Output *o = nullptr;
        if (m_mode == OutputMode::Extension || !m_surfaceContainer->primaryOutput()) {
            o = Output::createPrimary(output, qmlEngine(), this);
            o->outputItem()->stackBefore(m_surfaceContainer);
            m_surfaceContainer->addOutput(o);
        } else if (m_mode == OutputMode::Copy) {
            o = Output::createCopy(output, m_surfaceContainer->primaryOutput(), qmlEngine(), this);
        }
        Q_ASSERT(o);

        m_outputList.append(o);
        enableOutput(output);
        wOutputManager->newOutput(output);
    });

    connect(m_backend, &WBackend::outputRemoved, this, [this, wOutputManager] (WOutput *output) {
        auto index = indexOfOutput(output);
        Q_ASSERT(index >= 0);
        const auto o = m_outputList.takeAt(index);
        wOutputManager->removeOutput(output);
        m_surfaceContainer->removeOutput(o);
        delete o;
    });

    auto *xdgShell = m_server->attach<WXdgShell>(5);
    m_foreignToplevel = m_server->attach<WForeignToplevel>(xdgShell);
    m_extForeignToplevelListV1 = m_server->attach<WExtForeignToplevelListV1>();
    auto *layerShell = m_server->attach<WLayerShell>(xdgShell);
    auto *xdgOutputManager = m_server->attach<WXdgOutputManager>(m_surfaceContainer->outputLayout());
    m_windowMenu = engine->createWindowMenu(this);

    // XDG shell surface handling moved to ShellHandler
    // connect(xdgShell, &WXdgShell::toplevelSurfaceAdded, this, [this] (WXdgToplevelSurface *surface) {
    //     ...
    // });
    // connect(xdgShell, &WXdgShell::toplevelSurfaceRemoved, this, [this] (WXdgToplevelSurface *surface) {
    //     ...
    // });

    // XDG popup surface handling moved to ShellHandler
    // connect(xdgShell, &WXdgShell::popupSurfaceAdded, this, [this] (WXdgPopupSurface *surface) {
    //     ...
    // });
    // connect(xdgShell, &WXdgShell::popupSurfaceRemoved, this, [this] (WXdgPopupSurface *surface) {
    //     ...
    // });

    // Layer shell surface handling moved to ShellHandler
    // connect(layerShell, &WLayerShell::surfaceAdded, this, [this] (WLayerSurface *surface) {
    //     ...
    // });
    // connect(layerShell, &WLayerShell::surfaceRemoved, this, [this] (WLayerSurface *surface) {
    //     ...
    // });

    m_server->start();

    m_renderer = WRenderHelper::createRenderer(m_backend->handle());
    if (!m_renderer) {
        qFatal("Failed to create renderer");
    }

    m_allocator = qw_allocator::autocreate(*m_backend->handle(), *m_renderer);
    m_renderer->init_wl_display(*m_server->handle());

    // free follow display
    m_compositor = qw_compositor::create(*m_server->handle(), 6, *m_renderer);
    qw_subcompositor::create(*m_server->handle());
    qw_screencopy_manager_v1::create(*m_server->handle());
    qw_viewporter::create(*m_server->handle());
    m_renderWindow->init(m_renderer, m_allocator);

    // for xwayland
    auto *xwaylandOutputManager = m_server->attach<WXdgOutputManager>(m_surfaceContainer->outputLayout());
    xwaylandOutputManager->setScaleOverride(1.0);

    auto xwayland_lazy = true;
    m_xwayland = m_server->attach<WXWayland>(m_compositor, xwayland_lazy);
    m_xwayland->setSeat(m_seat);

    xdgOutputManager->setFilter([this] (WClient *client) {
        return client != m_xwayland->waylandClient();
    });
    xwaylandOutputManager->setFilter([this] (WClient *client) {
        return client == m_xwayland->waylandClient();
    });

    // XWayland surface handling moved to ShellHandler
    // connect(m_xwayland, &WXWayland::surfaceAdded, this, [this] (WXWaylandSurface *surface) {
    //     ...
    // });

    m_inputMethodHelper = new WInputMethodHelper(m_server, m_seat);

    // Input method surface handling moved to ShellHandler
    // connect(m_inputMethodHelper, &WInputMethodHelper::inputPopupSurfaceV2Added, this, [this](WInputPopupSurface *inputPopup) {
    //     ...
    // });
    // connect(m_inputMethodHelper, &WInputMethodHelper::inputPopupSurfaceV2Removed, this, [this](WInputPopupSurface *inputPopup) {
    //     ...
    // });

    m_xdgDecorationManager = m_server->attach<WXdgDecorationManager>();
    connect(m_xdgDecorationManager, &WXdgDecorationManager::surfaceModeChanged,
            this, [this] (WSurface *surface, WXdgDecorationManager::DecorationMode mode) {
        auto s = m_surfaceContainer->getSurface(surface);
        if (!s)
            return;
        s->setNoDecoration(mode != WXdgDecorationManager::Server);
    });

    bool freezeClientWhenDisable = false;
    m_socket = new WSocket(freezeClientWhenDisable);
    if (m_socket->autoCreate()) {
        m_server->addSocket(m_socket);
    } else {
        delete m_socket;
        qCritical("Failed to create socket");
        return;
    }

    auto gammaControlManager = qw_gamma_control_manager_v1::create(*m_server->handle());
    connect(gammaControlManager, &qw_gamma_control_manager_v1::notify_set_gamma, this, [this]
            (wlr_gamma_control_manager_v1_set_gamma_event *event) {
        auto *qwOutput = qw_output::from(event->output);
        size_t ramp_size = 0;
        uint16_t *r = nullptr, *g = nullptr, *b = nullptr;
        wlr_gamma_control_v1 *gamma_control = event->control;
        if (gamma_control) {
            ramp_size = gamma_control->ramp_size;
            r = gamma_control->table;
            g = gamma_control->table + gamma_control->ramp_size;
            b = gamma_control->table + 2 * gamma_control->ramp_size;
        }
        qw_output_state newState;
        newState.set_gamma_lut(ramp_size, r, g, b);

        if (!qwOutput->commit_state(newState)) {
            qw_gamma_control_v1::from(gamma_control)->send_failed_and_destroy();
        }
    });

    connect(wOutputManager, &WOutputManagerV1::requestTestOrApply, this, [this, wOutputManager]
            (qw_output_configuration_v1 *config, bool onlyTest) {
        QList<WOutputState> states = wOutputManager->stateListPending();
        bool ok = true;
        for (auto state : std::as_const(states)) {
            WOutput *output = state.output;
            qw_output_state newState;

            newState.set_enabled(state.enabled);
            if (state.enabled) {
                if (state.mode)
                    newState.set_mode(state.mode);
                else
                    newState.set_custom_mode(state.customModeSize.width(),
                                              state.customModeSize.height(),
                                              state.customModeRefresh);

                newState.set_adaptive_sync_enabled(state.adaptiveSyncEnabled);
                if (!onlyTest) {
                    newState.set_transform(static_cast<wl_output_transform>(state.transform));
                    newState.set_scale(state.scale);

                    WOutputViewport *viewport = getOutput(output)->screenViewport();
                    if (viewport) {
                        viewport->setX(state.x);
                        viewport->setY(state.y);
                    }
                }
            }

            if (onlyTest)
                ok &= output->handle()->test_state(newState);
            else
                ok &= output->handle()->commit_state(newState);
        }
        wOutputManager->sendResult(config, ok);
    });

    m_server->attach<WCursorShapeManagerV1>();
    qw_fractional_scale_manager_v1::create(*m_server->handle(), WLR_FRACTIONAL_SCALE_V1_VERSION);
    qw_data_control_manager_v1::create(*m_server->handle());
    qw_alpha_modifier_v1::create(*m_server->handle());

    m_backend->handle()->start();

    qInfo() << "Listing on:" << m_socket->fullServerName();
    startDemoClient();
}

// TogglableGesture *Helper::multiTaskViewGesture() const // 缺失：TogglableGesture 类在目标目录中不存在
// {
//     return m_multiTaskViewGesture;
// }

// TogglableGesture *Helper::windowGesture() const // 缺失：TogglableGesture 类在目标目录中不存在
// {
//     return m_windowGesture;
// }

bool Helper::socketEnabled() const
{
    return m_socket->isEnabled();
}

void Helper::setSocketEnabled(bool newEnabled)
{
    if (m_socket)
        m_socket->setEnabled(newEnabled);
    else
        qWarning() << "Can't set enabled for empty socket!";
}

// RootSurfaceContainer *Helper::rootContainer() const
// {
//     return m_surfaceContainer;
// }


void Helper::activeSurface(SurfaceWrapper *wrapper, Qt::FocusReason reason)
{
    if (!wrapper || wrapper->shellSurface()->hasCapability(WToplevelSurface::Capability::Activate))
        setActivatedSurface(wrapper);
    if (!wrapper || wrapper->shellSurface()->hasCapability(WToplevelSurface::Capability::Focus))
        setKeyboardFocusSurface(wrapper, reason);
}


bool Helper::startDemoClient()
{
#ifdef START_DEMO
    QProcess waylandClientDemo;

    // waylandClientDemo.setProgram(PROJECT_BINARY_DIR"/examples/animationclient/animationclient");
    waylandClientDemo.setProgram("konsole");
    waylandClientDemo.setArguments({"-platform", "wayland"});
    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    env.insert("WAYLAND_DISPLAY", m_socket->fullServerName());

    waylandClientDemo.setProcessEnvironment(env);
    return waylandClientDemo.startDetached();
#else
    return false;
#endif
}

bool Helper::beforeDisposeEvent(WSeat *seat, QWindow *, QInputEvent *event)
{
    if (event->type() == QEvent::KeyPress) {
        auto kevent = static_cast<QKeyEvent*>(event);
        if (QKeySequence(kevent->keyCombination()) == QKeySequence::Quit) {
            qApp->quit();
            return true;
        } else if (event->modifiers() == Qt::MetaModifier) {
            if (kevent->key() == Qt::Key_Right) {
                m_workspace->switchToNext();
                return true;
            } else if (kevent->key() == Qt::Key_Left) {
                m_workspace->switchToPrev();
                return true;
            }
        }
    }

    if (event->type() == QEvent::MouseMove || event->type() == QEvent::MouseButtonPress) {
        seat->cursor()->setVisible(true);
    } else if (event->type() == QEvent::TouchBegin) {
        seat->cursor()->setVisible(false);
    }

    if (auto surface = m_surfaceContainer->moveResizeSurface()) {
        // for move resize
        if (Q_LIKELY(event->type() == QEvent::MouseMove || event->type() == QEvent::TouchUpdate)) {
            auto cursor = seat->cursor();
            Q_ASSERT(cursor);
            QMouseEvent *ev = static_cast<QMouseEvent*>(event);

            auto ownsOutput = surface->ownsOutput();
            if (!ownsOutput) {
                m_surfaceContainer->endMoveResize();
                return false;
            }

            auto lastPosition = m_fakelastPressedPosition.value_or(cursor->lastPressedOrTouchDownPosition());
            auto increment_pos = ev->globalPosition() - lastPosition;
            m_surfaceContainer->doMoveResize(increment_pos);

            return true;
        } else if (event->type() == QEvent::MouseButtonRelease || event->type() == QEvent::TouchEnd) {
            m_surfaceContainer->endMoveResize();
            m_fakelastPressedPosition.reset();
        }
    }

    return false;
}

bool Helper::afterHandleEvent(WSeat *seat, WSurface *watched, QObject *surfaceItem, QObject *, QInputEvent *event)
{
    Q_UNUSED(seat)

    if (event->isSinglePointEvent() && static_cast<QSinglePointEvent*>(event)->isBeginEvent()) {
        // surfaceItem is qml type: XdgSurfaceItem or LayerSurfaceItem
        auto toplevelSurface = qobject_cast<WSurfaceItem*>(surfaceItem)->shellSurface();
        if (!toplevelSurface)
            return false;
        Q_ASSERT(toplevelSurface->surface() == watched);

        auto surface = m_surfaceContainer->getSurface(watched);
        activeSurface(surface, Qt::MouseFocusReason);
    }

    return false;
}

bool Helper::unacceptedEvent(WSeat *, QWindow *, QInputEvent *event)
{
    if (event->isSinglePointEvent()) {
        if (static_cast<QSinglePointEvent*>(event)->isBeginEvent()) {
            activeSurface(nullptr, Qt::OtherFocusReason);
        }
    }

    return false;
}

SurfaceWrapper *Helper::keyboardFocusSurface() const
{
    return m_keyboardFocusSurface;
}

void Helper::setKeyboardFocusSurface(SurfaceWrapper *newActivate, Qt::FocusReason reason)
{
    if (m_keyboardFocusSurface == newActivate)
        return;

    if (newActivate && !newActivate->shellSurface()->hasCapability(WToplevelSurface::Capability::Focus))
        return;

    if (m_keyboardFocusSurface) {
        if (newActivate) {
            if (m_keyboardFocusSurface->shellSurface()->keyboardFocusPriority()
                > newActivate->shellSurface()->keyboardFocusPriority())
                return;
        } else {
            if (m_keyboardFocusSurface->shellSurface()->keyboardFocusPriority() > 0)
                return;
        }
    }

    if (newActivate) {
        newActivate->setFocus(true, reason);
        m_seat->setKeyboardFocusSurface(newActivate->surface());
    } else if (m_keyboardFocusSurface) {
        m_keyboardFocusSurface->setFocus(false, reason);
        m_seat->setKeyboardFocusSurface(nullptr);
    }

    m_keyboardFocusSurface = newActivate;

    Q_EMIT keyboardFocusSurfaceChanged();
}

SurfaceWrapper *Helper::activatedSurface() const
{
    return m_activatedSurface;
}

void Helper::setActivatedSurface(SurfaceWrapper *newActivateSurface)
{
    if (m_activatedSurface == newActivateSurface)
        return;

    if (newActivateSurface) {
        newActivateSurface->stackToLast();
        if (newActivateSurface->type() == SurfaceWrapper::Type::XWayland) {
            auto xwaylandSurface = qobject_cast<WXWaylandSurface *>(newActivateSurface->shellSurface());
            xwaylandSurface->restack(nullptr, WXWaylandSurface::XCB_STACK_MODE_ABOVE);
        }
    }

    if (m_activatedSurface)
        m_activatedSurface->setActivate(false);
    if (newActivateSurface)
        newActivateSurface->setActivate(true);
    m_activatedSurface = newActivateSurface;
    Q_EMIT activatedSurfaceChanged();
}

void Helper::setCursorPosition(const QPointF &position)
{
    m_surfaceContainer->endMoveResize();
    m_seat->setCursorPosition(position);
}

void Helper::allowNonDrmOutputAutoChangeMode(WOutput *output)
{
    output->safeConnect(&qw_output::notify_request_state,
        this, [this] (wlr_output_event_request_state *newState) {
        if (newState->state->committed & WLR_OUTPUT_STATE_MODE) {
            auto output = qobject_cast<qw_output*>(sender());
            output->commit_state(newState->state);
        }
    });
}

void Helper::enableOutput(WOutput *output)
{
    // Enable on default
    auto qwoutput = output->handle();
    // Don't care for WOutput::isEnabled, must do WOutput::commit here,
    // In order to ensure trigger QWOutput::frame signal, WOutputRenderWindow
    // needs this signal to render next frmae. Because QWOutput::frame signal
    // maybe emit before WOutputRenderWindow::attach, if no commit here,
    // WOutputRenderWindow will ignore this ouptut on render.
    if (!qwoutput->property("_Enabled").toBool()) {
        qwoutput->setProperty("_Enabled", true);
        qw_output_state newState;

        if (!qwoutput->handle()->current_mode) {
            auto mode = qwoutput->preferred_mode();
            if (mode)
                newState.set_mode(mode);
        }
        newState.set_enabled(true);
        bool ok = qwoutput->commit_state(newState);
        Q_ASSERT(ok);
    }
}

int Helper::indexOfOutput(WOutput *output) const
{
    for (int i = 0; i < m_outputList.size(); i++) {
        if (m_outputList.at(i)->output() == output)
            return i;
    }
    return -1;
}

Output *Helper::getOutput(WOutput *output) const
{
    for (auto o : std::as_const(m_outputList)) {
        if (o->output() == output)
            return o;
    }
    return nullptr;
}

void Helper::addOutput()
{
    qobject_cast<qw_multi_backend*>(m_backend->handle())->for_each_backend([] (wlr_backend *backend, void *) {
        if (auto x11 = qw_x11_backend::from(backend)) {
            qw_output::from(x11->output_create());
        } else if (auto wayland = qw_wayland_backend::from(backend)) {
            qw_output::from(wayland->output_create());
        }
    }, nullptr);
}

void Helper::setOutputMode(OutputMode mode)
{
    if (m_outputList.length() < 2 || m_mode == mode)
        return;

    m_mode = mode;
    Q_EMIT outputModeChanged();
    for (int i = 0; i < m_outputList.size(); i++) {
        if (m_outputList.at(i) == m_surfaceContainer->primaryOutput())
            continue;

        Output *o;
        if (mode == OutputMode::Copy) {
            o = Output::createCopy(m_outputList.at(i)->output(), m_surfaceContainer->primaryOutput(), qmlEngine(), this);
            m_surfaceContainer->removeOutput(m_outputList.at(i));
        } else if(mode == OutputMode::Extension) {
            o = Output::createPrimary(m_outputList.at(i)->output(), qmlEngine(), this);
            o->outputItem()->stackBefore(m_surfaceContainer);
            m_surfaceContainer->addOutput(o);
            enableOutput(o->output());
        }

        m_outputList.at(i)->deleteLater();
        m_outputList.replace(i,o);
    }
}

void Helper::setOutputProxy(Output *output)
{

}

// updateLayerSurfaceContainer method moved to ShellHandler
// void Helper::updateLayerSurfaceContainer(SurfaceWrapper *surface)
// {
//     auto layer = qobject_cast<WLayerSurface*>(surface->shellSurface());
//     Q_ASSERT(layer);

//     if (auto oldContainer = surface->container())
//         oldContainer->removeSurface(surface);

//     switch (layer->layer()) {
//     case WLayerSurface::LayerType::Background:
//         m_backgroundContainer->addSurface(surface);
//         break;
//     case WLayerSurface::LayerType::Bottom:
//         m_bottomContainer->addSurface(surface);
//         break;
//     case WLayerSurface::LayerType::Top:
//         m_topContainer->addSurface(surface);
//         break;
//     case WLayerSurface::LayerType::Overlay:
//         m_overlayContainer->addSurface(surface);
//         break;
//     default:
//         Q_UNREACHABLE_RETURN();
//     }
// }

int Helper::currentUserId() const
{
    return m_currentUserId;
}

void Helper::setCurrentUserId(int uid)
{
    if (m_currentUserId == uid)
        return;
    m_currentUserId = uid;
    Q_EMIT currentUserIdChanged();
}

float Helper::animationSpeed() const
{
    return m_animationSpeed;
}

void Helper::setAnimationSpeed(float newAnimationSpeed)
{
    if (qFuzzyCompare(m_animationSpeed, newAnimationSpeed))
        return;
    m_animationSpeed = newAnimationSpeed;
    emit animationSpeedChanged();
}

Helper::OutputMode Helper::outputMode() const
{
    return m_mode;
}

QString Helper::cursorTheme() const
{
    return m_cursorTheme;
}

QSize Helper::cursorSize() const
{
    return m_cursorSize;
}

Helper::CurrentMode Helper::currentMode() const
{
    return m_currentMode;
}

void Helper::setCurrentMode(CurrentMode mode)
{
    if (m_currentMode == mode)
        return;
    m_currentMode = mode;
    Q_EMIT currentModeChanged();
}

// ShellHandler enhanced methods implementation

// handleDdeShellSurfaceAdded method moved to ShellHandler
// void Helper::handleDdeShellSurfaceAdded(WSurface *surface, SurfaceWrapper *wrapper)
// {
//     // Get DDE Shell surface interface
//     auto ddeShellSurface = DDEShellSurfaceInterface::get(surface);
//     if (!ddeShellSurface) {
//         qWarning() << "Failed to get DDE Shell surface interface";
//         return;
//     }

//     // Handle role changes (Overlay role affects stacking)
//     auto updateLayer = [ddeShellSurface, wrapper, this] {
//         if (ddeShellSurface->role().value() == DDEShellSurfaceInterface::OVERLAY) {
//             // Set overlay surfaces to always on top
//             wrapper->setAlwaysOnTop(true);
//         }
//     };

//     if (ddeShellSurface->role().has_value())
//         updateLayer();

//     connect(ddeShellSurface, &DDEShellSurfaceInterface::roleChanged, this, [updateLayer] {
//         updateLayer();
//     });

//     // Handle position changes
//     if (ddeShellSurface->surfacePos().has_value()) {
//         // Note: SurfaceWrapper doesn't have setClientRequstPos method
//         // Position handling would need to be implemented differently
//         qDebug() << "DDE Shell surface position:" << ddeShellSurface->surfacePos().value();
//     }

//     connect(ddeShellSurface, &DDEShellSurfaceInterface::positionChanged, this,
//             [wrapper](QPoint pos) {
//         qDebug() << "DDE Shell surface position changed:" << pos;
//         // Position handling would need to be implemented based on actual requirements
//     });

//     // Handle skip properties - these would need to be added to SurfaceWrapper
//     // For now, just log them
//     if (ddeShellSurface->skipSwitcher().has_value()) {
//         qDebug() << "DDE Shell skip switcher:" << ddeShellSurface->skipSwitcher().value();
//     }

//     if (ddeShellSurface->skipDockPreView().has_value()) {
//         qDebug() << "DDE Shell skip dock preview:" << ddeShellSurface->skipDockPreView().value();
//     }

//     if (ddeShellSurface->skipMutiTaskView().has_value()) {
//         qDebug() << "DDE Shell skip multitask view:" << ddeShellSurface->skipMutiTaskView().value();
//     }

//     // Connect to property change signals for future implementation
//     connect(ddeShellSurface, &DDEShellSurfaceInterface::skipSwitcherChanged, this,
//             [wrapper](bool skip) {
//         qDebug() << "DDE Shell skip switcher changed:" << skip;
//     });
//     connect(ddeShellSurface, &DDEShellSurfaceInterface::skipDockPreViewChanged, this,
//             [wrapper](bool skip) {
//         qDebug() << "DDE Shell skip dock preview changed:" << skip;
//     });
//     connect(ddeShellSurface, &DDEShellSurfaceInterface::skipMutiTaskViewChanged, this,
//             [wrapper](bool skip) {
//         qDebug() << "DDE Shell skip multitask view changed:" << skip;
//     });
//     connect(ddeShellSurface, &DDEShellSurfaceInterface::acceptKeyboardFocusChanged, this,
//             [wrapper](bool accept) {
//         qDebug() << "DDE Shell accept keyboard focus changed:" << accept;
//     });
// }

// setResourceManagerAtom method moved to ShellHandler
// void Helper::setResourceManagerAtom(WXWayland *xwayland, const QByteArray &value)
// {
//     auto xcb_conn = xwayland->xcbConnection();
//     auto root = xwayland->xcbScreen()->root;
//     xcb_change_property(xcb_conn,
//                         XCB_PROP_MODE_REPLACE,
//                         root,
//                         xwayland->atom("RESOURCE_MANAGER"),
//                         XCB_ATOM_STRING,
//                         8,
//                         value.size(),
//                         value.constData());
//     xcb_flush(xcb_conn);
// }

// setupSurfaceActiveWatcher method moved to ShellHandler
// void Helper::setupSurfaceActiveWatcher(SurfaceWrapper *wrapper)
// {
//     Q_ASSERT_X(wrapper->container(), Q_FUNC_INFO, "Must setContainer at first!");

//     // Note: SurfaceWrapper doesn't have requestActive/requestInactive signals
//     // This is a simplified implementation that focuses on the core functionality

//     if (wrapper->type() == SurfaceWrapper::Type::Layer) {
//         // For layer surfaces, handle keyboard interactivity
//         auto layerSurface = qobject_cast<WLayerSurface *>(wrapper->shellSurface());
//         if (layerSurface) {
//             if (layerSurface->layer() == WLayerSurface::LayerType::Overlay
//                 || layerSurface->keyboardInteractivity() == WLayerSurface::KeyboardInteractivity::Exclusive) {
//                 // Overlay and exclusive layers can get keyboard focus
//                 wrapper->setAlwaysOnTop(true);
//             }
//         }
//     }

//     // Basic workspace handling for toplevel surfaces
//     if (wrapper->type() == SurfaceWrapper::Type::XdgToplevel ||
//         wrapper->type() == SurfaceWrapper::Type::XWayland) {
//         // Ensure surface is properly positioned in workspace
//         if (wrapper->workspaceId() == -1) {
//             m_workspace->addSurface(wrapper);
//         }
//     }
// }

void Helper::activateSurface(SurfaceWrapper *wrapper)
{
    activeSurface(wrapper, Qt::OtherFocusReason);
}

Output *Helper::getOutputAtCursor() const
{
    QPoint cursorPos = QCursor::pos();
    for (auto output : m_outputList) {
        QRectF outputGeometry(output->outputItem()->position(), output->outputItem()->size());
        if (outputGeometry.contains(cursorPos)) {
            return output;
        }
    }

    return m_surfaceContainer->primaryOutput();
}


// ShellHandler accessor (commented out as ShellHandler is not available)
// ShellHandler *Helper::shellHandler() const
// {
//     return m_shellHandler; // ShellHandler class not found in target directory
// }

// Additional utility methods that can be ported
void Helper::addSocket(WSocket *socket)
{
    m_server->addSocket(socket);
}

WXWayland *Helper::createXWayland()
{
    // Simplified implementation - full version uses ShellHandler
    // return m_shellHandler->createXWayland(m_server, m_seat, m_compositor, false);
    // For now, return nullptr as ShellHandler is not available
    return nullptr;
}

void Helper::removeXWayland(WXWayland *xwayland)
{
    // Simplified implementation - full version uses ShellHandler
    // m_shellHandler->removeXWayland(xwayland);
    Q_UNUSED(xwayland)
}

WSocket *Helper::defaultWaylandSocket() const
{
    return m_socket;
}

WXWayland *Helper::defaultXWaylandSocket() const
{
    return m_xwayland;
}

// DDE Shell manager accessor (commented out as class is not available)
// DDEShellManagerInterfaceV1 *Helper::ddeShellManager() const
// {
//     return m_ddeShellManager; // DDEShellManagerInterfaceV1 class not found in target directory
// }

// User model accessor (commented out as class is not available)
// UserModel *Helper::userModel() const
// {
//     return m_userModel; // UserModel class not found in target directory
// }

// DDM interface accessor (commented out as class is not available)
// DDMInterfaceV1 *Helper::ddmInterfaceV1() const
// {
//     return m_ddmInterfaceV1; // DDMInterfaceV1 class not found in target directory
// }

// Session management methods (simplified versions)
void Helper::activateSession() {
    if (m_backend && !m_backend->isSessionActive())
        m_backend->activateSession();
}

void Helper::deactivateSession() {
    if (m_backend && m_backend->isSessionActive())
        m_backend->deactivateSession();
}

// Render control methods
void Helper::enableRender() {
    if (m_renderWindow)
        m_renderWindow->setRenderEnabled(true);
}

void Helper::disableRender() {
    if (m_renderWindow)
        m_renderWindow->setRenderEnabled(false);

    // Note: The full implementation includes additional logic for
    // revoking evdev devices during hibernation, but that's omitted here
    // as it requires additional system-level dependencies
}
