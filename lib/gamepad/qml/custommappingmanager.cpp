// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "custommappingmanager.h"

#include <deckshell/deckgamepad/mapping/deckgamepadcustommappingmanager.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QMetaObject>
#include <QtCore/QThread>

#include <type_traits>
#include <utility>

using deckshell::deckgamepad::DeckGamepadService;
using deckshell::deckgamepad::DeckGamepadCustomMappingManager;

namespace {
template <typename Func>
auto invokeBlocking(DeckGamepadCustomMappingManager *manager, Func &&func)
{
    using Ret = std::invoke_result_t<Func>;

    if (!manager) {
        if constexpr (!std::is_void_v<Ret>) {
            return Ret{};
        } else {
            return;
        }
    }

    if (QThread::currentThread() == manager->thread()) {
        if constexpr (!std::is_void_v<Ret>) {
            return func();
        } else {
            func();
            return;
        }
    }

    if constexpr (std::is_void_v<Ret>) {
        QMetaObject::invokeMethod(manager, std::forward<Func>(func), Qt::BlockingQueuedConnection);
        return;
    } else {
        Ret result{};
        QMetaObject::invokeMethod(manager, [&] { result = func(); }, Qt::BlockingQueuedConnection);
        return result;
    }
}
}

CustomMappingManager::CustomMappingManager(QObject *parent)
    : QObject(parent)
{
}

CustomMappingManager::~CustomMappingManager() = default;

void CustomMappingManager::setService(DeckGamepadService *service)
{
    m_service = service;
    syncFromService();
}

bool CustomMappingManager::supported() const
{
    return m_supported;
}

QString CustomMappingManager::createCustomMapping(int deviceId)
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId] { return mgr->createCustomMapping(deviceId); });
}

bool CustomMappingManager::hasCustomMapping(int deviceId) const
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId] { return mgr->hasCustomMapping(deviceId); });
}

QStringList CustomMappingManager::availablePresets() const
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr] { return mgr->availablePresets(); });
}

bool CustomMappingManager::loadPreset(int deviceId, const QString &presetName)
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId, presetName] { return mgr->loadPreset(deviceId, presetName); });
}

bool CustomMappingManager::saveToFile(const QString &filePath)
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, filePath] { return mgr->saveToFile(filePath); });
}

int CustomMappingManager::loadFromFile(const QString &filePath)
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, filePath] { return mgr->loadFromFile(filePath); });
}

bool CustomMappingManager::applyMapping(int deviceId)
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId] { return mgr->applyMapping(deviceId); });
}

bool CustomMappingManager::resetToSdlDefault(int deviceId)
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId] { return mgr->resetToSdlDefault(deviceId); });
}

bool CustomMappingManager::isMappingComplete(int deviceId) const
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId] { return mgr->isMappingComplete(deviceId); });
}

QStringList CustomMappingManager::getMissingMappings(int deviceId) const
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId] { return mgr->getMissingMappings(deviceId); });
}

QString CustomMappingManager::exportToSdlString(int deviceId) const
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId] { return mgr->exportToSdlString(deviceId); });
}

bool CustomMappingManager::importFromSdlString(int deviceId, const QString &sdlString)
{
    auto *mgr = mappingManager();
    return invokeBlocking(mgr, [mgr, deviceId, sdlString] { return mgr->importFromSdlString(deviceId, sdlString); });
}

void CustomMappingManager::syncFromService()
{
    const bool nextSupported = mappingManager() != nullptr;
    if (m_supported == nextSupported) {
        return;
    }

    m_supported = nextSupported;
    Q_EMIT supportedChanged();
}

DeckGamepadCustomMappingManager *CustomMappingManager::mappingManager() const
{
    return m_service ? m_service->customMappingManager() : nullptr;
}
