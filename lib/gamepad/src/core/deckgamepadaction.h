// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// 统一 Action/Intent IR：稳定 actionId + press/release/repeat 事件模型。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QMetaType>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

namespace DeckGamepadActionId {
// 导航（基础模块）
inline constexpr char NavUp[] = "nav.up";
inline constexpr char NavDown[] = "nav.down";
inline constexpr char NavLeft[] = "nav.left";
inline constexpr char NavRight[] = "nav.right";
inline constexpr char NavAccept[] = "nav.accept";
inline constexpr char NavBack[] = "nav.back";
inline constexpr char NavMenu[] = "nav.menu";

// Tab（scope 切换 canonical）
inline constexpr char NavTabNext[] = "nav.tab.next";
inline constexpr char NavTabPrev[] = "nav.tab.prev";

// Page（迁移期别名）：历史上 `nav.page.*` 被用于 scope 切换，但语义更接近 `nav.tab.*`。
// - 保留常量用于兼容旧 consumer / 旧映射
// - 默认 preset 应仅输出 canonical `nav.tab.*`，避免与别名双触发
inline constexpr char NavPageNext[] = "nav.page.next";
inline constexpr char NavPagePrev[] = "nav.page.prev";

// 排障（诊断 suggestedActions）
inline constexpr char HelpFocusWindow[] = "help.focus_window";
inline constexpr char HelpRequestAuthorization[] = "help.request_authorization";
inline constexpr char HelpCheckPermissions[] = "help.check_permissions";
inline constexpr char HelpSwitchToActiveSession[] = "help.switch_to_active_session";
inline constexpr char HelpRetry[] = "help.retry";
inline constexpr char HelpDisableGrab[] = "help.disable_grab";
} // namespace DeckGamepadActionId

struct DeckGamepadActionEvent {
    QString actionId;
    bool pressed = false;
    bool repeated = false;
    int timeMs = 0;
};

DECKGAMEPAD_END_NAMESPACE

Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadActionEvent)
