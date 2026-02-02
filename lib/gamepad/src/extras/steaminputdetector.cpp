// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/extras/steaminputdetector.h>

#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QProcess>
#include <QStandardPaths>
#include <QTextStream>

#include <errno.h>
#include <fcntl.h>
#include <unistd.h>

DECKGAMEPAD_BEGIN_NAMESPACE

SteamInputDetector::SteamInputDetector(QObject *parent)
    : QObject(parent)
    , m_detectTimer(new QTimer(this))
{
    connect(m_detectTimer, &QTimer::timeout, this, &SteamInputDetector::onAutoDetectTimer);
}

SteamInputDetector::~SteamInputDetector()
{
    if (m_detectTimer && m_detectTimer->isActive()) {
        m_detectTimer->stop();
    }
}

SteamInputDetector::DetectionResult SteamInputDetector::detectSteamInput()
{
    // 1) 检查 Steam 进程
    const bool steamRunning = isSteamProcessRunning();

    // 2) 检查 Steam 环境变量
    const bool steamEnv = hasSteamEnvironment();

    // 若两者都未命中，认为未运行
    if (!steamRunning && !steamEnv) {
        m_lastResult = NotDetected;
        Q_EMIT steamInputDetected(m_lastResult);
        return m_lastResult;
    }

    // Steam 运行中：进一步检查配置，判断是否可能启用 Input
    if (checkSteamConfig()) {
        m_lastResult = SteamInputActive;
        Q_EMIT conflictWarning(getConflictAdvice());
        Q_EMIT steamInputDetected(m_lastResult);
        return m_lastResult;
    }

    m_lastResult = SteamRunning;
    Q_EMIT steamInputDetected(m_lastResult);
    return m_lastResult;
}

bool SteamInputDetector::isSteamProcessRunning() const
{
    QDir procDir(QStringLiteral("/proc"));
    if (!procDir.exists()) {
        return false;
    }

    const QStringList steamProcs = getSteamProcessNames();
    const QFileInfoList entries = procDir.entryInfoList(QDir::Dirs | QDir::NoDotAndDotDot);

    for (const QFileInfo &entry : entries) {
        bool ok = false;
        const int pid = entry.fileName().toInt(&ok);
        if (!ok) {
            continue;
        }

        QFile cmdlineFile(QStringLiteral("/proc/%1/cmdline").arg(pid));
        if (!cmdlineFile.open(QIODevice::ReadOnly)) {
            continue;
        }

        QString cmdline = QString::fromLatin1(cmdlineFile.readAll());
        cmdline.replace(QLatin1Char('\0'), QLatin1Char(' '));

        for (const QString &procName : steamProcs) {
            if (cmdline.contains(procName, Qt::CaseInsensitive)) {
                return true;
            }
        }
    }

    return false;
}

bool SteamInputDetector::hasSteamEnvironment() const
{
    const QStringList steamEnvVars = {
        QStringLiteral("STEAM_RUNTIME"),
        QStringLiteral("STEAM_COMPAT_CLIENT_INSTALL_PATH"),
        QStringLiteral("SteamAppId"),
    };

    for (const QString &varName : steamEnvVars) {
        const QString value = readEnvironmentVariable(varName);
        if (!value.isEmpty()) {
            return true;
        }
    }

    return false;
}

bool SteamInputDetector::checkDeviceConflict(const QString &devicePath) const
{
    const int fd = open(devicePath.toUtf8().constData(), O_RDONLY | O_NONBLOCK);
    if (fd < 0) {
        return errno == EBUSY;
    }

    close(fd);
    return false;
}

QString SteamInputDetector::steamInstallPath() const
{
    const QString envPath = readEnvironmentVariable(QStringLiteral("STEAM_COMPAT_CLIENT_INSTALL_PATH"));
    if (!envPath.isEmpty() && QDir(envPath).exists()) {
        return envPath;
    }

    const QStringList paths = {
        QDir::homePath() + QStringLiteral("/.steam/steam"),
        QDir::homePath() + QStringLiteral("/.local/share/Steam"),
        QStringLiteral("/usr/share/steam"),
        QStringLiteral("/usr/local/share/steam"),
    };

    for (const QString &path : paths) {
        if (QDir(path).exists()) {
            return path;
        }
    }

    return {};
}

QStringList SteamInputDetector::steamProcesses() const
{
    if (!isSteamProcessRunning()) {
        return {};
    }

    QStringList foundProcesses;
    const QStringList steamProcs = getSteamProcessNames();

    QDir procDir(QStringLiteral("/proc"));
    if (!procDir.exists()) {
        return {};
    }

    const QFileInfoList entries = procDir.entryInfoList(QDir::Dirs | QDir::NoDotAndDotDot);
    for (const QFileInfo &entry : entries) {
        bool ok = false;
        const int pid = entry.fileName().toInt(&ok);
        if (!ok) {
            continue;
        }

        QFile cmdlineFile(QStringLiteral("/proc/%1/cmdline").arg(pid));
        if (!cmdlineFile.open(QIODevice::ReadOnly)) {
            continue;
        }

        QString cmdline = QString::fromLatin1(cmdlineFile.readAll());
        cmdline.replace(QLatin1Char('\0'), QLatin1Char(' '));

        for (const QString &procName : steamProcs) {
            if (cmdline.contains(procName, Qt::CaseInsensitive) && !foundProcesses.contains(procName)) {
                foundProcesses << procName;
            }
        }
    }

    return foundProcesses;
}

QString SteamInputDetector::detectionResultToString(DetectionResult result) const
{
    switch (result) {
    case NotDetected:
        return QStringLiteral("Not detected");
    case SteamRunning:
        return QStringLiteral("Steam running");
    case SteamInputActive:
        return QStringLiteral("Steam Input active");
    default:
        return QStringLiteral("Unknown");
    }
}

void SteamInputDetector::setAutoDetect(bool enable)
{
    if (m_autoDetect == enable) {
        return;
    }

    m_autoDetect = enable;

    if (!m_detectTimer) {
        return;
    }

    if (enable) {
        m_detectTimer->start(m_autoDetectInterval * 1000);
        detectSteamInput();
        return;
    }

    m_detectTimer->stop();
}

void SteamInputDetector::setAutoDetectInterval(int seconds)
{
    if (seconds < 10) {
        seconds = 10;
    }

    m_autoDetectInterval = seconds;

    if (m_detectTimer && m_detectTimer->isActive()) {
        m_detectTimer->stop();
        m_detectTimer->start(m_autoDetectInterval * 1000);
    }
}

int SteamInputDetector::autoDetectInterval() const
{
    return m_autoDetectInterval;
}

QString SteamInputDetector::getConflictAdvice() const
{
    switch (m_lastResult) {
    case NotDetected:
        return QStringLiteral("未检测到 Steam Input，DeckShell gamepad 功能可正常使用。");
    case SteamRunning:
        return QStringLiteral("检测到 Steam 运行中，但未确认 Steam Input 已启用。若出现冲突，请检查 Steam 控制器设置。");
    case SteamInputActive:
        return QStringLiteral(
            "检测到 Steam Input 可能处于启用状态，可能与 DeckShell 的 gamepad/键盘映射冲突。\n"
            "\n"
            "建议：\n"
            "1. 在 Steam 设置中关闭 Steam Input（Steam > 设置 > 控制器）。\n"
            "2. 若仅在 Steam 游戏内使用 Steam Input，请关闭 DeckShell 的键盘映射。\n"
            "3. 若希望系统级统一映射，请关闭 Steam Input，改用 DeckShell 配置。\n"
            "4. 如遇设备占用/权限问题，可查看 compositor 日志定位错误。");
    default:
        return {};
    }
}

void SteamInputDetector::onAutoDetectTimer()
{
    const DetectionResult oldResult = m_lastResult;
    const DetectionResult newResult = detectSteamInput();
    Q_UNUSED(oldResult);
    Q_UNUSED(newResult);
}

bool SteamInputDetector::checkProcess(const QString &processName) const
{
    QProcess process;
    process.start(QStringLiteral("pgrep"), QStringList() << QStringLiteral("-x") << processName);
    process.waitForFinished(1000);
    const QString output = QString::fromUtf8(process.readAllStandardOutput()).trimmed();
    return !output.isEmpty();
}

QString SteamInputDetector::readEnvironmentVariable(const QString &name) const
{
    return qEnvironmentVariable(name.toUtf8().constData());
}

bool SteamInputDetector::canOpenDevice(const QString &devicePath) const
{
    const int fd = open(devicePath.toUtf8().constData(), O_RDONLY | O_NONBLOCK);
    if (fd < 0) {
        return false;
    }
    close(fd);
    return true;
}

QStringList SteamInputDetector::getSteamProcessNames() const
{
    return {
        QStringLiteral("steam"),
        QStringLiteral("steamwebhelper"),
        QStringLiteral("reaper"),
        QStringLiteral("steaminput"),
        QStringLiteral("streaming_client"),
    };
}

bool SteamInputDetector::checkSteamConfig() const
{
    const QString steamPath = steamInstallPath();
    if (steamPath.isEmpty()) {
        return false;
    }

    const QString configPath = steamPath + QStringLiteral("/config/config.vdf");
    if (!QFile::exists(configPath)) {
        return false;
    }

    QFile configFile(configPath);
    if (!configFile.open(QIODevice::ReadOnly)) {
        return false;
    }

    QTextStream stream(&configFile);
    const QString content = stream.readAll();
    if (content.contains(QStringLiteral("SDL_GamepadBind"), Qt::CaseInsensitive)
        || content.contains(QStringLiteral("controller_config"), Qt::CaseInsensitive)) {
        return true;
    }

    return false;
}

DECKGAMEPAD_END_NAMESPACE

