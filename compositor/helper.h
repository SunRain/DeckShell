// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "qmlengine.h"
#include "workspace/workspace.h"
// #include "shellmanager.h" // ShellManager class not found in target directory

#include <wglobal.h>
#include <wqmlcreator.h>
#include <wseat.h>
#include <wxdgdecorationmanager.h>
#include <wextforeigntoplevellistv1.h>
#include <xcb/xcb.h>

#include <QObject>
#include <QQmlApplicationEngine>
#include <QPropertyAnimation>
#include <QDBusObjectPath>

Q_MOC_INCLUDE(<wtoplevelsurface.h>)
Q_MOC_INCLUDE(<wxdgsurface.h>)
Q_MOC_INCLUDE("surface/surfacewrapper.h")
Q_MOC_INCLUDE("workspace/workspace.h")
Q_MOC_INCLUDE("rootsurfacecontainer.h")
//Q_MOC_INCLUDE("modules/capture/capture.h")
Q_MOC_INCLUDE(<wlayersurface.h>)
Q_MOC_INCLUDE(<QDBusObjectPath>)

QT_BEGIN_NAMESPACE
class QQuickItem;
QT_END_NAMESPACE

WAYLIB_SERVER_BEGIN_NAMESPACE
class WServer;
class WOutputRenderWindow;
class WOutputLayout;
class WCursor;
class WBackend;
class WOutputItem;
class WOutputViewport;
class WOutputLayer;
class WOutput;
class WXWayland;
class WInputMethodHelper;
class WXdgDecorationManager;
class WSocket;
class WSurface;
class WToplevelSurface;
class WSurfaceItem;
class WForeignToplevel;
WAYLIB_SERVER_END_NAMESPACE

QW_BEGIN_NAMESPACE
class qw_renderer;
class qw_allocator;
class qw_compositor;
class qw_idle_notifier_v1;
class qw_idle_inhibit_manager_v1;
class qw_output_configuration_v1;
class qw_output_power_manager_v1;
class qw_idle_inhibitor_v1;
QW_END_NAMESPACE

WAYLIB_SERVER_USE_NAMESPACE
QW_USE_NAMESPACE

// Forward declarations for DDE Shell
class DDEShellManagerInterfaceV1;
class DDEShellSurfaceInterface;

class Output;
class SurfaceWrapper;
class SurfaceContainer;
class RootSurfaceContainer;
class LayerSurfaceContainer;
// class ForeignToplevelV1;
// class LockScreen;
// class ShortcutV1;
// class PersonalizationV1;
// class WallpaperColorV1;
// class WindowManagementV1;
// class Multitaskview;
// class DDEShellManagerInterfaceV1;
// class WindowPickerInterface;
// class VirtualOutputV1;
class ShellHandler;
class PrimaryOutputV1;
class CaptureSourceSelector;
class treeland_window_picker_v1;
// class IMultitaskView;
// class LockScreenInterface;
// class ILockScreen;
// class UserModel;
// class DDMInterfaceV1;

struct wlr_idle_inhibitor_v1;
struct wlr_output_power_v1_set_mode_event;
struct wlr_ext_foreign_toplevel_image_capture_source_manager_v1_request;

QW_BEGIN_NAMESPACE
class qw_ext_foreign_toplevel_image_capture_source_manager_v1;
QW_END_NAMESPACE

class Helper : public WSeatEventFilter
{
    friend class RootSurfaceContainer;
    Q_OBJECT
    Q_PROPERTY(bool socketEnabled READ socketEnabled WRITE setSocketEnabled NOTIFY socketEnabledChanged FINAL)
    //TODO should change name to rootSurfaceContainer?
    Q_PROPERTY(RootSurfaceContainer* rootContainer READ rootSurfaceContainer CONSTANT FINAL)
    //Q_PROPERTY(int currentUserId READ currentUserId WRITE setCurrentUserId NOTIFY currentUserIdChanged FINAL)
    Q_PROPERTY(float animationSpeed READ animationSpeed WRITE setAnimationSpeed NOTIFY animationSpeedChanged FINAL)
    Q_PROPERTY(OutputMode outputMode READ outputMode WRITE setOutputMode NOTIFY outputModeChanged FINAL)
    Q_PROPERTY(QString cursorTheme READ cursorTheme NOTIFY cursorThemeChanged FINAL)
    Q_PROPERTY(QSize cursorSize READ cursorSize NOTIFY cursorSizeChanged FINAL)
   // Q_PROPERTY(CurrentMode currentMode READ currentMode WRITE setCurrentMode NOTIFY currentModeChanged FINAL)

    // Additional properties from source file that can be ported
    // Q_PROPERTY(TogglableGesture* multiTaskViewGesture READ multiTaskViewGesture CONSTANT FINAL) // TogglableGesture class not found
    // Q_PROPERTY(TogglableGesture* windowGesture READ windowGesture CONSTANT FINAL) // TogglableGesture class not found
    Q_PROPERTY(SurfaceWrapper* activatedSurface READ activatedSurface NOTIFY activatedSurfaceChanged FINAL)
    Q_PROPERTY(Workspace* workspace READ workspace CONSTANT FINAL)
    QML_ELEMENT
    QML_SINGLETON

public:
    explicit Helper(QObject *parent = nullptr);
    ~Helper() override;

    enum class OutputMode
    {
        Copy,
        Extension
    };
    Q_ENUM(OutputMode)

    enum class CurrentMode
    {
        Normal,
        LockScreen,
        WindowSwitch,
        Multitaskview
    };
    Q_ENUM(CurrentMode)

    static Helper *instance();

    QmlEngine *qmlEngine() const;
    WOutputRenderWindow *window() const;
    ShellHandler *shellHandler() const;
    Workspace* workspace() const;
    // 新增：output() 方法，用于获取当前输出设备，与模板中的 getOutput() 功能类似但实现不同
    Output* output() const;
    void init();

    // TogglableGesture *multiTaskViewGesture() const; // 缺失：TogglableGesture 类在目标目录中不存在
    // TogglableGesture *windowGesture() const; // 缺失：TogglableGesture 类在目标目录中不存在

    bool socketEnabled() const;
    void setSocketEnabled(bool newSocketEnabled);

    // RootSurfaceContainer *rootContainer() const; // 缺失：与 rootSurfaceContainer() 重复
    Output *getOutput(WOutput *output) const;

    float animationSpeed() const;
    void setAnimationSpeed(float newAnimationSpeed);

    OutputMode outputMode() const;
    void setOutputMode(OutputMode mode);
    Q_INVOKABLE void addOutput();

    void addSocket(WSocket *socket);
    WXWayland *createXWayland();
    void removeXWayland(WXWayland *xwayland);

    WSocket *defaultWaylandSocket() const;
    WXWayland *defaultXWaylandSocket() const;

    // PersonalizationV1 *personalization() const; // 缺失：PersonalizationV1 类在目标目录中不存在

    WSeat *seat() const;

    bool toggleDebugMenuBar();

    QString cursorTheme() const;
    QSize cursorSize() const;
    // WindowManagementV1::DesktopState showDesktopState() const; // 缺失：WindowManagementV1 类在目标目录中不存在

    // Q_INVOKABLE bool isLaunchpad(WLayerSurface *surface) const; // 缺失：Launchpad 检测功能在目标文件中不存在

    // void handleWindowPicker(WindowPickerInterface *picker); // 缺失：窗口选择器处理功能在目标文件中不存在

    RootSurfaceContainer *rootSurfaceContainer() const;

    // void setMultitaskViewImpl(IMultitaskView *impl); // 缺失：多任务视图实现设置功能在目标文件中不存在
    // void setLockScreenImpl(ILockScreen *impl); // 缺失：锁屏实现设置功能在目标文件中不存在

    CurrentMode currentMode() const;
    void setCurrentMode(CurrentMode mode);

    // void showLockScreen(bool switchToGreeter = true); // 缺失：锁屏显示功能在目标文件中不存在

    Output* getOutputAtCursor() const;

    // UserModel *userModel() const; // 缺失：UserModel 类在目标目录中不存在
    // DDMInterfaceV1 *ddmInterfaceV1() const; // 缺失：DDMInterfaceV1 类在目标目录中不存在

    void activateSession();
    void deactivateSession();
    void enableRender();
    void disableRender();

    // 新增：activeSurface() 方法，用于激活表面，与模板中的 activateSurface() 功能类似但参数不同
  //  void activeSurface(SurfaceWrapper *wrapper, Qt::FocusReason reason);
    // 新增：activeSurface() 方法，用于激活表面，无 FocusReason 参数
 //   void activeSurface(SurfaceWrapper *wrapper);
    // 新增：currentUserId() 方法，用于获取当前用户 ID，与模板中的 userModel() 功能相关但实现不同
    int currentUserId() const;
    // 新增：setCurrentUserId() 方法，用于设置当前用户 ID
    void setCurrentUserId(int uid);
public Q_SLOTS:
    void activateSurface(SurfaceWrapper *wrapper, Qt::FocusReason reason = Qt::OtherFocusReason);
    void forceActivateSurface(SurfaceWrapper *wrapper,
                              Qt::FocusReason reason = Qt::OtherFocusReason);
    void fakePressSurfaceBottomRightToReszie(SurfaceWrapper *surface);
    bool surfaceBelongsToCurrentUser(SurfaceWrapper *wrapper);

    // 新增：activeSurface() 槽的重载版本，无 FocusReason 参数
   // void activeSurface(SurfaceWrapper *wrapper);

Q_SIGNALS:
    void socketEnabledChanged();
    void primaryOutputChanged();
    void activatedSurfaceChanged();

    void animationSpeedChanged();
    void socketFileChanged();
    void outputModeChanged();
    void cursorThemeChanged();
    void cursorSizeChanged();

    void currentModeChanged();

    // 新增：keyboardFocusSurfaceChanged() 信号，用于键盘焦点表面变化通知
 //   void keyboardFocusSurfaceChanged();
    // 新增：currentUserIdChanged() 信号，用于当前用户 ID 变化通知
 //   void currentUserIdChanged();
    // 新增：surfaceWrapperAdded() 信号，用于表面包装器添加通知
 //   void surfaceWrapperAdded(SurfaceWrapper *wrapper);
    // 新增：surfaceWrapperAboutToRemove() 信号，用于表面包装器即将移除通知
 //   void surfaceWrapperAboutToRemove(SurfaceWrapper *wrapper);

private Q_SLOTS:
    // void onShowDesktop(); // 缺失：显示桌面处理槽在目标文件中不存在
    // void deleteTaskSwitch(); // 缺失：任务切换删除槽在目标文件中不存在
    // void onPrepareForSleep(bool sleep); // 缺失：睡眠准备处理槽在目标文件中不存在
    // void onSessionNew(const QString &sessionId, const QDBusObjectPath &objectPath); // 缺失：新会话处理槽在目标文件中不存在

private:
    // void onOutputAdded(WOutput *output); // 缺失：输出添加处理方法在目标文件中不存在
    // void onOutputRemoved(WOutput *output); // 缺失：输出移除处理方法在目标文件中不存在
    // void onSurfaceModeChanged(WSurface *surface, WXdgDecorationManager::DecorationMode mode); // 缺失：表面模式变化处理方法在目标文件中不存在
    // void setGamma(struct wlr_gamma_control_manager_v1_set_gamma_event *event); // 缺失：伽马设置方法在目标文件中不存在
    // void onOutputTestOrApply(qw_output_configuration_v1 *config, bool onlyTest); // 缺失：输出测试或应用方法在目标文件中不存在
    // void onSetOutputPowerMode(wlr_output_power_v1_set_mode_event *event); // 缺失：输出电源模式设置方法在目标文件中不存在
    // void onNewIdleInhibitor(wlr_idle_inhibitor_v1 *inhibitor); // 缺失：空闲抑制器添加方法在目标文件中不存在
    // void onDockPreview(std::vector<SurfaceWrapper *> surfaces,
	//				 WSurface *target, 
	//				 QPoint pos, 
	//				 ForeignToplevelV1::PreviewDirection direction); // 缺失：Dock预览方法在目标文件中不存在
	// void onDockPreviewTooltip(QString tooltip,
	//			  WSurface *target,
	//			  QPoint pos, 
	//			  ForeignToplevelV1::PreviewDirection direction); // 缺失：Dock预览工具提示方法在目标文件中不存在
    // void onSetCopyOutput(treeland_virtual_output_v1 *virtual_output); // 缺失：设置复制输出方法在目标文件中不存在
    // void onRestoreCopyOutput(treeland_virtual_output_v1 *virtual_output); // 缺失：恢复复制输出方法在目标文件中不存在
    // void onSurfaceWrapperAdded(SurfaceWrapper *wrapper); // 缺失：表面包装器添加处理方法在目标文件中不存在
    // void onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper); // 缺失：表面包装器即将移除处理方法在目标文件中不存在
    // void handleRequestDrag([[maybe_unused]] WSurface *surface); // 缺失：拖拽请求处理方法在目标文件中不存在
    // void handleLockScreen(LockScreenInterface *lockScreen); // 缺失：锁屏处理方法在目标文件中不存在
    // void onSessionLock(); // 缺失：会话锁定处理方法在目标文件中不存在
    // void onSessionUnlock(); // 缺失：会话解锁处理方法在目标文件中不存在
    // void handleNewForeignToplevelCaptureRequest(wlr_ext_foreign_toplevel_image_capture_source_manager_v1_request *request); // 缺失：外来顶层捕获请求处理方法在目标文件中不存在

private:
    void allowNonDrmOutputAutoChangeMode(WOutput *output);

    int indexOfOutput(WOutput *output) const;

    SurfaceWrapper *keyboardFocusSurface() const;
    // void requestKeyboardFocusForSurface(SurfaceWrapper *newActivateSurface, Qt::FocusReason reason); // 缺失：键盘焦点请求方法在目标文件中不存在
    SurfaceWrapper *activatedSurface() const;
    void setActivatedSurface(SurfaceWrapper *newActivateSurface);

    void setCursorPosition(const QPointF &position);

    bool beforeDisposeEvent(WSeat *seat, QWindow *watched, QInputEvent *event) override;
    bool afterHandleEvent([[maybe_unused]] WSeat *seat,
                          WSurface *watched,
                          QObject *surfaceItem,
                          QObject *,
                          QInputEvent *event) override;
    bool unacceptedEvent(WSeat *, QWindow *, QInputEvent *event) override;

    // void handleLeftButtonStateChanged(const QInputEvent *event); // 缺失：左键状态变化处理方法在目标文件中不存在
    // void handleWhellValueChanged(const QInputEvent *event); // 缺失：滚轮值变化处理方法在目标文件中不存在
    // bool doGesture(QInputEvent *event); // 缺失：手势处理方法在目标文件中不存在
    // Output *createNormalOutput(WOutput *output); // 缺失：创建普通输出方法在目标文件中不存在
    // Output *createCopyOutput(WOutput *output, Output *proxy); // 缺失：创建复制输出方法在目标文件中不存在
    // QList<SurfaceWrapper *> getWorkspaceSurfaces(Output *filterOutput = nullptr); // 缺失：获取工作区表面方法在目标文件中不存在
    // void moveSurfacesToOutput(const QList<SurfaceWrapper *> &surfaces, Output *targetOutput, Output *sourceOutput); // 缺失：移动表面到输出方法在目标文件中不存在
    // bool isNvidiaCardPresent(); // 缺失：NVIDIA显卡检测方法在目标文件中不存在
    // void setWorkspaceVisible(bool visible); // 缺失：设置工作区可见性方法在目标文件中不存在
    bool isNvidiaCardPresent();
    void setWorkspaceVisible(bool visible);
    void restoreFromShowDesktop(SurfaceWrapper *activeSurface = nullptr);
    void updateIdleInhibitor();

    static Helper *m_instance;

    CurrentMode m_currentMode{ CurrentMode::Normal };

    // qtquick helper
    WOutputRenderWindow *m_renderWindow = nullptr;
    // QQuickItem *m_dockPreview = nullptr; // 缺失：Dock预览项在目标文件中不存在

    // gesture
    WServer *m_server = nullptr;
    RootSurfaceContainer *m_rootSurfaceContainer = nullptr;
    // TogglableGesture *m_multiTaskViewGesture = nullptr; // 缺失：多任务视图手势在目标文件中不存在
    // TogglableGesture *m_windowGesture = nullptr; // 缺失：窗口手势在目标文件中不存在

    // wayland helper
    WSocket *m_socket = nullptr;
    WSeat *m_seat = nullptr;
    WBackend *m_backend = nullptr;
    qw_renderer *m_renderer = nullptr;
    qw_allocator *m_allocator = nullptr;

    // protocols
    qw_compositor *m_compositor = nullptr;
    // qw_idle_notifier_v1 *m_idleNotifier = nullptr; // 缺失：空闲通知器在目标文件中不存在
    // qw_idle_inhibit_manager_v1 *m_idleInhibitManager = nullptr; // 缺失：空闲抑制管理器在目标文件中不存在
    // qw_output_power_manager_v1 *m_outputPowerManager = nullptr; // 缺失：输出电源管理器在目标文件中不存在
    // qw_ext_foreign_toplevel_image_capture_source_manager_v1 *m_foreignToplevelImageCaptureManager = nullptr; // 缺失：外来顶层图像捕获管理器在目标文件中不存在
    ShellHandler *m_shellHandler = nullptr;
    // WXWayland *m_defaultXWayland = nullptr; // 缺失：默认XWayland在目标文件中不存在
    WXdgDecorationManager *m_xdgDecorationManager = nullptr;
    WForeignToplevel *m_foreignToplevel = nullptr;
    WExtForeignToplevelListV1 *m_extForeignToplevelListV1 = nullptr;
    // ForeignToplevelV1 *m_treelandForeignToplevel = nullptr; // 缺失：Treeland外来顶层在目标文件中不存在
    // ShortcutV1 *m_shortcut = nullptr; // 缺失：快捷键在目标文件中不存在
    // PersonalizationV1 *m_personalization = nullptr; // 缺失：个性化在目标文件中不存在
    // WallpaperColorV1 *m_wallpaperColorV1 = nullptr; // 缺失：壁纸颜色在目标文件中不存在
    // WOutputManagerV1 *m_outputManager = nullptr; // 缺失：输出管理器在目标文件中不存在
    // WindowManagementV1 *m_windowManagement = nullptr; // 缺失：窗口管理在目标文件中不存在
    // WindowManagementV1::DesktopState m_showDesktop = WindowManagementV1::DesktopState::Normal; // 缺失：显示桌面状态在目标文件中不存在
    DDEShellManagerInterfaceV1 *m_ddeShellV1 = nullptr;
    // VirtualOutputV1 *m_virtualOutput = nullptr; // 缺失：虚拟输出在目标文件中不存在
    PrimaryOutputV1 *m_primaryOutputV1 = nullptr;
    // DDMInterfaceV1 *m_ddmInterfaceV1 = nullptr; // 缺失：DDM接口在目标文件中不存在

    // private data
    QList<Output *> m_outputList;
    // QPointer<QQuickItem> m_taskSwitch; // 缺失：任务切换项在目标文件中不存在
    // QList<qw_idle_inhibitor_v1 *> m_idleInhibitors; // 缺失：空闲抑制器列表在目标文件中不存在

    SurfaceWrapper *m_activatedSurface = nullptr;
    // LockScreen *m_lockScreen = nullptr; // 缺失：锁屏在目标文件中不存在
    float m_animationSpeed = 1.0;
    // quint64 m_taskAltTimestamp = 0; // 缺失：任务Alt时间戳在目标文件中不存在
    // quint32 m_taskAltCount = 0; // 缺失：任务Alt计数在目标文件中不存在
    OutputMode m_mode = OutputMode::Extension;
    std::optional<QPointF> m_fakelastPressedPosition;

    // QPointer<CaptureSourceSelector> m_captureSelector; // 缺失：捕获源选择器在目标文件中不存在

    // QPropertyAnimation *m_workspaceScaleAnimation{ nullptr }; // 缺失：工作区缩放动画在目标文件中不存在
    // QPropertyAnimation *m_workspaceOpacityAnimation{ nullptr }; // 缺失：工作区不透明度动画在目标文件中不存在

    // bool m_singleMetaKeyPendingPressed{ false }; // 缺失：单Meta键待按下状态在目标文件中不存在

    // IMultitaskView *m_multitaskView{ nullptr }; // 缺失：多任务视图在目标文件中不存在
    // UserModel *m_userModel{ nullptr }; // 缺失：用户模型在目标文件中不存在

    // quint32 m_atomDeepinNoTitlebar; // 缺失：Deepin无标题栏原子在目标文件中不存在
};
