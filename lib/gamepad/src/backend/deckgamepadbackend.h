// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

/*
 * 参考 qtgamepad 的 linux 实现
 * 以及 Godot 4.0 的 joypad_linux
 */

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>
#include <deckshell/deckgamepad/core/deckgamepaderror.h>
#include <deckshell/deckgamepad/core/deckgamepaddeviceinfo.h>
#include <deckshell/deckgamepad/core/deckgamepadruntimeconfig.h>
#include <deckshell/deckgamepad/mapping/deckgamepadmapping.h>

#include <QtCore/QObject>
#include <QtCore/QSocketNotifier>
#include <QtCore/QHash>
#include <QtCore/QTimer>
#include <QtCore/QString>

#include <array>
#include <functional>
#include <memory>

extern "C" {
struct udev;
struct udev_monitor;
struct udev_device;
struct input_absinfo;
}

DECKGAMEPAD_BEGIN_NAMESPACE

class DeckGamepadSdlControllerDb;
class JsonCalibrationStore;
struct CalibrationData;
class DeviceAccessBroker;
class SessionGate;

class DECKGAMEPAD_EXPORT DeckGamepadDevice : public QObject
{
    Q_OBJECT
    friend class DeckGamepadBackend; // 允许后端访问私有成员

public:
    explicit DeckGamepadDevice(int id,
                               const QString &devpath,
                               DeckGamepadSdlControllerDb *sdlDb = nullptr,
                               QObject *parent = nullptr);
    ~DeckGamepadDevice();

    int deviceId() const { return m_id; }
    QString devicePath() const { return m_devpath; }
    QString name() const { return m_name; }
    QString guid() const { return m_guid; }
    bool isConnected() const { return m_fd != -1; }
    bool supportsRumble() const { return m_hasFF; }

    // SDL 映射信息
    bool hasSdlMapping() const { return m_deviceMapping.isValid(); }
    QString mappingName() const { return m_deviceMapping.name; }

    // 物理键/轴映射（用于自定义映射编辑）
    const QHash<int, int> &physicalButtonMap() const { return m_physicalButtonMap; }
    const QHash<int, int> &physicalAxisMap() const { return m_physicalAxisMap; }

    bool open();
    // fd 由调用方提供；releaseDevice 在 close() 时调用（用于归还 broker 持有的资源）。
    bool openWithFd(int fd, std::function<void()> releaseDevice = {});
    void close();
    void closeForIoError();

    // 重新从 SDL DB 读取并应用映射（用于自定义映射变更后）。
    void reloadMapping();

Q_SIGNALS:
    void buttonEvent(int deviceId, DeckGamepadButtonEvent event);
    void axisEvent(int deviceId, DeckGamepadAxisEvent event);
    void hatEvent(int deviceId, DeckGamepadHatEvent event);
    void disconnected(int deviceId);

private Q_SLOTS:
    void handleReadyRead();

private:
    enum {
        MAX_ABS = 63,
        MAX_KEY = 767,
        JOY_AXIS_COUNT = 6,
    };

    struct AxisInfo {
        int min = 0;
        int max = 0;
        int flat = 0; // Deadzone
    };

    void setupDevice();
    void setupSdlMapping();
    void processEvents();
    double normalizeAxisValue(int code, int value);
    GamepadButton mapButton(int evdev_code) const;
    GamepadAxis mapAxis(int evdev_code) const;
    bool isAxisInverted(int evdev_code) const;

    // 高级功能（轴调参/振动）
    bool startVibration(float weakMagnitude, float strongMagnitude, int duration_ms);
    void stopVibration();

    int m_id;
    QString m_devpath;
    QString m_name;
    QString m_guid;
    int m_fd;

    QSocketNotifier *m_notifier;
    
    // SDL 映射支持
    DeckGamepadSdlControllerDb *m_sdlDb;
    DeviceMapping m_deviceMapping;
    QHash<int, int> m_physicalButtonMap; // evdev code → SDL button index
    QHash<int, int> m_physicalAxisMap;   // evdev code → SDL axis index

    // 按键映射：evdev code -> gamepad button index
    int m_keyMap[MAX_KEY];

    // 轴信息（归一化）
    AxisInfo m_absInfo[MAX_ABS];

    // 当前 HAT 状态
    std::array<int, 4> m_hatXByHat{};
    std::array<int, 4> m_hatYByHat{};

    // 半轴（+a/-a）数字化状态：evdev axis code -> {-1,0,1}
    QHash<int, int> m_halfAxisStateByCode;

    // 力反馈
    bool m_hasFF;
    int m_ffEffectId;

    std::function<void()> m_releaseDevice;

    // 轴设置（axis -> deadzone/sensitivity）
    QHash<uint32_t, float> m_customDeadzones;
    QHash<uint32_t, float> m_axisSensitivity;

    const CalibrationData *m_calibrationData = nullptr;
};

class DECKGAMEPAD_EXPORT DeckGamepadBackend : public QObject
{
    Q_OBJECT
    friend class DeckGamepadBackendTestHooks;

public:
    // Legacy singleton入口：历史上用于直接访问 backend。
    // 推荐路径：使用 DeckGamepadService + IDeckGamepadProvider（支持 provider 选择/回滚与线程化演进）。
    static DeckGamepadBackend *instance();

    explicit DeckGamepadBackend(QObject *parent = nullptr);
    ~DeckGamepadBackend();

    void setRuntimeConfig(const DeckGamepadRuntimeConfig &config);
    DeckGamepadRuntimeConfig runtimeConfig() const;

    bool start();
    void stop();

    DeckGamepadError lastError() const;

    QList<int> knownGamepads() const;
    QList<int> connectedGamepads() const;
    DeckGamepadDevice *device(int id) const;
    DeckGamepadDeviceInfo deviceInfo(int deviceId) const;
    QString deviceUid(int deviceId) const;

    DeckGamepadDeviceAvailability deviceAvailability(int deviceId) const;
    DeckGamepadError deviceLastError(int deviceId) const;

    // 高级功能：轴设置
    void setAxisDeadzone(int deviceId, uint32_t axis, float deadzone);
    void setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity);
    void resetAxisSettings(int deviceId, uint32_t axis);

    // 高级功能：振动
    bool startVibration(int deviceId,
                        float weakMagnitude,
                        float strongMagnitude,
                        int duration_ms = 1000);
    void stopVibration(int deviceId);

    // SDL GameController DB
    DeckGamepadSdlControllerDb *sdlDb() const { return m_sdlDb; }
    int reloadSdlDb(const QString &path = QString());
    int sdlMappingCount() const;

    // 自定义映射管理器
    class DeckGamepadCustomMappingManager *customMappingManager() const
    {
        return m_customMappingMgr;
    }

Q_SIGNALS:
    void lastErrorChanged(DeckGamepadError error);
    void deviceInfoChanged(int deviceId, DeckGamepadDeviceInfo info);
    void deviceAvailabilityChanged(int deviceId, DeckGamepadDeviceAvailability availability);
    void deviceErrorChanged(int deviceId, DeckGamepadError error);

    void gamepadConnected(int deviceId, const QString &name);
    void gamepadDisconnected(int deviceId);
    void buttonEvent(int deviceId, DeckGamepadButtonEvent event);
    void axisEvent(int deviceId, DeckGamepadAxisEvent event);
    void hatEvent(int deviceId, DeckGamepadHatEvent event);
    void sdlDatabaseLoaded(int count);

private Q_SLOTS:
    void handleUdevEvent();
    void retryUnavailableDevices();
    void handleSessionGateActiveChanged(bool active);

private:
    struct KnownDevice {
        QString devpath;
        DeckGamepadDeviceInfo info;
        DeckGamepadDeviceAvailability availability = DeckGamepadDeviceAvailability::Unavailable;
        DeckGamepadError lastError;
        int retryAttempt = 0;
        qint64 nextRetryWallclockMs = 0;
    };

    void probeGamepads();
    bool isGamepadUdevDevice(struct udev_device *dev) const;
    QString udevDeviceName(struct udev_device *dev) const;
    bool isGamepadDevice(const QString &devpath, int *openErrno = nullptr);
    void openGamepad(struct udev_device *dev, const QString &devpath);
    bool tryOpenGamepad(int deviceId, const QString &devpath);
    void closeGamepad(int deviceId);
    int getUnusedDeviceId();
    QString findDefaultSdlDatabase();
    void loadCalibration();
    void scheduleNextRetry();
    void setError(DeckGamepadError error);
    void setDeviceAvailability(int deviceId, DeckGamepadDeviceAvailability availability);
    void setDeviceError(int deviceId, DeckGamepadError error);

    static DeckGamepadBackend *s_instance;

    struct udev *m_udev;
    struct udev_monitor *m_udevMonitor;
    QSocketNotifier *m_udevNotifier;

    QHash<int, DeckGamepadDevice *> m_devices; // deviceId -> device
    QHash<QString, int> m_devicePaths;         // devpath -> deviceId
    QHash<int, KnownDevice> m_knownDevices;    // deviceId -> known device info

    int m_nextDeviceId;

    // SDL DB
    DeckGamepadSdlControllerDb *m_sdlDb;

    // 自定义映射
    class DeckGamepadCustomMappingManager *m_customMappingMgr;

    std::unique_ptr<JsonCalibrationStore> m_calibrationStore;
    std::unique_ptr<CalibrationData> m_calibrationData;

    QTimer *m_retryTimer = nullptr;
    bool m_running = false;

    DeckGamepadRuntimeConfig m_runtimeConfig;
    DeckGamepadError m_lastError;

    std::unique_ptr<DeviceAccessBroker> m_accessBroker;
    std::unique_ptr<SessionGate> m_sessionGate;

    static constexpr int MAX_GAMEPADS = 16;
};

DECKGAMEPAD_END_NAMESPACE
