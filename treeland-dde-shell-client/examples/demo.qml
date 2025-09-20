import QtQuick
import QtQuick.Window
import QtQuick.Controls
import DeckShell.ddeshellclient 1.0

Window {
    id: rootWindow
    width: 500
    height: 450
    visible: true
    title: "DDE Shell - QML Demo"

    // Using Attached Properties to configure DDE shell surface
    // This is the layer-shell-qt style QML integration!
    DShellClientSurface.skipMultitaskview: skipMultitaskCheckbox.checked
    DShellClientSurface.skipSwitcher: skipSwitcherCheckbox.checked
    DShellClientSurface.skipDockPreview: skipDockCheckbox.checked
    DShellClientSurface.acceptKeyboardFocus: acceptFocusCheckbox.checked
    DShellClientSurface.role: ShellSurface.Role.Overlay

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#e8f5e9" }
            GradientStop { position: 1.0; color: "#c8e6c9" }
        }

        Column {
            anchors.centerIn: parent
            spacing: 20
            width: parent.width - 80

            Text {
                text: "QML Demo - Declarative API"
                font.pixelSize: 20
                font.bold: true
                color: "#1b5e20"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: "Using Attached Properties (layer-shell-qt style)"
                font.pixelSize: 14
                color: "#2e7d32"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Rectangle {
                width: parent.width
                height: 1
                color: "#81c784"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            // Property controls
            GroupBox {
                title: "DDE Shell Properties"
                width: parent.width
                anchors.horizontalCenter: parent.horizontalCenter

                Column {
                    spacing: 15
                    width: parent.width

                    CheckBox {
                        id: skipMultitaskCheckbox
                        text: "Skip Multitask View"
                        checked: true
                        font.pixelSize: 13
                    }

                    CheckBox {
                        id: skipSwitcherCheckbox
                        text: "Skip Window Switcher"
                        checked: false
                        font.pixelSize: 13
                    }

                    CheckBox {
                        id: skipDockCheckbox
                        text: "Skip Dock Preview"
                        checked: false
                        font.pixelSize: 13
                    }

                    CheckBox {
                        id: acceptFocusCheckbox
                        text: "Accept Keyboard Focus"
                        checked: true
                        font.pixelSize: 13
                    }
                }
            }

            Text {
                text: "Properties update in real-time via QML bindings.\nNo imperative code needed!"
                font.pixelSize: 12
                font.italic: true
                color: "#388e3c"
                horizontalAlignment: Text.AlignHCenter
                width: parent.width
                wrapMode: Text.WordWrap
            }

            Button {
                text: "Read Current Properties"
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: {
                    console.log("=== DDE Shell Properties ===")
                    console.log("skipMultitaskview:", DShellClientSurface.skipMultitaskview)
                    console.log("skipSwitcher:", DShellClientSurface.skipSwitcher)
                    console.log("skipDockPreview:", DShellClientSurface.skipDockPreview)
                    console.log("acceptKeyboardFocus:", DShellClientSurface.acceptKeyboardFocus)
                }
            }
        }
    }

    Component.onCompleted: {
        console.log("QML Demo window created successfully!")
        console.log("Initial skipMultitaskview:", DShellClientSurface.skipMultitaskview)
    }
}
