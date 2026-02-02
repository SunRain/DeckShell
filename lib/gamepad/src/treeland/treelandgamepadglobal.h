// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/qglobal.h>

#include <deckshell/deckgamepad/core/deckgamepad.h>

// Export macro for library symbols
#if defined(TREELAND_GAMEPAD_LIBRARY)
#  define TREELAND_GAMEPAD_EXPORT Q_DECL_EXPORT
#else
#  define TREELAND_GAMEPAD_EXPORT Q_DECL_IMPORT
#endif

namespace TreelandGamepad {
using deckshell::deckgamepad::GamepadAxis;
using deckshell::deckgamepad::GamepadButton;
using deckshell::deckgamepad::GamepadHatMask;
using deckshell::deckgamepad::DeckGamepadAxisEvent;
using deckshell::deckgamepad::DeckGamepadButtonEvent;
using deckshell::deckgamepad::DeckGamepadHatEvent;

} // namespace TreelandGamepad
