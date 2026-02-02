// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import DeckShell.DeckGamepad

ApplicationWindow {
    id: root
    width: 900
    height: 520
    visible: true
    title: "DeckShell.DeckGamepad demo"

    property int selectedDeviceId: -1

    Component.onCompleted: {
        GamepadManager.start()
    }

    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            spacing: 12

            Label { text: "Backend:" }
            ComboBox {
                id: backendCombo
                model: [ "Auto", "Evdev（providerSelection 决定 IO/单线程）", "Treeland" ]
                onActivated: (index) => {
                    GamepadManager.backendMode = index
                }
            }

            Label { text: "ProviderSelection:" }
            ComboBox {
                id: providerCombo
                // 不再暴露 EvdevUdev（legacy evdev-udev）；如需单线程调试模式，请使用：
                // - 环境变量：DECKGAMEPAD_EVDEV_SINGLE_THREAD=1
                // - 或构建期：-DDECKGAMEPAD_DEFAULT_PROVIDER=evdev-udev
                model: [ "Auto", "Evdev" ]
                currentIndex: GamepadManager.providerSelection === 2 ? 1 : 0
                onActivated: (index) => {
                    GamepadManager.providerSelection = (index === 0) ? 0 : 2
                }
            }

            Button {
                text: "Start"
                onClicked: GamepadManager.start()
            }
            Button {
                text: "Stop"
                onClicked: GamepadManager.stop()
            }

            Label {
                text: "Active: " + GamepadManager.activeBackend + " (" + GamepadManager.activeProviderName + ")"
            }

            Item { Layout.fillWidth: true }
        }
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        GroupBox {
            title: "Devices"
            Layout.preferredWidth: 320
            Layout.fillHeight: true

            ColumnLayout {
                anchors.fill: parent
                spacing: 8

                Label { text: "Connected: " + GamepadManager.connectedCount }

                ListView {
                    id: listView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: GamepadManager.deviceModel

                    delegate: ItemDelegate {
                        width: listView.width
                        text: model.deviceName + " (id=" + model.deviceId + ")"
                        highlighted: model.deviceId === root.selectedDeviceId
                        onClicked: root.selectedDeviceId = model.deviceId
                    }
                }

                TextArea {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 90
                    readOnly: true
                    wrapMode: Text.Wrap
                    text: GamepadManager.diagnostic
                        + (GamepadManager.diagnosticKey.length ? ("\nkey: " + GamepadManager.diagnosticKey) : "")
                        + (GamepadManager.suggestedActions.length ? ("\nactions: " + GamepadManager.suggestedActions.join(", ")) : "")
                    placeholderText: "diagnostic"
                }
            }
        }

        GroupBox {
            title: "Selected device"
            Layout.fillWidth: true
            Layout.fillHeight: true

            Gamepad {
                id: gp
                deviceId: root.selectedDeviceId
            }

            ServiceActionRouter {
                id: serviceRouter
                active: true
                gamepad: gp
            }

            GamepadKeyNavigation {
                id: nav
                active: true
                gamepad: gp
                actionSource: serviceRouter
                target: keySink
            }

            ColumnLayout {
                anchors.fill: parent
                spacing: 8

                Label { text: "deviceId: " + gp.deviceId }
                Label { text: "name: " + gp.name }
                Label { text: "connected: " + gp.connected }
                Label { text: "hat: " + gp.hatDirection }
                Label { text: "keyNav.suppressionReason: " + nav.suppressionReason }

                GridLayout {
                    columns: 4
                    Layout.fillWidth: true

                    Label { text: "A: " + gp.buttonA }
                    Label { text: "B: " + gp.buttonB }
                    Label { text: "X: " + gp.buttonX }
                    Label { text: "Y: " + gp.buttonY }

                    Label { text: "Up: " + gp.buttonDpadUp }
                    Label { text: "Down: " + gp.buttonDpadDown }
                    Label { text: "Left: " + gp.buttonDpadLeft }
                    Label { text: "Right: " + gp.buttonDpadRight }

                    Label { text: "LX: " + gp.axisLeftX.toFixed(2) }
                    Label { text: "LY: " + gp.axisLeftY.toFixed(2) }
                    Label { text: "RX: " + gp.axisRightX.toFixed(2) }
                    Label { text: "RY: " + gp.axisRightY.toFixed(2) }
                }

                Rectangle {
                    id: keySink
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "#111111"
                    radius: 8
                    focus: true

                    property string lastKeyText: ""
                    property string lastActionText: ""

                    Keys.onPressed: (event) => {
                        lastKeyText = "Key pressed: " + event.key
                        event.accepted = true
                    }
                    Keys.onReleased: (event) => {
                        lastKeyText = "Key released: " + event.key
                        event.accepted = true
                    }

                    Connections {
                        target: serviceRouter
                        function onActionTriggered(actionId, pressed, repeated) {
                            keySink.lastActionText = "Action: " + actionId + " pressed=" + pressed + " repeated=" + repeated
                        }
                    }

                    Text {
                        anchors.centerIn: parent
                        color: "#ffffff"
                        text: parent.lastKeyText.length
                            ? parent.lastKeyText
                            : (parent.lastActionText.length ? parent.lastActionText : "Focus here; use DPad/LStick/A/B")
                    }
                }
            }
        }
    }
}
