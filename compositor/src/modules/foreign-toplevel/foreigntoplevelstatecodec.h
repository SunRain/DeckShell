// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "foreigntoplevelhandlev1.h"

#include <QByteArray>

#include <cstdint>

namespace ForeignToplevelStateCodec {

/// Encodes internal state flags using wire values supported by resourceVersion.
QByteArray encode(ForeignToplevelHandleV1::States states, uint32_t resourceVersion);

} // namespace ForeignToplevelStateCodec
