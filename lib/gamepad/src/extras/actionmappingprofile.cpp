// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "actionmappingprofile.h"

#include <deckshell/deckgamepad/core/deckgamepadaction.h>

#include <QtCore/QFile>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonValue>

DECKGAMEPAD_BEGIN_NAMESPACE

static DeckGamepadActionBinding bindingFromJsonValue(const QJsonValue &value)
{
    DeckGamepadActionBinding binding;

    if (value.isString()) {
        binding.actionId = value.toString();
        return binding;
    }

    if (value.isObject()) {
        const QJsonObject obj = value.toObject();
        binding.actionId = obj.value(QStringLiteral("action_id")).toString();
        if (binding.actionId.isEmpty()) {
            binding.actionId = obj.value(QStringLiteral("actionId")).toString();
        }
        return binding;
    }

    // null/undefined/other: treat as explicit unbind
    binding.actionId = QString{};
    return binding;
}

static QJsonValue bindingToJsonValue(const DeckGamepadActionBinding &binding)
{
    // 简化输出：以字符串为主（空字符串表示显式解绑）
    return QJsonValue(binding.actionId);
}

QJsonObject ActionMappingProfile::toJson() const
{
    QJsonObject root;
    root[QStringLiteral("version")] = QStringLiteral("1.0");

    if (hasNavigationPriority) {
        const char *priority = "dpad_over_left_stick";
        if (navigationPriority == NavigationPriority::LeftStickOverDpad) {
            priority = "left_stick_over_dpad";
        }
        root[QStringLiteral("navigation_priority")] = QString::fromLatin1(priority);
    }

    if (hasRepeatConfig) {
        QJsonObject repeatObj;
        repeatObj[QStringLiteral("enabled")] = repeat.enabled;
        repeatObj[QStringLiteral("delay_ms")] = repeat.delayMs;
        repeatObj[QStringLiteral("interval_ms")] = repeat.intervalMs;
        root[QStringLiteral("repeat")] = repeatObj;
    }

    QJsonObject buttonObj;
    for (auto it = buttonBindings.constBegin(); it != buttonBindings.constEnd(); ++it) {
        const QString key = QString::number(static_cast<int>(it.key()));
        buttonObj[key] = bindingToJsonValue(it.value());
    }
    root[QStringLiteral("button_bindings")] = buttonObj;

    QJsonObject axisObj;
    for (auto it = axisBindings.constBegin(); it != axisBindings.constEnd(); ++it) {
        const QString key = QString::number(static_cast<int>(it.key()));

        QJsonObject entry;
        if (it.value().hasNegative) {
            entry[QStringLiteral("negative")] = bindingToJsonValue(it.value().negative);
        }
        if (it.value().hasPositive) {
            entry[QStringLiteral("positive")] = bindingToJsonValue(it.value().positive);
        }
        if (it.value().hasThreshold) {
            entry[QStringLiteral("threshold")] = it.value().threshold;
        }

        axisObj[key] = entry;
    }
    root[QStringLiteral("axis_bindings")] = axisObj;

    return root;
}

ActionMappingProfile ActionMappingProfile::fromJson(const QJsonObject &obj)
{
    ActionMappingProfile profile;

    if (obj.contains(QStringLiteral("navigation_priority"))) {
        profile.hasNavigationPriority = true;
        const QString v = obj.value(QStringLiteral("navigation_priority")).toString();
        if (v == QLatin1String("left_stick_over_dpad")) {
            profile.navigationPriority = NavigationPriority::LeftStickOverDpad;
        } else {
            profile.navigationPriority = NavigationPriority::DpadOverLeftStick;
        }
    }

    const QJsonValue repeatValue = obj.value(QStringLiteral("repeat"));
    if (repeatValue.isObject()) {
        profile.hasRepeatConfig = true;
        const QJsonObject repeatObj = repeatValue.toObject();
        profile.repeat.enabled = repeatObj.value(QStringLiteral("enabled")).toBool(false);
        profile.repeat.delayMs = repeatObj.value(QStringLiteral("delay_ms")).toInt(350);
        profile.repeat.intervalMs = repeatObj.value(QStringLiteral("interval_ms")).toInt(80);
    }

    const QJsonObject buttonsObj = obj.value(QStringLiteral("button_bindings")).toObject();
    for (const QString &key : buttonsObj.keys()) {
        bool ok = false;
        const int buttonInt = key.toInt(&ok);
        if (!ok) {
            continue;
        }
        if (buttonInt < 0 || buttonInt >= GAMEPAD_BUTTON_MAX) {
            continue;
        }
        const GamepadButton button = static_cast<GamepadButton>(buttonInt);
        profile.buttonBindings[button] = bindingFromJsonValue(buttonsObj.value(key));
    }

    const QJsonObject axisBindingsObj = obj.value(QStringLiteral("axis_bindings")).toObject();
    for (const QString &key : axisBindingsObj.keys()) {
        bool ok = false;
        const int axisInt = key.toInt(&ok);
        if (!ok) {
            continue;
        }
        if (axisInt < 0 || axisInt >= GAMEPAD_AXIS_MAX) {
            continue;
        }

        const QJsonObject entry = axisBindingsObj.value(key).toObject();
        DeckGamepadAxisActionBinding binding;

        if (entry.contains(QStringLiteral("negative"))) {
            binding.hasNegative = true;
            binding.negative = bindingFromJsonValue(entry.value(QStringLiteral("negative")));
        }
        if (entry.contains(QStringLiteral("positive"))) {
            binding.hasPositive = true;
            binding.positive = bindingFromJsonValue(entry.value(QStringLiteral("positive")));
        }
        if (entry.contains(QStringLiteral("threshold"))) {
            binding.hasThreshold = true;
            binding.threshold = static_cast<float>(entry.value(QStringLiteral("threshold")).toDouble(0.0));
        }

        const GamepadAxis axis = static_cast<GamepadAxis>(axisInt);
        profile.axisBindings[axis] = binding;
    }

    return profile;
}

ActionMappingProfile ActionMappingProfile::createNavigationPreset()
{
    ActionMappingProfile profile;
    profile.hasNavigationPriority = true;
    profile.navigationPriority = NavigationPriority::DpadOverLeftStick;

    // DPad
    profile.buttonBindings[GAMEPAD_BUTTON_DPAD_UP].actionId = QString::fromLatin1(DeckGamepadActionId::NavUp);
    profile.buttonBindings[GAMEPAD_BUTTON_DPAD_DOWN].actionId = QString::fromLatin1(DeckGamepadActionId::NavDown);
    profile.buttonBindings[GAMEPAD_BUTTON_DPAD_LEFT].actionId = QString::fromLatin1(DeckGamepadActionId::NavLeft);
    profile.buttonBindings[GAMEPAD_BUTTON_DPAD_RIGHT].actionId = QString::fromLatin1(DeckGamepadActionId::NavRight);

    // Buttons
    profile.buttonBindings[GAMEPAD_BUTTON_A].actionId = QString::fromLatin1(DeckGamepadActionId::NavAccept);
    profile.buttonBindings[GAMEPAD_BUTTON_B].actionId = QString::fromLatin1(DeckGamepadActionId::NavBack);
    profile.buttonBindings[GAMEPAD_BUTTON_START].actionId = QString::fromLatin1(DeckGamepadActionId::NavMenu);
    profile.buttonBindings[GAMEPAD_BUTTON_L1].actionId = QString::fromLatin1(DeckGamepadActionId::NavTabPrev);
    profile.buttonBindings[GAMEPAD_BUTTON_R1].actionId = QString::fromLatin1(DeckGamepadActionId::NavTabNext);

    // Left stick → directions（threshold 作为 release 阈值；press 阈值由 mapper 的 hysteresis 决定）
    {
        DeckGamepadAxisActionBinding x;
        x.hasNegative = true;
        x.negative.actionId = QString::fromLatin1(DeckGamepadActionId::NavLeft);
        x.hasPositive = true;
        x.positive.actionId = QString::fromLatin1(DeckGamepadActionId::NavRight);
        profile.axisBindings[GAMEPAD_AXIS_LEFT_X] = x;
    }
    {
        DeckGamepadAxisActionBinding y;
        y.hasNegative = true;
        y.negative.actionId = QString::fromLatin1(DeckGamepadActionId::NavUp);
        y.hasPositive = true;
        y.positive.actionId = QString::fromLatin1(DeckGamepadActionId::NavDown);
        profile.axisBindings[GAMEPAD_AXIS_LEFT_Y] = y;
    }

    return profile;
}

void ActionMappingProfile::applyOverridesFrom(const ActionMappingProfile &overrides)
{
    if (overrides.hasNavigationPriority) {
        navigationPriority = overrides.navigationPriority;
        hasNavigationPriority = true;
    }

    if (overrides.hasRepeatConfig) {
        repeat = overrides.repeat;
        hasRepeatConfig = true;
    }

    // buttons：显式覆盖（空字符串表示解绑）
    for (auto it = overrides.buttonBindings.constBegin(); it != overrides.buttonBindings.constEnd(); ++it) {
        buttonBindings[it.key()] = it.value();
    }

    // axis：按字段覆盖（空字符串表示解绑）
    for (auto it = overrides.axisBindings.constBegin(); it != overrides.axisBindings.constEnd(); ++it) {
        auto &dst = axisBindings[it.key()];
        const auto &src = it.value();
        if (src.hasThreshold) {
            dst.threshold = src.threshold;
            dst.hasThreshold = true;
        }
        if (src.hasNegative) {
            dst.negative = src.negative;
            dst.hasNegative = true;
        }
        if (src.hasPositive) {
            dst.positive = src.positive;
            dst.hasPositive = true;
        }
    }
}

bool ActionMappingProfile::loadFromFile(const QString &path, ActionMappingProfile *outProfile, QString *errorMessage)
{
    if (!outProfile) {
        if (errorMessage) {
            *errorMessage = QStringLiteral("outProfile is null");
        }
        return false;
    }

    QFile file(path);
    if (!file.exists()) {
        if (errorMessage) {
            *errorMessage = QStringLiteral("file not found: %1").arg(path);
        }
        return false;
    }
    if (!file.open(QIODevice::ReadOnly)) {
        if (errorMessage) {
            *errorMessage = QStringLiteral("failed to open file: %1").arg(path);
        }
        return false;
    }

    QJsonParseError parseError;
    const QJsonDocument doc = QJsonDocument::fromJson(file.readAll(), &parseError);
    if (parseError.error != QJsonParseError::NoError || doc.isNull() || !doc.isObject()) {
        if (errorMessage) {
            *errorMessage = QStringLiteral("invalid json: %1 (%2)")
                .arg(path, parseError.errorString());
        }
        return false;
    }

    *outProfile = ActionMappingProfile::fromJson(doc.object());
    return true;
}

DECKGAMEPAD_END_NAMESPACE
