// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// Action Mapping Profile：将标准化的 GamepadButton/GamepadAxis 映射为稳定 actionId（可持久化 JSON）。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QJsonObject>
#include <QtCore/QMap>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

struct DeckGamepadActionBinding {
    QString actionId; // 空字符串表示显式解绑
};

struct DeckGamepadAxisActionBinding {
    DeckGamepadActionBinding negative;
    bool hasNegative = false;

    DeckGamepadActionBinding positive;
    bool hasPositive = false;

    float threshold = 0.0f; // (0.0 - 1.0)
    bool hasThreshold = false;
};

struct DeckGamepadActionRepeatConfig {
    bool enabled = false;
    int delayMs = 350;
    int intervalMs = 80;
};

struct ActionMappingProfile {
    enum class NavigationPriority {
        DpadOverLeftStick = 0,
        LeftStickOverDpad,
    };

    // Source priority（仅影响“方向动作”决策：DPad vs LeftStick）
    NavigationPriority navigationPriority = NavigationPriority::DpadOverLeftStick;
    bool hasNavigationPriority = false;

    // Repeat（仅用于“方向动作”）
    DeckGamepadActionRepeatConfig repeat;
    bool hasRepeatConfig = false;

    // bindings
    QMap<GamepadButton, DeckGamepadActionBinding> buttonBindings;
    QMap<GamepadAxis, DeckGamepadAxisActionBinding> axisBindings;

    QJsonObject toJson() const;
    static ActionMappingProfile fromJson(const QJsonObject &obj);

    static ActionMappingProfile createNavigationPreset();
    void applyOverridesFrom(const ActionMappingProfile &overrides);

    static bool loadFromFile(const QString &path, ActionMappingProfile *outProfile, QString *errorMessage = nullptr);
};

DECKGAMEPAD_END_NAMESPACE

