// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// deckgamepad 运行期配置：提供路径策略与少量硬化开关，避免 core 绑定特定应用（如 DeckShell）运行环境假设。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QDir>
#include <QtCore/QFile>
#include <QtCore/QStandardPaths>
#include <QtCore/QString>
#include <QtCore/QStringList>

DECKGAMEPAD_BEGIN_NAMESPACE

// 设备访问策略：direct-open 为基础能力；logind/seatd 为可选增强（由后端按可用性探测）。
enum class DeckGamepadDeviceAccessMode {
    Auto = 0,
    DirectOpen,
    LogindTakeDevice,
};

// 采集门控策略：默认仅在 active session 采集（锁屏/切 VT/多会话下自动门控与恢复）。
enum class DeckGamepadCapturePolicy {
    ActiveSessionOnly = 0,
    Always,
};

// 设备抓取策略：EVIOCGRAB（独占）为可选，默认共享。
enum class DeckGamepadEvdevGrabMode {
    Shared = 0,
    Exclusive,
    Auto,
};

// Provider 选择：用于 DeckGamepadService 控制 evdev 分支的线程模型/调试回滚通道。
// 注意：当前实现下，Evdev/EvdevUdev 均由 EvdevProvider 承载：
// - Evdev：IO 线程模式（推荐，避免 I/O 拉慢 UI 线程）
// - EvdevUdev：单线程调试模式（行为接近历史 evdev-udev，便于排查/回归对比）
enum class DeckGamepadProviderSelection {
    Auto = 0, // follow build default selection
    EvdevUdev,
    Evdev,
};

struct DeckGamepadRuntimeConfig {
    // SDL GameController DB（gamecontrollerdb.txt）
    QString sdlDbPathOverride;
    QStringList sdlDbSearchPaths;

    // Custom mapping（custom_gamepad_mappings.txt）
    QString customMappingPathOverride;

    // Calibration data（calibration.json）
    QString calibrationPathOverride;

    // Action mapping profile（action_mapping_profile.json）
    // 用于“标准化输入（GamepadButton/GamepadAxis）→ 上层动作语义（actionId）”的直接可配置方案。
    QString actionMappingProfilePathOverride;

    // 兼容读取旧路径（例如历史上固定在 ~/.config/DeckShell/...）
    bool enableLegacyDeckShellPaths = true;
    QString legacyDataDirName = QStringLiteral("DeckShell");

    // 权限不足/短暂 I/O 异常时，是否启用自动重试（带退避，避免 busy loop）
    bool enableAutoRetryOpen = true;
    int retryBackoffMinMs = 2000;
    int retryBackoffMaxMs = 60000;

    // ========== 设备访问/会话门控/抓取 ==========
    DeckGamepadDeviceAccessMode deviceAccessMode = DeckGamepadDeviceAccessMode::Auto;
    DeckGamepadCapturePolicy capturePolicy = DeckGamepadCapturePolicy::ActiveSessionOnly;
    DeckGamepadEvdevGrabMode grabMode = DeckGamepadEvdevGrabMode::Shared;

    // ========== Provider 选择/回滚通道 ==========
    // Auto：使用构建期默认选择（见 CMake: DECKGAMEPAD_DEFAULT_PROVIDER）。
    // 仅在 DeckGamepadService “自动选择 provider”模式下生效；手动 setProvider() 的场景会忽略该字段。
    DeckGamepadProviderSelection providerSelection = DeckGamepadProviderSelection::Auto;

    // ========== compositor/转发相关 ==========
    // axis/hat 高频事件整形（默认关闭）。>0 时按窗口合并（仅 axis/hat；button 不合并）。
    int axisCoalesceIntervalMs = 0;
    int hatCoalesceIntervalMs = 0;

    QString defaultCustomMappingPath() const
    {
        const QString configDir = QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation);
        return QDir(configDir).filePath(QStringLiteral("custom_gamepad_mappings.txt"));
    }

    QString defaultCalibrationPath() const
    {
        const QString configDir = QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation);
        return QDir(configDir).filePath(QStringLiteral("calibration.json"));
    }

    QString defaultActionMappingProfilePath() const
    {
        const QString configDir = QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation);
        return QDir(configDir).filePath(QStringLiteral("action_mapping_profile.json"));
    }

    QString legacyConfigDir() const
    {
        const QString configHome = QStandardPaths::writableLocation(QStandardPaths::ConfigLocation);
        return QDir(configHome).filePath(legacyDataDirName);
    }

    QString legacySdlDbPath() const
    {
        return QDir(legacyConfigDir()).filePath(QStringLiteral("gamecontrollerdb.txt"));
    }

    QString legacyCustomMappingPath() const
    {
        return QDir(legacyConfigDir()).filePath(QStringLiteral("custom_gamepad_mappings.txt"));
    }

    QString legacyCalibrationPath() const
    {
        return QDir(legacyConfigDir()).filePath(QStringLiteral("calibration.json"));
    }

    QString legacyActionMappingProfilePath() const
    {
        return QDir(legacyConfigDir()).filePath(QStringLiteral("action_mapping_profile.json"));
    }

    QStringList defaultSdlDbSearchPaths() const
    {
        // 默认搜索路径同时兼容：
        // - 新的独立项目安装目录（DeckShellGamepad）
        // - 历史 DeckShell 安装目录与用户目录（legacy）
        //
        // 上层可通过 sdlDbSearchPaths/override 覆盖。
        const QString installedDataDirName = QStringLiteral("DeckShellGamepad");
        return {
            legacySdlDbPath(),
            QStringLiteral("/usr/share/") + installedDataDirName + QStringLiteral("/gamecontrollerdb.txt"),
            QStringLiteral("/usr/local/share/") + installedDataDirName + QStringLiteral("/gamecontrollerdb.txt"),
            QStringLiteral("/usr/share/") + legacyDataDirName + QStringLiteral("/gamecontrollerdb.txt"),
            QStringLiteral("/usr/local/share/") + legacyDataDirName + QStringLiteral("/gamecontrollerdb.txt"),
        };
    }

    QString resolveSdlDbPath() const
    {
        if (!sdlDbPathOverride.isEmpty() && QFile::exists(sdlDbPathOverride)) {
            return sdlDbPathOverride;
        }

        const QByteArray envPath = qgetenv("SDL_GAMECONTROLLERCONFIG_FILE");
        if (!envPath.isEmpty()) {
            const QString path = QString::fromUtf8(envPath);
            if (QFile::exists(path)) {
                return path;
            }
        }

        const QStringList searchPaths = !sdlDbSearchPaths.isEmpty()
            ? sdlDbSearchPaths
            : (enableLegacyDeckShellPaths ? defaultSdlDbSearchPaths() : QStringList{});

        for (const QString &path : searchPaths) {
            if (!path.isEmpty() && QFile::exists(path)) {
                return path;
            }
        }

        return QString{};
    }

    QString resolveCustomMappingPath() const
    {
        if (!customMappingPathOverride.isEmpty()) {
            return customMappingPathOverride;
        }
        return defaultCustomMappingPath();
    }

    QString resolveCalibrationPath() const
    {
        if (!calibrationPathOverride.isEmpty()) {
            return calibrationPathOverride;
        }
        return defaultCalibrationPath();
    }

    // 注意：profile 属于“可选输入文件”，仅当文件存在时返回路径；否则视为未配置（回退默认 preset）。
    QString resolveActionMappingProfilePath() const
    {
        if (!actionMappingProfilePathOverride.isEmpty() && QFile::exists(actionMappingProfilePathOverride)) {
            return actionMappingProfilePathOverride;
        }

        const QString defaultPath = defaultActionMappingProfilePath();
        if (!defaultPath.isEmpty() && QFile::exists(defaultPath)) {
            return defaultPath;
        }

        if (enableLegacyDeckShellPaths) {
            const QString legacyPath = legacyActionMappingProfilePath();
            if (!legacyPath.isEmpty() && QFile::exists(legacyPath)) {
                return legacyPath;
            }
        }

        return QString{};
    }
};

DECKGAMEPAD_END_NAMESPACE

Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadRuntimeConfig)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadDeviceAccessMode)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadCapturePolicy)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadEvdevGrabMode)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadProviderSelection)
