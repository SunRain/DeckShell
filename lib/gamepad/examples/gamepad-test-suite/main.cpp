// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QApplication>
#include <QCommandLineParser>
#include "gamepadtestsuite.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setApplicationName("Gamepad Test Suite");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("DeckShell");
    
    // 命令行参数
    QCommandLineParser parser;
    parser.setApplicationDescription("Treeland Gamepad Protocol Test Suite - 综合测试工具");
    parser.addHelpOption();
    parser.addVersionOption();
    
    QCommandLineOption debugOption(QStringList() << "d" << "debug",
                                   "启用调试输出");
    parser.addOption(debugOption);
    
    QCommandLineOption socketOption(QStringList() << "s" << "socket",
                                   "指定Wayland socket名称", "socket");
    parser.addOption(socketOption);
    
    parser.process(app);
    
    // 设置调试级别
    if (parser.isSet(debugOption)) {
        qSetMessagePattern("[%{time h:mm:ss.zzz}] [%{category}] %{message}");
    }
    
    // 创建主窗口
    GamepadTestSuite window;
    
    // 如果指定了socket，传递给窗口
    if (parser.isSet(socketOption)) {
        window.setWaylandSocket(parser.value(socketOption));
    }
    
    window.show();
    
    return app.exec();
}
