#include "window.h"

#include <QApplication>
#include <QDebug>
#include <QMainWindow>
#include <QPointer>
#include <QTimer>

#include <QtWaylandClient/private/qwaylandwindow_p.h>
#include <QtGui/qpa/qplatformwindow.h>

#include "shellsurface.h"
#include "waylandmanager.h"

#include <memory>

// Static member initialization
std::unique_ptr<WaylandManager> Window::s_waylandManager = nullptr;
QHash<QWindow *, Window *> Window::s_windows;

Window *Window::get(QWindow *window)
{
    if (!window) {
        qWarning() << QStringLiteral("Window::get: window is null");
        return nullptr;
    }

    // Check if Window object already exists for this QWindow
    auto it = s_windows.value(window);
    if (it) {
        return it;
    }

    // Create new Window object with QWindow as parent (Qt parent-child memory management)
    return new Window(window);
}

Window *Window::get(QMainWindow *mainWindow)
{
    if (!mainWindow) {
        qWarning() << QStringLiteral("Window::get: MainWindow is null");
        return nullptr;
    }

    QWindow *qwindow = mainWindow->windowHandle();
    if (qwindow) {
        // windowHandle already available, use normal path
        return get(qwindow);
    }

    // windowHandle not ready, create Window and monitor for it
    qDebug() << QStringLiteral("WindowHandle not available yet, creating Window with deferred initialization");

    auto newWindow = new Window(nullptr, mainWindow);
    newWindow->m_mainWindow = mainWindow;
    newWindow->m_initState = InitState::WaitingForWindowHandle;

    // Install event filter to monitor QEvent::WinIdChange
    mainWindow->installEventFilter(newWindow);

    // Start polling as backup (in case event is missed)
    newWindow->startWindowHandlePolling();

    return newWindow;
}

// QML Attached Properties interface
Window *Window::qmlAttachedProperties(QObject *object)
{
    // Try to cast to QWindow directly (works for QWindow and QQuickWindow)
    if (auto *window = qobject_cast<QWindow *>(object)) {
        qDebug() << "qmlAttachedProperties: Got QWindow" << window;
        return get(window);
    }

    qWarning() << "qmlAttachedProperties: object is not a QWindow" << object;
    return nullptr;
}

Window::Window(QWindow *window, QObject *parent)
    : QObject(window ? window : parent)  // Use window as parent for automatic cleanup
    , m_qwindow(window)
    , m_pendingSkipMultitaskview(false)
    , m_hasPendingSkipMultitaskview(false)
    , m_initState(InitState::WaitingForWindowHandle)
{
    if (window) {
        s_windows.insert(window, this);
        scheduleInitialization();
    }
}

Window::Window(QWindow *window, QMainWindow *mainWindow, QObject *parent)
    : QObject(mainWindow ? mainWindow : parent)  // Use mainWindow as parent
    , m_qwindow(window)
    , m_mainWindow(mainWindow)
    , m_pendingSkipMultitaskview(false)
    , m_hasPendingSkipMultitaskview(false)
    , m_initState(InitState::WaitingForWindowHandle)
{
}

Window::~Window()
{
    if (!m_qwindow.isNull()) {
        s_windows.remove(m_qwindow);
    }
}

bool Window::eventFilter(QObject *watched, QEvent *event)
{
    // 只处理 MainWindow 的 WinIdChange 事件
    if (watched != m_mainWindow.data()) {
        return QObject::eventFilter(watched, event);
    }

    if (event->type() == QEvent::WinIdChange) {
        qDebug() << QStringLiteral("Window detected WinIdChange event for MainWindow");

        if (auto *qwindow = m_mainWindow->windowHandle()) {
            handleWindowHandleReady(qwindow);

            // 移除事件过滤器（减少后续开销）
            m_mainWindow->removeEventFilter(this);
        }

        // 返回 false，不拦截事件（允许其他过滤器处理）
        return false;
    }

    return QObject::eventFilter(watched, event);
}

void Window::handleWindowHandleReady(QWindow *qwindow)
{
    qDebug() << QStringLiteral("WindowHandle ready:") << qwindow;

    m_qwindow = qwindow;

    // 加入静态缓存（避免重复创建）
    // 注意：无法获取当前对象的 QSharedPointer，由外部管理
    // 这里只是记录日志，实际缓存在 get() 中处理

    m_initState = InitState::WaitingForWaylandManager;

    // 继续初始化流程
    scheduleInitialization();
}

void Window::startWindowHandlePolling()
{
    if (m_windowHandlePollCount >= kMaxWindowHandlePollCount) {
        qWarning() << QStringLiteral("WindowHandle polling exceeded maximum attempts (")
                   << kMaxWindowHandlePollCount << QStringLiteral(")");
        m_initState = InitState::Failed;
        emit initializationFailed();
        return;
    }

    QTimer::singleShot(kWindowHandlePollInterval, this, [this]() {
        if (m_initState != InitState::WaitingForWindowHandle) {
            return;  // 已通过信号处理，停止轮询
        }

        if (m_mainWindow && m_mainWindow->windowHandle()) {
            handleWindowHandleReady(m_mainWindow->windowHandle());
        } else {
            ++m_windowHandlePollCount;
            qDebug() << QStringLiteral("WindowHandle polling attempt")
                     << m_windowHandlePollCount << QStringLiteral("of")
                     << kMaxWindowHandlePollCount;
            startWindowHandlePolling();  // 递归重试
        }
    });
}

void Window::scheduleInitialization()
{
    if (m_initState == InitState::Succeeded) {
        return;  // 已成功，无需重复初始化
    }

    // 步骤1：确保 WaylandManager 已初始化
    if (!ensureWaylandManagerInitialized()) {
        qDebug() << QStringLiteral("WaylandManager not initialized, retrying in")
                 << m_retryDelay << QStringLiteral("ms");
        m_initState = InitState::WaitingForWaylandManager;

        // 使用 QTimer 延迟重试
        QTimer::singleShot(m_retryDelay, this, [this]() {
            scheduleInitialization();  // 递归重试
        });
        return;
    }

    // 步骤2：检查协议是否就绪
    if (!s_waylandManager->isReady()) {
        qDebug() << QStringLiteral("Wayland protocol not ready, waiting for ready signal");
        m_initState = InitState::WaitingForProtocol;

        // 连接信号，协议就绪后自动初始化
        connect(s_waylandManager.get(), &WaylandManager::ready, this,
                &Window::tryInitialize, Qt::UniqueConnection);
        return;
    }

    // 步骤3：条件已满足，立即尝试初始化
    tryInitialize();
}

void Window::tryInitialize()
{
    if (m_initState == InitState::Succeeded) {
        return;  // 已成功，无需重试
    }

    m_initState = InitState::Initializing;

    if (initialize()) {
        // 初始化成功
        m_initState = InitState::Succeeded;
        m_retryCount = 0;  // 重置计数器

        qDebug() << QStringLiteral("Window initialization succeeded");

        // 执行排队的操作
        executeQueuedOperations();

        // 通知调用者
        emit initialized();

    } else {
        // 初始化失败，调度重试
        ++m_retryCount;

        if (m_retryCount >= kMaxRetryCount) {
            m_initState = InitState::Failed;
            qCritical() << QStringLiteral("Window initialization failed after")
                       << kMaxRetryCount << QStringLiteral("retries");
            emit initializationFailed();
            return;
        }

        m_initState = InitState::RetryPending;

        // 指数退避：100ms → 200ms → 400ms → ... → 最大 5s
        m_retryDelay = qMin(m_retryDelay * 2, kMaxRetryDelay);

        qDebug() << QStringLiteral("Retrying initialization in") << m_retryDelay
                 << QStringLiteral("ms (attempt") << (m_retryCount + 1)
                 << QStringLiteral("of") << kMaxRetryCount << QStringLiteral(")");

        QTimer::singleShot(m_retryDelay, this, &Window::tryInitialize);
    }
}

bool Window::initialize()
{
    qDebug() << Q_FUNC_INFO << QStringLiteral("Setting up DDE shell surface for window:")
             << m_qwindow.data();

    if (m_qwindow.isNull()) {
        qWarning() << QStringLiteral("Window::initialize: window is null");
        return false;
    }

    // Get the native wl_surface from the window
    // Use static_cast instead of dynamic_cast for platform-specific window types
    // This is safe because we're running on Wayland and handle() returns QWaylandWindow*
    auto *platformWindow = m_qwindow->handle();
    if (!platformWindow) {
        qDebug() << Q_FUNC_INFO << QStringLiteral("Failed to get platform window handle");
        return false;
    }

    auto *waylandWindow = static_cast<QtWaylandClient::QWaylandWindow *>(platformWindow);
    if (!waylandWindow) {
        qDebug() << Q_FUNC_INFO << QStringLiteral("Failed to get Wayland window");
        return false;
    }

    auto *surface = waylandWindow->surface();
    if (!surface) {
        qWarning() << QStringLiteral("Failed to get wl_surface");
        return false;
    }

    qDebug() << Q_FUNC_INFO << QStringLiteral("Got wl_surface:") << surface
             << QStringLiteral(", creating shell surface");

    // Create shell surface
    m_shellSurface.reset(s_waylandManager->createShellSurface(surface));
    if (!m_shellSurface) {
        qWarning() << QStringLiteral("Failed to create shell surface");
        return false;
    }

    qDebug() << Q_FUNC_INFO << QStringLiteral("Shell surface created successfully for surface:")
             << surface;
    return true;
}

void Window::setSkipMultitaskview(bool skip)
{
    if (m_skipMultitaskview == skip) {
        return;  // No change
    }

    m_skipMultitaskview = skip;
    emit skipMultitaskviewChanged();

    if (m_initState == InitState::Succeeded && m_shellSurface) {
        // Already initialized, apply immediately
        m_shellSurface->setSkipMultitaskview(skip);
        qDebug() << QStringLiteral("Successfully set skip multitaskview to") << skip;
    } else {
        // Not initialized, queue operation
        qDebug() << QStringLiteral("Queueing setSkipMultitaskview(") << skip
                 << QStringLiteral(") operation, will execute after initialization");

        m_pendingOperations.enqueue([this, skip]() {
            if (m_shellSurface) {
                m_shellSurface->setSkipMultitaskview(skip);
                qDebug() << QStringLiteral("Executed queued setSkipMultitaskview(") << skip
                         << QStringLiteral(")");
            }
        });
    }
}

void Window::setSurfacePosition(const QPoint &pos)
{
    if (m_initState == InitState::Succeeded && m_shellSurface) {
        m_shellSurface->setSurfacePosition(pos);
        qDebug() << QStringLiteral("Successfully set surface position to") << pos;
    } else {
        qDebug() << QStringLiteral("Queueing setSurfacePosition(") << pos
                 << QStringLiteral(") operation, will execute after initialization");

        m_pendingOperations.enqueue([this, pos]() {
            if (m_shellSurface) {
                m_shellSurface->setSurfacePosition(pos);
                qDebug() << QStringLiteral("Executed queued setSurfacePosition(") << pos
                         << QStringLiteral(")");
            }
        });
    }
}

void Window::setRole(ShellSurface::Role role)
{
    if (m_role == role) {
        return;  // No change
    }

    m_role = role;
    emit roleChanged();

    if (m_initState == InitState::Succeeded && m_shellSurface) {
        m_shellSurface->setRole(role);
        qDebug() << QStringLiteral("Successfully set role to")
                 << static_cast<uint32_t>(role);
    } else {
        qDebug() << QStringLiteral("Queueing setRole(")
                 << static_cast<uint32_t>(role)
                 << QStringLiteral(") operation, will execute after initialization");

        m_pendingOperations.enqueue([this, role]() {
            if (m_shellSurface) {
                m_shellSurface->setRole(role);
                qDebug() << QStringLiteral("Executed queued setRole(")
                         << static_cast<uint32_t>(role) << QStringLiteral(")");
            }
        });
    }
}

void Window::setAutoPlacement(uint32_t offset)
{
    if (m_initState == InitState::Succeeded && m_shellSurface) {
        m_shellSurface->setAutoPlacement(offset);
        qDebug() << QStringLiteral("Successfully set auto placement to") << offset;
    } else {
        qDebug() << QStringLiteral("Queueing setAutoPlacement(") << offset
                 << QStringLiteral(") operation, will execute after initialization");

        m_pendingOperations.enqueue([this, offset]() {
            if (m_shellSurface) {
                m_shellSurface->setAutoPlacement(offset);
                qDebug() << QStringLiteral("Executed queued setAutoPlacement(") << offset
                         << QStringLiteral(")");
            }
        });
    }
}

void Window::setSkipSwitcher(bool skip)
{
    if (m_skipSwitcher == skip) {
        return;  // No change
    }

    m_skipSwitcher = skip;
    emit skipSwitcherChanged();

    if (m_initState == InitState::Succeeded && m_shellSurface) {
        m_shellSurface->setSkipSwitcher(skip);
        qDebug() << QStringLiteral("Successfully set skip switcher to") << skip;
    } else {
        qDebug() << QStringLiteral("Queueing setSkipSwitcher(") << skip
                 << QStringLiteral(") operation, will execute after initialization");

        m_pendingOperations.enqueue([this, skip]() {
            if (m_shellSurface) {
                m_shellSurface->setSkipSwitcher(skip);
                qDebug() << QStringLiteral("Executed queued setSkipSwitcher(") << skip
                         << QStringLiteral(")");
            }
        });
    }
}

void Window::setSkipDockPreview(bool skip)
{
    if (m_skipDockPreview == skip) {
        return;  // No change
    }

    m_skipDockPreview = skip;
    emit skipDockPreviewChanged();

    if (m_initState == InitState::Succeeded && m_shellSurface) {
        m_shellSurface->setSkipDockPreview(skip);
        qDebug() << QStringLiteral("Successfully set skip dock preview to") << skip;
    } else {
        qDebug() << QStringLiteral("Queueing setSkipDockPreview(") << skip
                 << QStringLiteral(") operation, will execute after initialization");

        m_pendingOperations.enqueue([this, skip]() {
            if (m_shellSurface) {
                m_shellSurface->setSkipDockPreview(skip);
                qDebug() << QStringLiteral("Executed queued setSkipDockPreview(") << skip
                         << QStringLiteral(")");
            }
        });
    }
}

void Window::setAcceptKeyboardFocus(bool accept)
{
    if (m_acceptKeyboardFocus == accept) {
        return;  // No change
    }

    m_acceptKeyboardFocus = accept;
    emit acceptKeyboardFocusChanged();

    if (m_initState == InitState::Succeeded && m_shellSurface) {
        m_shellSurface->setAcceptKeyboardFocus(accept);
        qDebug() << QStringLiteral("Successfully set accept keyboard focus to") << accept;
    } else {
        qDebug() << QStringLiteral("Queueing setAcceptKeyboardFocus(") << accept
                 << QStringLiteral(") operation, will execute after initialization");

        m_pendingOperations.enqueue([this, accept]() {
            if (m_shellSurface) {
                m_shellSurface->setAcceptKeyboardFocus(accept);
                qDebug() << QStringLiteral("Executed queued setAcceptKeyboardFocus(") << accept
                         << QStringLiteral(")");
            }
        });
    }
}

void Window::executeQueuedOperations()
{
    if (m_pendingOperations.isEmpty()) {
        return;
    }

    qDebug() << QStringLiteral("Executing") << m_pendingOperations.size()
             << QStringLiteral("queued operations");

    while (!m_pendingOperations.isEmpty()) {
        auto operation = m_pendingOperations.dequeue();
        operation();  // 执行
    }
}

void Window::applyPendingSettings()
{
    if (!m_shellSurface) {
        qWarning() << QStringLiteral("Window::applyPendingSettings: shell surface not available");
        return;
    }

    if (m_hasPendingSkipMultitaskview) {
        qDebug() << QStringLiteral("Applying pending setSkipMultitaskview setting:")
                 << m_pendingSkipMultitaskview;
        m_shellSurface->setSkipMultitaskview(m_pendingSkipMultitaskview);
        m_hasPendingSkipMultitaskview = false;
    }
}

bool Window::ensureWaylandManagerInitialized()
{
    if (s_waylandManager) {
        return true;
    }

    s_waylandManager = std::make_unique<WaylandManager>(qApp);
    if (!s_waylandManager) {
        qCritical() << QStringLiteral("Failed to create WaylandManager instance");
        return false;
    }

    qDebug() << QStringLiteral("WaylandManager initialized successfully");
    return true;
}
