// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadviewer.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setApplicationName("gamepad-visualizer");
    app.setApplicationVersion("1.0.0");

    GamepadViewer viewer;
    viewer.resize(700, 600);
    viewer.show();

    return app.exec();
}
