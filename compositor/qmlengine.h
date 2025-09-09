// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QQmlApplicationEngine>
#include <QQmlComponent>
#include <QLoggingCategory>
#include <functional>

#include <wglobal.h>

QT_BEGIN_NAMESPACE
class QQuickItem;
QT_END_NAMESPACE

WAYLIB_SERVER_BEGIN_NAMESPACE
class WOutputItem;
WAYLIB_SERVER_END_NAMESPACE

WAYLIB_SERVER_USE_NAMESPACE

Q_DECLARE_LOGGING_CATEGORY(qLcCompositor)

//class WallpaperImageProvider;
class SurfaceWrapper;
class Output;
class Workspace;
class WorkspaceModel;

//#include "surface/surfaceproxy.h"

// Forward declaration for CaptureManagerV1
class CaptureManagerV1;
//Q_DECLARE_OPAQUE_POINTER(CaptureManagerV1)
class QmlEngine : public QQmlApplicationEngine
{
    Q_OBJECT
public:
    explicit QmlEngine(QObject *parent = nullptr);

    // 通用组件创建方法
    QQuickItem *createComponent(QQmlComponent &component,
                                QQuickItem *parent,
                                const QVariantMap &properties = QVariantMap());

    // 新增：高级组件创建方法 with error handling
    QQuickItem *createComponentWithErrorHandling(QQmlComponent &component,
                                                 QQuickItem *parent,
                                                 const QVariantMap &properties = QVariantMap(),
                                                 QString *errorString = nullptr);

    // 新增：异步组件创建方法
    QQuickItem *createComponentAsync(QQmlComponent &component,
                                     QQuickItem *parent,
                                     const QVariantMap &properties = QVariantMap(),
                                     const std::function<void(QQuickItem*, const QString&)> &callback = nullptr);

    QQuickItem *createTitleBar(SurfaceWrapper *surface, QQuickItem *parent);
    QQuickItem *createDecoration(SurfaceWrapper *surface, QQuickItem *parent);
    QObject *createWindowMenu(QObject *parent);
    QQuickItem *createBorder(SurfaceWrapper *surface, QQuickItem *parent);
    QQuickItem *createTaskBar(Output *output, QQuickItem *parent);
    // 新增：createShadow (对应模板的 createXdgShadow，但名称不同)
    QQuickItem *createShadow(QQuickItem *parent);
    QQuickItem *createXdgShadow(QQuickItem *parent);
    QQuickItem *createTaskSwitcher(Output *output, QQuickItem *parent);
    QQuickItem *createGeometryAnimation(SurfaceWrapper *surface,
                                        const QRectF &startGeo,
                                        const QRectF &endGeo,
                                        QQuickItem *parent);
    QQuickItem *createMenuBar(WOutputItem *output, QQuickItem *parent);
    // 注意：参数不同，模板是 (Workspace *parent)，目标是 (Workspace *parent, WorkspaceModel *from, WorkspaceModel *to)
    QQuickItem *createWorkspaceSwitcher(Workspace *parent);
//	QQuickItem *createWorkspaceSwitcher(Workspace *parent, WorkspaceModel *from, WorkspaceModel *to);
    QQuickItem *createNewAnimation(SurfaceWrapper *surface, QQuickItem *parent, uint direction);
    QQuickItem *createLaunchpadAnimation(SurfaceWrapper *surface,
                                         uint direction,
                                         QQuickItem *parent);
    // 新增：重载版本
   // QQuickItem *createLaunchpadAnimation(QQuickItem *parent);
    QQuickItem *createLaunchpadCover(SurfaceWrapper *surface, Output *output, QQuickItem *parent);
    // 新增：重载版本
   // QQuickItem *createLaunchpadCover(QQuickItem *parent);
    QQuickItem *createLayerShellAnimation(SurfaceWrapper *surface,
                                          QQuickItem *parent,
                                          uint direction);
    // 新增：重载版本
  //  QQuickItem *createLayerShellAnimation(QQuickItem *parent);
    // 注意：参数不同，模板是 (Output *output, QQuickItem *parent)，目标是 (QQuickItem *parent)
   // QQuickItem *createLockScreen(QQuickItem *parent);
    QQuickItem *createLockScreen(Output *output, QQuickItem *parent);
    QQuickItem *createMinimizeAnimation(SurfaceWrapper *surface,
                                        QQuickItem *parent,
                                        const QRectF &iconGeometry,
                                        uint direction);
    // 注意：目标有重载版本
    //QQuickItem *createMinimizeAnimation(SurfaceWrapper *surface, QQuickItem *parent);
    QQuickItem *createDockPreview(QQuickItem *parent);
    QQuickItem *createShowDesktopAnimation(SurfaceWrapper *surface, QQuickItem *parent, bool show);
   // QQuickItem *createCaptureSelector(QQuickItem *parent, class CaptureManagerV1 *captureManager);
   QQuickItem *createCaptureSelector(QQuickItem *parent, CaptureManagerV1 *captureManager);
    QQuickItem *createWindowPicker(QQuickItem *parent);
    QQmlComponent *surfaceContentComponent() { return &surfaceContent; }
    // 新增
  //  WallpaperImageProvider *wallpaperImageProvider();

private:
    QQmlComponent titleBarComponent;
    QQmlComponent decorationComponent;
    QQmlComponent windowMenuComponent;
    QQmlComponent borderComponent;
    QQmlComponent taskBarComponent;
    QQmlComponent surfaceContent;
    // 新增：shadowComponent (对应 createShadow)
    QQmlComponent shadowComponent;
    QQmlComponent xdgShadowComponent;
    QQmlComponent taskSwitchComponent;
    QQmlComponent geometryAnimationComponent;
    QQmlComponent menuBarComponent;
    QQmlComponent workspaceSwitcher;
    QQmlComponent newAnimationComponent;
    // 注意：模板有 #ifndef DISABLE_DDM 条件
#ifndef DISABLE_DDM
    QQmlComponent lockScreenComponent;
#endif
    QQmlComponent dockPreviewComponent;
    QQmlComponent minimizeAnimationComponent;
    QQmlComponent showDesktopAnimatioComponentn;
    QQmlComponent captureSelectorComponent;
    QQmlComponent windowPickerComponent;
    QQmlComponent launchpadAnimationComponent;
    QQmlComponent launchpadCoverComponent;
    QQmlComponent layershellAnimationComponent;
};
