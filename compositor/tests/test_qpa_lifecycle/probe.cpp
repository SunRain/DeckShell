// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <wserver.h>

#include <QGuiApplication>
#include <qpa/qplatformtheme.h>

WAYLIB_SERVER_USE_NAMESPACE

int main(int argc, char *argv[])
{
    WServer::initializeQPA({ }, [](const QString &) {
        return static_cast<QPlatformTheme *>(new QPlatformTheme());
    });

    QGuiApplication app(argc, argv);
    return 0;
}
