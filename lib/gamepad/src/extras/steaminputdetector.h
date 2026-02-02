// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QObject>
#include <QString>
#include <QStringList>
#include <QTimer>

DECKGAMEPAD_BEGIN_NAMESPACE

/**
 * @brief Steam Input 冲突检测器
 *
 * 用于检测 Steam/Steam Input 是否处于运行状态，从而提示可能与 DeckShell 的
 * gamepad/keyboard mapping 等功能产生冲突。
 *
 * 说明：
 * - 该类只做“检测与提示”，不做任何系统级干预。
 * - 自动检测默认关闭；开启后会以定时器间隔执行检测并发出信号。
 */
class DECKGAMEPAD_EXPORT SteamInputDetector : public QObject
{
    Q_OBJECT

public:
    enum DetectionResult {
        NotDetected = 0,      ///< 未检测到 Steam
        SteamRunning = 1,     ///< Steam 运行中，但未确认 Input 激活
        SteamInputActive = 2  ///< 检测到 Steam Input 可能处于激活状态（潜在冲突）
    };
    Q_ENUM(DetectionResult)

    explicit SteamInputDetector(QObject *parent = nullptr);
    ~SteamInputDetector() override;

    // ========== 检测接口 ==========

    /**
     * @brief 执行一次完整检测
     */
    DetectionResult detectSteamInput();

    bool isSteamProcessRunning() const;
    bool hasSteamEnvironment() const;

    /**
     * @brief 检测设备节点是否被占用（EBUSY）
     */
    bool checkDeviceConflict(const QString &devicePath) const;

    // ========== 信息接口 ==========

    QString steamInstallPath() const;
    QStringList steamProcesses() const;
    QString detectionResultToString(DetectionResult result) const;

    // ========== 配置 ==========

    void setAutoDetect(bool enable);
    bool isAutoDetectEnabled() const { return m_autoDetect; }
    void setAutoDetectInterval(int seconds);
    int autoDetectInterval() const;

    // ========== 建议 ==========

    QString getConflictAdvice() const;

Q_SIGNALS:
    void steamInputDetected(DetectionResult result);
    void conflictWarning(const QString &message);

private Q_SLOTS:
    void onAutoDetectTimer();

private:
    bool m_autoDetect = false;
    int m_autoDetectInterval = 30; // seconds

    DetectionResult m_lastResult = NotDetected;
    QTimer *m_detectTimer = nullptr;

    bool checkProcess(const QString &processName) const;
    QString readEnvironmentVariable(const QString &name) const;
    bool canOpenDevice(const QString &devicePath) const;
    QStringList getSteamProcessNames() const;
    bool checkSteamConfig() const;
};

DECKGAMEPAD_END_NAMESPACE

