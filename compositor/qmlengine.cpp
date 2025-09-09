// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "output.h"
#include "qmlengine.h"
#include "surface/surfacewrapper.h"
#include "wallpaperprovider.h"
#include "workspace/workspace.h"

#include <woutputitem.h>

#include <QQuickItem>
#include <QVariantMap>

Q_LOGGING_CATEGORY(qLcCompositor, "deckshell.qmlEngine")

QmlEngine::QmlEngine(QObject *parent)
    : QQmlApplicationEngine(parent)
    , titleBarComponent(this, "DeckShell.Compositor", "TitleBar")
    , decorationComponent(this, "DeckShell.Compositor", "Decoration")
    , windowMenuComponent(this, "DeckShell.Compositor", "WindowMenu")
    , borderComponent(this, "DeckShell.Compositor", "Border")
    , taskBarComponent(this, "DeckShell.Compositor", "TaskBar")
    , surfaceContent(this, "DeckShell.Compositor", "SurfaceContent")
    , shadowComponent(this, "DeckShell.Compositor", "Shadow")
    , xdgShadowComponent(this, "DeckShell.Compositor", "XdgShadow")
    , taskSwitchComponent(this, "DeckShell.Compositor", "TaskSwitcher")
    , geometryAnimationComponent(this, "DeckShell.Compositor", "GeometryAnimation")
    , menuBarComponent(this, "DeckShell.Compositor", "OutputMenuBar")
    , workspaceSwitcher(this, "DeckShell.Compositor", "WorkspaceSwitcher")
    , newAnimationComponent(this, "DeckShell.Compositor", "NewAnimation")
    , lockScreenComponent(this, "DeckShell.Compositor", "LockScreen")
    , dockPreviewComponent(this, "DeckShell.Compositor", "DockPreview")
    , minimizeAnimationComponent(this, "DeckShell.Compositor", "MinimizeAnimation")
    , showDesktopAnimatioComponentn(this, "DeckShell.Compositor", "ShowDesktopAnimation")
    , captureSelectorComponent(this, "DeckShell.Compositor", "CaptureSelectorLayer")
    , windowPickerComponent(this, "DeckShell.Compositor", "WindowPickerLayer")
    , launchpadAnimationComponent(this, "DeckShell.Compositor", "LaunchpadAnimation")
    , launchpadCoverComponent(this, "DeckShell.Compositor", "LaunchpadCover")
    , layershellAnimationComponent(this, "DeckShell.Compositor", "LayerShellAnimation")
{
}

QQuickItem *QmlEngine::createComponent(QQmlComponent &component,
                                      QQuickItem *parent,
                                      const QVariantMap &properties)
{
    auto context = qmlContext(parent);
    auto obj = component.beginCreate(context);
    if (!properties.isEmpty()) {
        component.setInitialProperties(obj, properties);
    }
    auto item = qobject_cast<QQuickItem *>(obj);
    if (!item) {
        qCFatal(qLcCompositor) << "Can't create component:" << component.errorString();
        return nullptr;
    }
    QQmlEngine::setObjectOwnership(item, QQmlEngine::objectOwnership(parent));
    item->setParent(parent);
    item->setParentItem(parent);
    component.completeCreate();

    qCDebug(qLcCompositor) << "Component created successfully:" << component.url().toString();
    return item;
}

QQuickItem *QmlEngine::createTitleBar(SurfaceWrapper *surface, QQuickItem *parent)
{
    return createComponent(titleBarComponent, parent, {
        {"surface", QVariant::fromValue(surface)}
    });
}

QQuickItem *QmlEngine::createDecoration(SurfaceWrapper *surface, QQuickItem *parent)
{
    return createComponent(decorationComponent, parent, {
        {"surface", QVariant::fromValue(surface)}
    });
}

QObject *QmlEngine::createWindowMenu(QObject *parent)
{
    auto context = qmlContext(parent);
    auto obj = windowMenuComponent.beginCreate(context);
    if (!obj) {
        qCFatal(qLcCompositor) << "Can't create WindowMenu:" << windowMenuComponent.errorString();
    }
    obj->setParent(parent);
    windowMenuComponent.completeCreate();

    return obj;
}

QQuickItem *QmlEngine::createBorder(SurfaceWrapper *surface, QQuickItem *parent)
{
    return createComponent(borderComponent, parent, {
        {"surface", QVariant::fromValue(surface)}
    });
}

QQuickItem *QmlEngine::createTaskBar(Output *output, QQuickItem *parent)
{
    auto item = createComponent(taskBarComponent, parent, {
        {"output", QVariant::fromValue(output)}
    });
    if (!item) {
        qCWarning(qLcCompositor) << "Failed to create TaskBar:" << taskBarComponent.errorString();
    }
    return item;
}

QQuickItem *QmlEngine::createXdgShadow(QQuickItem *parent)
{
    return createComponent(xdgShadowComponent, parent);
}

QQuickItem *QmlEngine::createTaskSwitcher(Output *output, QQuickItem *parent)
{
    return createComponent(taskSwitchComponent, parent, {
        {"output", QVariant::fromValue(output)}
    });
}

QQuickItem *QmlEngine::createGeometryAnimation(SurfaceWrapper *surface,
                                                const QRectF &startGeo,
                                                const QRectF &endGeo,
                                                QQuickItem *parent)
{
    return createComponent(geometryAnimationComponent, parent, {
        {"surface", QVariant::fromValue(surface)},
        {"fromGeometry", QVariant::fromValue(startGeo)},
        {"toGeometry", QVariant::fromValue(endGeo)}
    });
}

QQuickItem *QmlEngine::createMenuBar(WOutputItem *output, QQuickItem *parent)
{
    return createComponent(menuBarComponent, parent, {
        {"output", QVariant::fromValue(output)}
    });
}

// QQuickItem *QmlEngine::createWorkspaceSwitcher(Workspace *parent, WorkspaceModel *from, WorkspaceModel *to)
// {
//     // 注意：参数不同，模板是 (Workspace *parent)，目标是 (Workspace *parent, WorkspaceModel *from, WorkspaceModel *to)
//     return createComponent(workspaceSwitcher, parent, {
//         {"parent", QVariant::fromValue(parent)},
//         {"from", QVariant::fromValue(from)},
//         {"to", QVariant::fromValue(to)}
//     });
// }
QQuickItem *QmlEngine::createWorkspaceSwitcher(Workspace *parent)
{
    return createComponent(workspaceSwitcher, parent);
}

QQuickItem *QmlEngine::createNewAnimation(SurfaceWrapper *surface, QQuickItem *parent, uint direction)
{
    return createComponent(newAnimationComponent, parent, {
        {"target", QVariant::fromValue(surface)},
        {"direction", QVariant::fromValue(direction)}
    });
}

QQuickItem *QmlEngine::createLaunchpadAnimation(SurfaceWrapper *surface, uint direction, QQuickItem *parent)
{
    return createComponent(launchpadAnimationComponent, parent, {
        {"target", QVariant::fromValue(surface)},
        {"direction", QVariant::fromValue(direction)}
    });
}

QQuickItem *QmlEngine::createLaunchpadCover(SurfaceWrapper *surface, Output *output, QQuickItem *parent)
{
    return createComponent(launchpadCoverComponent, parent, {
        {"wrapper", QVariant::fromValue(surface)},
        {"output", QVariant::fromValue(output->output())}
    });
}

QQuickItem *QmlEngine::createLayerShellAnimation(SurfaceWrapper *surface, QQuickItem *parent, uint direction)
{
    return createComponent(layershellAnimationComponent, parent, {
        {"target", QVariant::fromValue(surface)},
        {"direction", QVariant::fromValue(direction)}
    });
}

QQuickItem *QmlEngine::createDockPreview(QQuickItem *parent)
{
    return createComponent(dockPreviewComponent, parent);
}

// QQuickItem *QmlEngine::createLockScreen(QQuickItem *parent)
// {
//     // 注意：参数不同，模板是 (Output *output, QQuickItem *parent)，目标是 (QQuickItem *parent)
//     return createComponent(lockScreenComponent, parent);
// }

QQuickItem *QmlEngine::createLockScreen(Output *output, QQuickItem *parent)
{
#ifndef DISABLE_DDM
    return createComponent(lockScreenComponent,
                           parent,
                           { { "output", QVariant::fromValue(output->output()) },
                             { "outputItem", QVariant::fromValue(output->outputItem()) } });
#else
    Q_UNREACHABLE_RETURN(nullptr);
#endif
}

QQuickItem *QmlEngine::createMinimizeAnimation(SurfaceWrapper *surface,
                                               QQuickItem *parent,
                                               const QRectF &iconGeometry,
                                               uint direction)
{
    return createComponent(minimizeAnimationComponent, parent, {
        {"target", QVariant::fromValue(surface)},
        {"position", QVariant::fromValue(iconGeometry)},
        {"direction", QVariant::fromValue(direction)}
    });
}

QQuickItem *QmlEngine::createShowDesktopAnimation(SurfaceWrapper *surface, QQuickItem *parent, bool show)
{
    return createComponent(showDesktopAnimatioComponentn, parent, {
        {"target", QVariant::fromValue(surface)},
        {"showDesktop", QVariant::fromValue(show)}
    });
}

// QQuickItem *QmlEngine::createCaptureSelector(QQuickItem *parent, class CaptureManagerV1 *captureManager)
// {
//     // 注意：目标中被注释掉，现已取消注释并实现
//     return createComponent(
//         captureSelectorComponent,
//         parent,
//         { { "captureManager", QVariant::fromValue(captureManager) },
//           { "z", QVariant::fromValue(1000) } } ); // 使用固定值代替 RootSurfaceContainer::CaptureLayerZOrder
// }

QQuickItem *QmlEngine::createCaptureSelector(QQuickItem *parent, CaptureManagerV1 *captureManager)
{
    return createComponent(
        captureSelectorComponent,
        parent,
        { { "captureManager", QVariant::fromValue(captureManager) },
          { "z", QVariant::fromValue(RootSurfaceContainer::CaptureLayerZOrder) } });
}


QQuickItem *QmlEngine::createWindowPicker(QQuickItem *parent)
{
    return createComponent(windowPickerComponent, parent);
}

// 新增：createShadow (对应模板的 createXdgShadow，但名称不同)
QQuickItem *QmlEngine::createShadow(QQuickItem *parent)
{
    return createComponent(shadowComponent, parent);
}

// 新增：高级组件创建方法 with error handling
QQuickItem *QmlEngine::createComponentWithErrorHandling(QQmlComponent &component,
                                                        QQuickItem *parent,
                                                        const QVariantMap &properties,
                                                        QString *errorString)
{
    auto context = qmlContext(parent);
    auto obj = component.beginCreate(context);
    if (!properties.isEmpty()) {
        component.setInitialProperties(obj, properties);
    }
    auto item = qobject_cast<QQuickItem *>(obj);

    if (item) {
        item->setParent(parent);
        item->setParentItem(parent);
        component.completeCreate();
        qCDebug(qLcCompositor) << "Component created successfully with error handling:" << component.url().toString();
        return item;
    } else {
        QString error = component.errorString();
        qCWarning(qLcCompositor) << "Failed to create component with error handling:" << error;
        if (errorString) {
            *errorString = error;
        }
        component.completeCreate();
        return nullptr;
    }
}

// 新增：异步组件创建方法
QQuickItem *QmlEngine::createComponentAsync(QQmlComponent &component,
                                             QQuickItem *parent,
                                             const QVariantMap &properties,
                                             const std::function<void(QQuickItem*, const QString&)> &callback)
{
    auto context = qmlContext(parent);
    auto obj = component.beginCreate(context);
    if (!properties.isEmpty()) {
        component.setInitialProperties(obj, properties);
    }
    auto item = qobject_cast<QQuickItem *>(obj);

    if (item) {
        item->setParent(parent);
        item->setParentItem(parent);
        component.completeCreate();
        qCDebug(qLcCompositor) << "Component created successfully asynchronously:" << component.url().toString();
        if (callback) {
            callback(item, QString());
        }
        return item;
    } else {
        QString error = component.errorString();
        qCWarning(qLcCompositor) << "Failed to create component asynchronously:" << error;
        component.completeCreate();
        if (callback) {
            callback(nullptr, error);
        }
        return nullptr;
    }
}

// 新增：重载版本
QQuickItem *QmlEngine::createLaunchpadAnimation(QQuickItem *parent)
{
    return createComponent(launchpadAnimationComponent, parent);
}

// 新增：重载版本
QQuickItem *QmlEngine::createLaunchpadCover(QQuickItem *parent)
{
    return createComponent(launchpadCoverComponent, parent);
}

// 新增：重载版本
QQuickItem *QmlEngine::createLayerShellAnimation(QQuickItem *parent)
{
    return createComponent(layershellAnimationComponent, parent);
}

// 新增：wallpaperImageProvider
// WallpaperImageProvider *QmlEngine::wallpaperImageProvider()
// {
//     if (!wallpaperProvider) {
//         wallpaperProvider = new WallpaperImageProvider;
//         Q_ASSERT(!this->imageProvider("wallpaper"));
//         addImageProvider("wallpaper", wallpaperProvider);
//     }

//     return wallpaperProvider;
// }
