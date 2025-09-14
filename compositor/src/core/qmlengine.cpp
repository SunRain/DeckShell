// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "qmlengine.h"

#include "core/rootsurfacecontainer.h"
#include "modules/capture/capture.h"
#include "output/output.h"
#include "surface/surfacewrapper.h"
#include "workspace/workspace.h"
#include "common/treelandlogging.h"

#include <woutput.h>
#include <woutputitem.h>

#include <QQuickItem>

Q_LOGGING_CATEGORY(qLcQmlEngine, "treeland.qmlEngine")

QmlEngine::QmlEngine(QObject *parent)
    : QQmlApplicationEngine(parent)
    , titleBarComponent(this, "DeckShell.Compositor", "TitleBar")
    , decorationComponent(this, "DeckShell.Compositor", "Decoration")
    , windowMenuComponent(this, "DeckShell.Compositor", "WindowMenu")
    , taskBarComponent(this, "DeckShell.Compositor", "TaskBar")
    , surfaceContent(this, "DeckShell.Compositor", "SurfaceContent")
    , xdgShadowComponent(this, "DeckShell.Compositor", "XdgShadow")
    , taskSwitchComponent(this, "DeckShell.Compositor", "TaskSwitcher")
    , geometryAnimationComponent(this, "DeckShell.Compositor", "GeometryAnimation")
    , menuBarComponent(this, "DeckShell.Compositor", "OutputMenuBar")
    , workspaceSwitcher(this, "DeckShell.Compositor", "WorkspaceSwitcher")
    , newAnimationComponent(this, "DeckShell.Compositor", "NewAnimation")
#ifndef DISABLE_DDM
    , lockScreenComponent(this, "DeckShell.Compositor", "Greeter")
#endif
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
        qCFatal(qLcQmlEngine) << "Can't create component:" << component.errorString();
    }
    QQmlEngine::setObjectOwnership(item, QQmlEngine::objectOwnership(parent));
    item->setParent(parent);
    item->setParentItem(parent);
    component.completeCreate();

    return item;
}

QQuickItem *QmlEngine::createTitleBar(SurfaceWrapper *surface, QQuickItem *parent)
{
    return createComponent(titleBarComponent,
                           parent,
                           { { "surface", QVariant::fromValue(surface) } });
}

QQuickItem *QmlEngine::createDecoration(SurfaceWrapper *surface, QQuickItem *parent)
{
    return createComponent(decorationComponent,
                           parent,
                           { { "surface", QVariant::fromValue(surface) } });
}

QObject *QmlEngine::createWindowMenu(QObject *parent)
{
    auto context = qmlContext(parent);
    auto obj = windowMenuComponent.beginCreate(context);
    if (!obj) {
        qCFatal(qLcQmlEngine) << "Can't create WindowMenu:" << windowMenuComponent.errorString();
    }
    obj->setParent(parent);
    windowMenuComponent.completeCreate();

    return obj;
}

QQuickItem *QmlEngine::createBorder(SurfaceWrapper *surface, QQuickItem *parent)
{
    return createComponent(borderComponent,
                           parent,
                           { { "surface", QVariant::fromValue(surface) } });
}

QQuickItem *QmlEngine::createTaskBar(Output *output, QQuickItem *parent)
{
    return createComponent(taskBarComponent, parent, { { "output", QVariant::fromValue(output) } });
}

QQuickItem *QmlEngine::createXdgShadow(QQuickItem *parent)
{
    return createComponent(xdgShadowComponent, parent);
}

QQuickItem *QmlEngine::createTaskSwitcher(Output *output, QQuickItem *parent)
{
    return createComponent(taskSwitchComponent,
                           parent,
                           { { "output", QVariant::fromValue(output) } });
}

QQuickItem *QmlEngine::createGeometryAnimation(SurfaceWrapper *surface,
                                               const QRectF &startGeo,
                                               const QRectF &endGeo,
                                               QQuickItem *parent)
{
    return createComponent(geometryAnimationComponent,
                           parent,
                           {
                               { "surface", QVariant::fromValue(surface) },
                               { "fromGeometry", QVariant::fromValue(startGeo) },
                               { "toGeometry", QVariant::fromValue(endGeo) },
                           });
}

QQuickItem *QmlEngine::createMenuBar(WOutputItem *output, QQuickItem *parent)
{
    return createComponent(menuBarComponent, parent, { { "output", QVariant::fromValue(output) } });
}

QQuickItem *QmlEngine::createWorkspaceSwitcher(Workspace *parent)
{
    return createComponent(workspaceSwitcher, parent);
}

QQuickItem *QmlEngine::createNewAnimation(SurfaceWrapper *surface,
                                          QQuickItem *parent,
                                          uint direction)
{
    return createComponent(newAnimationComponent,
                           parent,
                           {
                               { "target", QVariant::fromValue(surface) },
                               { "direction", QVariant::fromValue(direction) },
                           });
}

QQuickItem *QmlEngine::createLaunchpadAnimation(SurfaceWrapper *surface,
                                                uint direction,
                                                QQuickItem *parent)
{
    return createComponent(launchpadAnimationComponent,
                           parent,
                           {
                               { "target", QVariant::fromValue(surface) },
                               { "direction", QVariant::fromValue(direction) },
                           });
}

QQuickItem *QmlEngine::createLaunchpadCover(SurfaceWrapper *surface,
                                            Output *output,
                                            QQuickItem *parent)
{
    return createComponent(launchpadCoverComponent,
                           parent,
                           { { "wrapper", QVariant::fromValue(surface) },
                             { "output", QVariant::fromValue(output->output()) } });
}

QQuickItem *QmlEngine::createLayerShellAnimation(SurfaceWrapper *surface,
                                                 QQuickItem *parent,
                                                 uint direction)
{
    return createComponent(layershellAnimationComponent,
                           parent,
                           {
                               { "target", QVariant::fromValue(surface) },
                               { "direction", QVariant::fromValue(direction) },
                           });
}

QQuickItem *QmlEngine::createDockPreview(QQuickItem *parent)
{
    return createComponent(dockPreviewComponent, parent);
}

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
    return createComponent(minimizeAnimationComponent,
                           parent,
                           {
                               { "target", QVariant::fromValue(surface) },
                               { "position", QVariant::fromValue(iconGeometry) },
                               { "direction", QVariant::fromValue(direction) },
                           });
}

QQuickItem *QmlEngine::createShowDesktopAnimation(SurfaceWrapper *surface,
                                                  QQuickItem *parent,
                                                  bool show)
{
    return createComponent(showDesktopAnimatioComponentn,
                           parent,
                           {
                               { "target", QVariant::fromValue(surface) },
                               { "showDesktop", QVariant::fromValue(show) },
                           });
}

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
