// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

import QtQuick
import QtQuick.Controls

Item {
    id: root

    Rectangle {
        anchors.fill: parent
        color: "black"
        opacity: 0.8
    }

    Text {
        anchors.centerIn: parent
        text: "Lock Screen"
        font.pointSize: 24
        color: "white"
    }

    // TODO: Implement lock screen functionality
}