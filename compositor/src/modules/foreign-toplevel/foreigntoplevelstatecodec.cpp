// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "foreigntoplevelstatecodec.h"

#include "wayland-treeland-foreign-toplevel-manager-v1-server-protocol.h"

namespace {

void appendState(QByteArray &encoded, uint32_t state)
{
    encoded.append(reinterpret_cast<const char *>(&state), sizeof(state));
}

} // namespace

namespace ForeignToplevelStateCodec {

QByteArray encode(ForeignToplevelHandleV1::States states, uint32_t resourceVersion)
{
    QByteArray encoded;

    if (states.testFlag(ForeignToplevelHandleV1::State::Maximized))
        appendState(encoded, TREELAND_FOREIGN_TOPLEVEL_HANDLE_V1_STATE_MAXIMIZED);

    if (states.testFlag(ForeignToplevelHandleV1::State::Minimized))
        appendState(encoded, TREELAND_FOREIGN_TOPLEVEL_HANDLE_V1_STATE_MINIMIZED);

    if (states.testFlag(ForeignToplevelHandleV1::State::Activated))
        appendState(encoded, TREELAND_FOREIGN_TOPLEVEL_HANDLE_V1_STATE_ACTIVATED);

    if (states.testFlag(ForeignToplevelHandleV1::State::Fullscreen))
        appendState(encoded, TREELAND_FOREIGN_TOPLEVEL_HANDLE_V1_STATE_FULLSCREEN);

    if (resourceVersion >= 2 && states.testFlag(ForeignToplevelHandleV1::State::Attention)) {
        appendState(encoded, TREELAND_FOREIGN_TOPLEVEL_HANDLE_V1_STATE_ATTENTION);
    }

    return encoded;
}

} // namespace ForeignToplevelStateCodec
