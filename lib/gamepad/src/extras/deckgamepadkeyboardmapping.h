// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QObject>
#include <QHash>
#include <QJsonObject>

DECKGAMEPAD_BEGIN_NAMESPACE

// 复用 deckgamepad.h 中的 GamepadButton/GamepadAxis，不重复定义。

// 单个按键的键盘映射配置。
struct KeyMapping {
    int qtKey; // Qt::Key_*
    int modifiers; // Qt::KeyboardModifier
    QString description; // 展示用途

    KeyMapping() : qtKey(0), modifiers(0) {}
    KeyMapping(int k, int m = 0, const QString &desc = QString())
        : qtKey(k), modifiers(m), description(desc) {}

    bool isValid() const { return qtKey != 0; }

    QJsonObject toJson() const;
    static KeyMapping fromJson(const QJsonObject &obj);
};

// 轴映射（双向：负向/正向各一组按键）。
struct AxisKeyMapping {
    KeyMapping negative;
    KeyMapping positive;
    float threshold; // (0.0-1.0)

    AxisKeyMapping() : threshold(0.5f) {}

    QJsonObject toJson() const;
    static AxisKeyMapping fromJson(const QJsonObject &obj);
};

// 将手柄输入映射为键盘事件信号（本类不负责实际注入）。
class DeckGamepadKeyboardMappingManager : public QObject
{
    Q_OBJECT

public:
    explicit DeckGamepadKeyboardMappingManager(QObject *parent = nullptr);
    ~DeckGamepadKeyboardMappingManager() override;

    // 启用/禁用

    bool isEnabled() const { return m_enabled; }
    void setEnabled(bool enabled);

    // 按键映射

    void setButtonMapping(GamepadButton button, const KeyMapping &key);
    KeyMapping buttonMapping(GamepadButton button) const;
    void clearButtonMapping(GamepadButton button);

    // 轴映射

    void setAxisMapping(GamepadAxis axis, const AxisKeyMapping &keys);
    AxisKeyMapping axisMapping(GamepadAxis axis) const;
    void clearAxisMapping(GamepadAxis axis);

    // 输入处理：若存在映射则发出 keyEvent。
    void processButton(GamepadButton button, bool pressed);

    // 输入处理：跨越阈值时触发（按下/释放）。
    void processAxis(GamepadAxis axis, float value);

    // 预设模板

    void applyWASDPreset();
    void applyArrowPreset();
    void applyNumpadPreset();

    void clearAll();

    // 序列化

    QJsonObject toJson() const;
    bool fromJson(const QJsonObject &obj);

    bool saveToFile(const QString &path) const;
    bool loadFromFile(const QString &path);

Q_SIGNALS:
    void keyEvent(int qtKey, int modifiers, bool pressed);

    void enabledChanged(bool enabled);
    void mappingChanged();

private:
    void emitKeyEvent(const KeyMapping &mapping, bool pressed);
    QString buttonToString(GamepadButton button) const;
    QString axisToString(GamepadAxis axis) const;

    bool m_enabled;

    QHash<GamepadButton, KeyMapping> m_buttonMappings;

    QHash<GamepadAxis, AxisKeyMapping> m_axisMappings;

    // 记录当前轴方向状态，用于检测阈值跨越。
    struct AxisState {
        bool negativeActive = false;
        bool positiveActive = false;
    };
    QHash<GamepadAxis, AxisState> m_axisStates;
};

DECKGAMEPAD_END_NAMESPACE
