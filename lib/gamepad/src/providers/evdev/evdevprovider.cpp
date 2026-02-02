// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "evdevprovider.h"

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcalibrationstore.h>

#include <QtCore/QByteArray>
#include <QtCore/QMetaObject>
#include <QtCore/QThread>

#include <algorithm>
#include <type_traits>
#include <utility>

DECKGAMEPAD_BEGIN_NAMESPACE

class EvdevProviderWorker final : public QObject
{
public:
    explicit EvdevProviderWorker(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

    DeckGamepadBackend *backend() const { return m_backend.get(); }

    void ensureBackend()
    {
        if (!m_backend) {
            m_backend = std::make_unique<DeckGamepadBackend>();
        }
    }

    void destroyBackend() { m_backend.reset(); }

private:
    std::unique_ptr<DeckGamepadBackend> m_backend;
};

namespace {
template <typename Func>
auto invokeBlocking(QObject *target, Func &&func)
{
    using Ret = std::invoke_result_t<Func>;

    if (!target) {
        if constexpr (!std::is_void_v<Ret>) {
            return Ret{};
        } else {
            return;
        }
    }

    if (QThread::currentThread() == target->thread()) {
        if constexpr (!std::is_void_v<Ret>) {
            return func();
        } else {
            func();
            return;
        }
    }

    if constexpr (std::is_void_v<Ret>) {
        QMetaObject::invokeMethod(target, std::forward<Func>(func), Qt::BlockingQueuedConnection);
        return;
    } else {
        Ret result{};
        QMetaObject::invokeMethod(target, [&] { result = func(); }, Qt::BlockingQueuedConnection);
        return result;
    }
}

template <typename Func>
void invokeQueued(QObject *target, Func &&func)
{
    if (!target) {
        return;
    }
    if (QThread::currentThread() == target->thread()) {
        func();
        return;
    }
    QMetaObject::invokeMethod(target, std::forward<Func>(func), Qt::QueuedConnection);
}
}

EvdevProvider::EvdevProvider(QObject *parent)
    : IDeckGamepadProvider(parent)
{
    (void)ensureBackendForConfig(m_config);
}

EvdevProvider::~EvdevProvider()
{
    destroyBackend();
}

QString EvdevProvider::name() const
{
    return QStringLiteral("evdev");
}

bool EvdevProvider::setRuntimeConfig(const DeckGamepadRuntimeConfig &config)
{
    if (m_running) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::InvalidConfig;
        err.message = QStringLiteral("setRuntimeConfig is only allowed when provider is not running");
        err.context = QStringLiteral("EvdevProvider::setRuntimeConfig");
        err.recoverable = true;
        setError(err);
        return false;
    }

    m_config = config;
    if (!ensureBackendForConfig(m_config)) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::BackendStartFailed;
        err.message = QStringLiteral("Failed to prepare backend instance");
        err.context = QStringLiteral("EvdevProvider::setRuntimeConfig");
        err.recoverable = false;
        setError(err);
        return false;
    }
    ensureCalibrationStore();
    return true;
}

DeckGamepadRuntimeConfig EvdevProvider::runtimeConfig() const
{
    return m_config;
}

bool EvdevProvider::start()
{
    if (m_running) {
        return true;
    }

    clearCaches();
    if (!ensureBackendForConfig(m_config)) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::BackendStartFailed;
        err.message = QStringLiteral("Failed to prepare backend instance");
        err.context = QStringLiteral("EvdevProvider::start");
        err.recoverable = false;
        setError(err);
        return false;
    }

    ensureBackendConnections();

    auto *backend = m_backend;
    DeckGamepadError backendErr;
    if (m_backendMode == BackendMode::SingleThreadDebug) {
        backend->setRuntimeConfig(m_config);
        m_running = backend->start();
        backendErr = backend->lastError();
    } else {
        m_running = invokeBlocking(backend, [backend, config = m_config, &backendErr] {
            backend->setRuntimeConfig(config);
            const bool ok = backend->start();
            backendErr = backend->lastError();
            return ok;
        });
    }
    if (!m_running) {
        if (backendErr.isOk()) {
            backendErr.code = DeckGamepadErrorCode::BackendStartFailed;
            backendErr.message = QStringLiteral("backend start failed");
            backendErr.context = QStringLiteral("DeckGamepadBackend::start");
            backendErr.recoverable = true;
        }
        setError(std::move(backendErr));
        clearCaches();
        return false;
    }

    syncSnapshotFromBackend();
    return m_running;
}

void EvdevProvider::stop()
{
    if (!m_running) {
        return;
    }

    auto *backend = m_backend;
    if (backend) {
        if (m_backendMode == BackendMode::SingleThreadDebug) {
            backend->stop();
        } else {
            invokeBlocking(backend, [backend] { backend->stop(); });
        }
    }
    m_running = false;
    clearCaches();
}

QList<int> EvdevProvider::knownGamepads() const
{
    return sortedDeviceIds(m_knownIds);
}

QList<int> EvdevProvider::connectedGamepads() const
{
    return sortedDeviceIds(m_connectedIds);
}

QString EvdevProvider::deviceName(int deviceId) const
{
    return m_deviceInfoCache.value(deviceId).name;
}

QString EvdevProvider::deviceGuid(int deviceId) const
{
    return m_deviceInfoCache.value(deviceId).guid;
}

DeckGamepadDeviceInfo EvdevProvider::deviceInfo(int deviceId) const
{
    return m_deviceInfoCache.value(deviceId);
}

QString EvdevProvider::deviceUid(int deviceId) const
{
    return m_deviceInfoCache.value(deviceId).deviceUid;
}

DeckGamepadDeviceAvailability EvdevProvider::deviceAvailability(int deviceId) const
{
    return m_deviceAvailabilityCache.value(deviceId, DeckGamepadDeviceAvailability::Removed);
}

DeckGamepadError EvdevProvider::deviceLastError(int deviceId) const
{
    return m_deviceLastErrorCache.value(deviceId);
}

void EvdevProvider::setAxisDeadzone(int deviceId, uint32_t axis, float deadzone)
{
    auto *backend = m_backend;
    invokeQueued(backend, [backend, deviceId, axis, deadzone] { backend->setAxisDeadzone(deviceId, axis, deadzone); });
}

void EvdevProvider::setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity)
{
    auto *backend = m_backend;
    invokeQueued(backend, [backend, deviceId, axis, sensitivity] { backend->setAxisSensitivity(deviceId, axis, sensitivity); });
}

bool EvdevProvider::startVibration(int deviceId, float weakMagnitude, float strongMagnitude, int durationMs)
{
    auto *backend = m_backend;
    if (!backend) {
        return false;
    }
    if (m_backendMode == BackendMode::SingleThreadDebug) {
        return backend->startVibration(deviceId, weakMagnitude, strongMagnitude, durationMs);
    }
    return invokeBlocking(backend, [backend, deviceId, weakMagnitude, strongMagnitude, durationMs] {
        return backend->startVibration(deviceId, weakMagnitude, strongMagnitude, durationMs);
    });
}

void EvdevProvider::stopVibration(int deviceId)
{
    auto *backend = m_backend;
    invokeQueued(backend, [backend, deviceId] { backend->stopVibration(deviceId); });
}

DeckGamepadCustomMappingManager *EvdevProvider::customMappingManager() const
{
    return m_customMappingManager;
}

ICalibrationStore *EvdevProvider::calibrationStore() const
{
    return m_calibrationStore.get();
}

DeckGamepadError EvdevProvider::lastError() const
{
    return m_lastError;
}

DeckGamepadDiagnostic EvdevProvider::diagnostic() const
{
    return DeckGamepadDiagnostic{};
}

void EvdevProvider::ensureBackendConnections()
{
    if (!m_backend || m_backendConnectionsReady) {
        return;
    }

    m_backendConnectionsReady = true;

    connect(m_backend,
            &DeckGamepadBackend::lastErrorChanged,
            this,
            &EvdevProvider::handleBackendLastErrorChanged,
            Qt::UniqueConnection);

    connect(m_backend,
            &DeckGamepadBackend::deviceInfoChanged,
            this,
            &EvdevProvider::handleBackendDeviceInfoChanged,
            Qt::UniqueConnection);
    connect(m_backend,
            &DeckGamepadBackend::gamepadConnected,
            this,
            &EvdevProvider::handleBackendGamepadConnected,
            Qt::UniqueConnection);
    connect(m_backend,
            &DeckGamepadBackend::gamepadDisconnected,
            this,
            &EvdevProvider::handleBackendGamepadDisconnected,
            Qt::UniqueConnection);
    connect(m_backend,
            &DeckGamepadBackend::buttonEvent,
            this,
            &EvdevProvider::buttonEvent,
            Qt::UniqueConnection);
    connect(m_backend,
            &DeckGamepadBackend::axisEvent,
            this,
            &EvdevProvider::axisEvent,
            Qt::UniqueConnection);
    connect(m_backend,
            &DeckGamepadBackend::hatEvent,
            this,
            &EvdevProvider::hatEvent,
            Qt::UniqueConnection);

    connect(m_backend,
            &DeckGamepadBackend::deviceAvailabilityChanged,
            this,
            &EvdevProvider::handleBackendDeviceAvailabilityChanged,
            Qt::UniqueConnection);
    connect(m_backend,
            &DeckGamepadBackend::deviceErrorChanged,
            this,
            &EvdevProvider::handleBackendDeviceErrorChanged,
            Qt::UniqueConnection);
}

void EvdevProvider::handleBackendLastErrorChanged(DeckGamepadError error)
{
    setError(std::move(error));
}

void EvdevProvider::handleBackendDeviceInfoChanged(int deviceId, DeckGamepadDeviceInfo info)
{
    m_knownIds.insert(deviceId);
    m_deviceInfoCache.insert(deviceId, std::move(info));
}

void EvdevProvider::handleBackendDeviceAvailabilityChanged(int deviceId, DeckGamepadDeviceAvailability availability)
{
    if (availability == DeckGamepadDeviceAvailability::Removed) {
        m_knownIds.remove(deviceId);
        m_connectedIds.remove(deviceId);
        m_deviceInfoCache.remove(deviceId);
        m_deviceAvailabilityCache.remove(deviceId);
        m_deviceLastErrorCache.remove(deviceId);
    } else {
        m_knownIds.insert(deviceId);
        m_deviceAvailabilityCache.insert(deviceId, availability);
    }

    Q_EMIT deviceAvailabilityChanged(deviceId, availability);
}

void EvdevProvider::handleBackendDeviceErrorChanged(int deviceId, DeckGamepadError error)
{
    m_deviceLastErrorCache.insert(deviceId, error);
    Q_EMIT deviceLastErrorChanged(deviceId, std::move(error));
}

void EvdevProvider::handleBackendGamepadConnected(int deviceId, const QString &name)
{
    m_knownIds.insert(deviceId);
    m_connectedIds.insert(deviceId);

    DeckGamepadDeviceInfo info = m_deviceInfoCache.value(deviceId);
    if (info.name != name) {
        info.name = name;
        m_deviceInfoCache.insert(deviceId, std::move(info));
    }

    Q_EMIT gamepadConnected(deviceId, name);
}

void EvdevProvider::handleBackendGamepadDisconnected(int deviceId)
{
    m_connectedIds.remove(deviceId);
    Q_EMIT gamepadDisconnected(deviceId);
}

void EvdevProvider::ensureCalibrationStore()
{
    const QString path = m_config.resolveCalibrationPath();
    if (!m_calibrationStore) {
        m_calibrationStore = std::make_unique<JsonCalibrationStore>(path);
        return;
    }

    m_calibrationStore->setFilePath(path);
}

void EvdevProvider::setError(DeckGamepadError error)
{
    m_lastError = std::move(error);
    Q_EMIT lastErrorChanged(m_lastError);
}

bool EvdevProvider::wantsIoThread(const DeckGamepadRuntimeConfig &config) const
{
    const QByteArray raw = qgetenv("DECKGAMEPAD_EVDEV_SINGLE_THREAD");
    if (!raw.isEmpty()) {
        const QByteArray normalized = raw.trimmed().toLower();
        if (normalized.isEmpty()
            || normalized == QByteArrayLiteral("1")
            || normalized == QByteArrayLiteral("true")
            || normalized == QByteArrayLiteral("yes")
            || normalized == QByteArrayLiteral("on")) {
            return false;
        }
        if (normalized == QByteArrayLiteral("0")
            || normalized == QByteArrayLiteral("false")
            || normalized == QByteArrayLiteral("no")
            || normalized == QByteArrayLiteral("off")) {
            // explicitly disabled
        } else {
            return false;
        }
    }

    switch (config.providerSelection) {
    case DeckGamepadProviderSelection::EvdevUdev:
        return false;
    case DeckGamepadProviderSelection::Evdev:
        return true;
    case DeckGamepadProviderSelection::Auto:
    default:
#if DECKGAMEPAD_DEFAULT_PROVIDER_EVDEV
        return true;
#else
        return false;
#endif
    }
}

bool EvdevProvider::ensureBackendForConfig(const DeckGamepadRuntimeConfig &config)
{
    const bool wantIoThread = wantsIoThread(config);
    const BackendMode desiredMode = wantIoThread ? BackendMode::IoThread : BackendMode::SingleThreadDebug;

    if (m_backend && desiredMode == m_backendMode) {
        return true;
    }

    destroyBackend();
    m_backendMode = desiredMode;

    if (m_backendMode == BackendMode::SingleThreadDebug) {
        m_singleThreadBackend = std::make_unique<DeckGamepadBackend>(this);
        m_backend = m_singleThreadBackend.get();
    } else {
        if (!m_ioThread) {
            m_ioThread = new QThread(this);
            m_ioThread->setObjectName(QStringLiteral("DeckGamepadEvdevProviderIO"));
            m_ioThread->start();
        }

        if (!m_worker) {
            m_worker = new EvdevProviderWorker();
            m_worker->moveToThread(m_ioThread);
        }

        auto *worker = m_worker;
        invokeBlocking(worker, [worker] { worker->ensureBackend(); });
        m_backend = worker->backend();
    }

    if (!m_backend) {
        destroyBackend();
        return false;
    }

    m_backendConnectionsReady = false;
    ensureBackendConnections();

    auto *backend = m_backend;
    if (m_backendMode == BackendMode::SingleThreadDebug) {
        backend->setRuntimeConfig(config);
        m_customMappingManager = backend->customMappingManager();
    } else {
        invokeBlocking(backend, [backend, config] { backend->setRuntimeConfig(config); });
        m_customMappingManager = invokeBlocking(backend, [backend] { return backend->customMappingManager(); });
    }
    ensureCalibrationStore();
    return true;
}

void EvdevProvider::destroyBackend()
{
    stop();

    m_customMappingManager = nullptr;

    if (m_worker) {
        auto *worker = m_worker;
        auto *mainThread = QThread::currentThread();

        invokeBlocking(worker, [worker] { worker->destroyBackend(); });
        invokeBlocking(worker, [worker, mainThread] { worker->moveToThread(mainThread); });

        delete worker;
        m_worker = nullptr;
    }
    m_backend = nullptr;

    m_singleThreadBackend.reset();

    if (m_ioThread) {
        m_ioThread->quit();
        m_ioThread->wait();
        delete m_ioThread;
        m_ioThread = nullptr;
    }

    m_backendConnectionsReady = false;
    m_backendMode = BackendMode::IoThread;
    clearCaches();
}

QList<int> EvdevProvider::sortedDeviceIds(const QSet<int> &ids) const
{
    QList<int> list = ids.values();
    std::sort(list.begin(), list.end());
    return list;
}

void EvdevProvider::clearCaches()
{
    m_knownIds.clear();
    m_connectedIds.clear();
    m_deviceInfoCache.clear();
    m_deviceAvailabilityCache.clear();
    m_deviceLastErrorCache.clear();
}

void EvdevProvider::syncSnapshotFromBackend()
{
    if (!m_backend) {
        return;
    }

    struct Snapshot {
        QList<int> known;
        QList<int> connected;
        QHash<int, DeckGamepadDeviceInfo> info;
        QHash<int, DeckGamepadDeviceAvailability> availability;
        QHash<int, DeckGamepadError> lastError;
    };

    Snapshot snapshot;
    auto *backend = m_backend;

    if (m_backendMode == BackendMode::SingleThreadDebug) {
        snapshot.known = backend->knownGamepads();
        snapshot.connected = backend->connectedGamepads();
        for (int id : snapshot.known) {
            snapshot.info.insert(id, backend->deviceInfo(id));
            snapshot.availability.insert(id, backend->deviceAvailability(id));
            snapshot.lastError.insert(id, backend->deviceLastError(id));
        }
    } else {
        snapshot = invokeBlocking(backend, [backend] {
            Snapshot out;
            out.known = backend->knownGamepads();
            out.connected = backend->connectedGamepads();
            for (int id : out.known) {
                out.info.insert(id, backend->deviceInfo(id));
                out.availability.insert(id, backend->deviceAvailability(id));
                out.lastError.insert(id, backend->deviceLastError(id));
            }
            return out;
        });
    }

    m_knownIds.clear();
    for (int id : snapshot.known) {
        m_knownIds.insert(id);
    }
    m_connectedIds.clear();
    for (int id : snapshot.connected) {
        m_connectedIds.insert(id);
    }
    m_deviceInfoCache = std::move(snapshot.info);
    m_deviceAvailabilityCache = std::move(snapshot.availability);
    m_deviceLastErrorCache = std::move(snapshot.lastError);
}

DECKGAMEPAD_END_NAMESPACE
