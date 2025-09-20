#ifndef WINDOW_H
#define WINDOW_H

#include "ddeshellclient_export.h"

#include <QEvent>
#include <QHash>
#include <QObject>
#include <QPoint>
#include <QPointer>
#include <QQueue>
#include <QTimer>
#include <QWindow>
#include <qqml.h>

#include <functional>
#include <memory>

#include "shellsurface.h"

class WaylandManager;
class QMainWindow;

class DDESHELLCLIENT_EXPORT Window : public QObject
{
    Q_OBJECT
    QML_ANONYMOUS
    Q_CLASSINFO("RegisterAttachedProperties", "true")

    // Q_PROPERTY declarations for QML support
    Q_PROPERTY(bool skipMultitaskview READ skipMultitaskview WRITE setSkipMultitaskview NOTIFY skipMultitaskviewChanged)
    Q_PROPERTY(bool skipSwitcher READ skipSwitcher WRITE setSkipSwitcher NOTIFY skipSwitcherChanged)
    Q_PROPERTY(bool skipDockPreview READ skipDockPreview WRITE setSkipDockPreview NOTIFY skipDockPreviewChanged)
    Q_PROPERTY(bool acceptKeyboardFocus READ acceptKeyboardFocus WRITE setAcceptKeyboardFocus NOTIFY acceptKeyboardFocusChanged)
    Q_PROPERTY(ShellSurface::Role role READ role WRITE setRole NOTIFY roleChanged)

public:
    // 初始化状态枚举
    enum class InitState {
        NotStarted,              // 未开始
        WaitingForWindowHandle,  // 等待 MainWindow::windowHandle()
        WaitingForWaylandManager, // 等待 WaylandManager 初始化
        WaitingForProtocol,      // 等待 Wayland 协议就绪
        Initializing,            // 正在初始化
        RetryPending,            // 等待重试
        Succeeded,               // 初始化成功
        Failed,                  // 最终失败
    };

    // Static factory methods - return raw pointer managed by Qt parent-child
    [[nodiscard]] static Window *get(QWindow *window);
    [[nodiscard]] static Window *get(QMainWindow *mainWindow);
    ~Window() override;

    // 显式禁用拷贝和移动操作 - 确保对象生命周期管理的安全性
    Window(const Window&) = delete;
    Window& operator=(const Window&) = delete;
    Window(Window&& other) noexcept = delete;
    Window& operator=(Window&& other) noexcept = delete;

    // Property getters (for QML)
    [[nodiscard]] bool skipMultitaskview() const { return m_skipMultitaskview; }
    [[nodiscard]] bool skipSwitcher() const { return m_skipSwitcher; }
    [[nodiscard]] bool skipDockPreview() const { return m_skipDockPreview; }
    [[nodiscard]] bool acceptKeyboardFocus() const { return m_acceptKeyboardFocus; }
    [[nodiscard]] ShellSurface::Role role() const { return m_role; }

    // Property setters (send requests to compositor)
    void setSkipMultitaskview(bool skip);
    void setSurfacePosition(const QPoint &pos);
    void setRole(ShellSurface::Role role);
    void setAutoPlacement(uint32_t offset);
    void setSkipSwitcher(bool skip);
    void setSkipDockPreview(bool skip);
    void setAcceptKeyboardFocus(bool accept);

    // 状态查询方法
    [[nodiscard]] bool isInitialized() const { return m_initState == InitState::Succeeded; }
    [[nodiscard]] InitState initState() const { return m_initState; }

    // QML Attached Properties interface
    static Window *qmlAttachedProperties(QObject *object);

Q_SIGNALS:
    void initialized();           // 初始化成功时发出
    void initializationFailed();  // 最终失败时发出（达到最大重试次数）

    // Property change signals (for QML)
    void skipMultitaskviewChanged();
    void skipSwitcherChanged();
    void skipDockPreviewChanged();
    void acceptKeyboardFocusChanged();
    void roleChanged();

private:
    explicit Window(QWindow *window, QObject *parent = nullptr);
    explicit Window(QWindow *window, QMainWindow *mainWindow, QObject *parent = nullptr);

    bool initialize();
    void applyPendingSettings();

    // 延迟初始化相关方法
    void scheduleInitialization();                    // 启动异步初始化流程
    void tryInitialize();                             // 尝试初始化（可能重试）
    void executeQueuedOperations();                   // 执行排队操作
    void handleWindowHandleReady(QWindow *qwindow);  // windowHandle 就绪处理
    void startWindowHandlePolling();                  // 启动轮询
    bool eventFilter(QObject *watched, QEvent *event) override;  // 事件过滤器

    [[nodiscard]] static bool ensureWaylandManagerInitialized();

    static std::unique_ptr<WaylandManager> s_waylandManager;
    static QHash<QWindow *, Window *> s_windows;  // Raw pointer managed by Qt parent-child

    QPointer<QWindow> m_qwindow;
    QScopedPointer<ShellSurface> m_shellSurface;

    // 延迟初始化状态
    InitState m_initState = InitState::NotStarted;
    int m_retryCount = 0;
    int m_retryDelay = 100;  // 初始重试间隔 100ms
    int m_windowHandlePollCount = 0;

    // 操作队列
    QQueue<std::function<void()>> m_pendingOperations;

    // MainWindow 场景支持
    QPointer<QMainWindow> m_mainWindow;

    // Property storage (current state)
    bool m_skipMultitaskview = false;
    bool m_skipSwitcher = false;
    bool m_skipDockPreview = false;
    bool m_acceptKeyboardFocus = true;  // Default: accept keyboard focus
    ShellSurface::Role m_role = ShellSurface::Role::Overlay;

    // Legacy pending settings (for backward compatibility)
    bool m_pendingSkipMultitaskview = false;
    bool m_hasPendingSkipMultitaskview = false;

    // 常量
    static constexpr int kMaxRetryCount = 10;
    static constexpr int kInitialRetryDelay = 100;        // 100ms
    static constexpr int kMaxRetryDelay = 5000;           // 5s
    static constexpr int kWindowHandlePollInterval = 50;  // 50ms
    static constexpr int kMaxWindowHandlePollCount = 20;  // 最多轮询 20 次（1 秒）
};

#endif // WINDOW_H
