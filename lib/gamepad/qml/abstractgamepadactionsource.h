// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtQml/qqml.h>

// QML 侧 action 触发统一抽象：用于在属性类型层面约束信号形态，
// 并启用类型安全的 connect（替代 QObject* + 字符串 connect）。
class AbstractGamepadActionSource : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    QML_UNCREATABLE("Abstract base type; use ServiceActionRouter or GamepadActionRouter")

public:
    explicit AbstractGamepadActionSource(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

Q_SIGNALS:
    void actionTriggered(const QString &actionId, bool pressed, bool repeated);
};

