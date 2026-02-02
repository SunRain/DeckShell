// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// 手柄统一错误模型（结构化诊断契约）：用于 Provider/Service 对外稳定暴露可解释错误。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QMetaType>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

enum class DeckGamepadDeviceAvailability {
    Available = 0,
    Unavailable,
    Removed,
};

enum class DeckGamepadErrorCode {
    None = 0,
    PermissionDenied,
    Io,
    InvalidConfig,
    BackendStartFailed,
    NotSupported,
    Unknown,
};

// 对外稳定的错误语义（用于上层做一致降级/提示，避免绑定到实现细节）。
enum class DeckGamepadErrorKind {
    None = 0,
    Denied,
    Unsupported,
    Unavailable,
    InvalidConfig,
    Io,
    Unknown,
};

inline DeckGamepadErrorKind deckGamepadErrorKindFromCode(DeckGamepadErrorCode code)
{
    switch (code) {
    case DeckGamepadErrorCode::None:
        return DeckGamepadErrorKind::None;
    case DeckGamepadErrorCode::PermissionDenied:
        return DeckGamepadErrorKind::Denied;
    case DeckGamepadErrorCode::NotSupported:
        return DeckGamepadErrorKind::Unsupported;
    case DeckGamepadErrorCode::BackendStartFailed:
        return DeckGamepadErrorKind::Unavailable;
    case DeckGamepadErrorCode::InvalidConfig:
        return DeckGamepadErrorKind::InvalidConfig;
    case DeckGamepadErrorCode::Io:
        return DeckGamepadErrorKind::Io;
    case DeckGamepadErrorCode::Unknown:
    default:
        return DeckGamepadErrorKind::Unknown;
    }
}

struct DeckGamepadError {
    DeckGamepadErrorCode code = DeckGamepadErrorCode::None;
    QString message;
    int sysErrno = 0;
    QString context;
    QString hint;
    bool recoverable = false;

    bool isOk() const { return code == DeckGamepadErrorCode::None; }
    DeckGamepadErrorKind kind() const { return deckGamepadErrorKindFromCode(code); }
};

DECKGAMEPAD_END_NAMESPACE

Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadError)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadErrorCode)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadErrorKind)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadDeviceAvailability)
