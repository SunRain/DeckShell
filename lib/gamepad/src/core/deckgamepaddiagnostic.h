// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// 结构化诊断契约：使用稳定 key 供 UI/自动化测试断言，details 仅作为辅助上下文（可变）。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QMetaType>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QVariantMap>

DECKGAMEPAD_BEGIN_NAMESPACE

namespace DeckGamepadDiagnosticKey {
inline constexpr char PermissionDenied[] = "deckgamepad.permission.denied";
inline constexpr char SessionInactive[] = "deckgamepad.session.inactive";
inline constexpr char LogindUnavailable[] = "deckgamepad.logind.unavailable";
inline constexpr char DeviceBusy[] = "deckgamepad.device.busy";
inline constexpr char DeviceGrabFailed[] = "deckgamepad.device.grab_failed";
inline constexpr char WaylandFocusGated[] = "deckgamepad.wayland.focus_gated";
inline constexpr char WaylandNotAuthorized[] = "deckgamepad.wayland.not_authorized";
} // namespace DeckGamepadDiagnosticKey

struct DeckGamepadDiagnostic {
    QString key;            // 稳定诊断 key（空表示 OK）
    QVariantMap details;    // 可变上下文（脱敏）
    QStringList suggestedActions; // 建议动作（稳定 actionId 集合）

    bool isOk() const { return key.isEmpty(); }
};

DECKGAMEPAD_END_NAMESPACE

Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadDiagnostic)

