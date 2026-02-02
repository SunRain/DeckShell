// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/mapping/deckgamepadmapping.h>

#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtCore/QStringList>

DECKGAMEPAD_BEGIN_NAMESPACE

class DeckGamepadSdlControllerDbPrivate;
struct SdlRawMapping;

/**
 * @brief SDL GameController Database manager
 * 
 * This class manages the SDL GameController Database, which contains button/axis
 * mappings for thousands of gamepad devices. It provides loading, querying, and
 * conversion functionality.
 * 
 * The database file format is the same as SDL2's gamecontrollerdb.txt:
 * GUID,Name,a:b0,b:b1,x:b2,y:b3,leftshoulder:b4,...,platform:Linux
 * 
 * @note This class is typically used internally by DeckGamepadBackend.
 */
class DECKGAMEPAD_EXPORT DeckGamepadSdlControllerDb : public QObject
{
    Q_OBJECT
    
public:
    explicit DeckGamepadSdlControllerDb(QObject *parent = nullptr);
    ~DeckGamepadSdlControllerDb() override;
    
    // ========== Database Management ==========
    
    /**
     * @brief Load SDL GameController DB from file
     * @param filePath Path to gamecontrollerdb.txt
     * @return Number of mappings loaded, or -1 on error
     * 
     * This clears any existing mappings before loading.
     */
    int loadDatabase(const QString &filePath);
    
    /**
     * @brief Append mappings from another file
     * @param filePath Path to additional mapping file
     * @return Number of new mappings added, or -1 on error
     * 
     * This does not clear existing mappings.
     */
    int appendDatabase(const QString &filePath);
    
    /**
     * @brief Clear all loaded mappings
     */
    void clear();
    
    /**
     * @brief Get total number of loaded device mappings
     */
    int mappingCount() const;
    
    // ========== Query API ==========
    
    /**
     * @brief Check if a mapping exists for the given GUID
     */
    bool hasMapping(const QString &guid) const;
    
    /**
     * @brief Get device name from GUID
     * @return Device name, or empty string if not found
     */
    QString getDeviceName(const QString &guid) const;
    
    // ========== Device Mapping Conversion ==========
    
    /**
     * @brief Create optimized device mapping for runtime use
     * 
     * This converts the SDL raw mapping to a DeviceMapping structure optimized
     * for O(1) lookups during event processing.
     * 
     * @param guid Device GUID
     * @param physicalButtonMap Mapping from evdev button code to SDL button index
     * @param physicalAxisMap Mapping from evdev axis code to SDL axis index
     * @return Precomputed device mapping, or empty if GUID not found
     * 
     * The physical*Map parameters are built by device introspection (scanning
     * which buttons/axes the device actually has).
     */
    DeviceMapping createDeviceMapping(
        const QString &guid,
        const QHash<int, int> &physicalButtonMap,
        const QHash<int, int> &physicalAxisMap
    ) const;
    
    // ========== GUID Utilities ==========
    
    /**
     * @brief Extract SDL GUID from device path and name
     * 
     * Uses udev to get USB vendor/product IDs and formats them as SDL GUID.
     * Format: 03000000VVVVPPPP0000000000000000
     * 
     * @param devicePath evdev device path (e.g., "/dev/input/event5")
     * @param deviceName Device name from EVIOCGNAME ioctl
     * @return SDL GUID string, or empty on failure
     */
    static QString extractGuid(const QString &devicePath, const QString &deviceName);
    
    /**
     * @brief Format GUID to SDL standard format
     * 
     * Ensures GUID is lowercase and 32 hex characters.
     * 
     * @param rawGuid Raw GUID string
     * @return Formatted GUID
     */
    static QString formatGuid(const QString &rawGuid);
    
    // ========== Custom Mappings ==========
    
    /**
     * @brief Add a custom mapping
     * 
     * @param mappingString SDL format mapping string
     *        Format: "GUID,Name,a:b0,b:b1,...,platform:Linux"
     * @return true on success, false on parse error
     * 
     * Custom mappings override database mappings for the same GUID.
     */
    bool addMapping(const QString &mappingString);
    
    /**
     * @brief Remove a mapping by GUID
     */
    void removeMapping(const QString &guid);
    
    /**
     * @brief Export all mappings to SDL format
     * @return List of mapping strings
     */
    QStringList exportMappings() const;
    
Q_SIGNALS:
    /**
     * @brief Emitted when database is loaded
     * @param count Number of mappings loaded
     */
    void databaseLoaded(int count);
    
    /**
     * @brief Emitted when a custom mapping is added
     */
    void mappingAdded(const QString &guid);
    
    /**
     * @brief Emitted when a mapping is removed
     */
    void mappingRemoved(const QString &guid);
    
private:
    Q_DECLARE_PRIVATE(DeckGamepadSdlControllerDb)
    QScopedPointer<DeckGamepadSdlControllerDbPrivate> d_ptr;
};

DECKGAMEPAD_END_NAMESPACE
