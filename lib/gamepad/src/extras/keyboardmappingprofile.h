// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/extras/deckgamepadkeyboardmapping.h>

#include <QString>
#include <QDateTime>
#include <QJsonObject>
#include <QMap>

DECKGAMEPAD_BEGIN_NAMESPACE

/**
 * @brief Keyboard Mapping Profile
 * 
 * Represents a complete keyboard mapping configuration that can be
 * saved, loaded, and switched between different game scenarios.
 * 
 * Profiles are stored as individual JSON files.
 * The storage path is determined by the upper layer (e.g. compositor config manager),
 * typically under XDG AppConfigLocation/profiles with legacy fallback if needed.
 */
struct KeyboardMappingProfile {
    QString name;
    QString description;
    QDateTime createdAt;
    QDateTime modifiedAt;
    
    // Mappings
    QMap<GamepadButton, KeyMapping> buttonMappings;
    QMap<GamepadAxis, AxisKeyMapping> axisMappings;
    
    KeyboardMappingProfile();
    explicit KeyboardMappingProfile(const QString &profileName);
    
    bool isValid() const { return !name.isEmpty(); }
    
    /**
     * @brief Serialize to JSON
     */
    QJsonObject toJson() const;
    
    /**
     * @brief Deserialize from JSON
     */
    static KeyboardMappingProfile fromJson(const QJsonObject &obj);
    
    /**
     * @brief Apply this profile to a keyboard mapping manager
     */
    void applyTo(DeckGamepadKeyboardMappingManager *manager) const;
    
    /**
     * @brief Load profile from a keyboard mapping manager
     */
    static KeyboardMappingProfile fromManager(const QString &name, 
                                               const DeckGamepadKeyboardMappingManager *manager);
    
    // ========== Preset Templates ==========
    
    /**
     * @brief WASD preset for FPS games
     * Left Stick: WASD
     * A: Space (Jump), B: Shift (Sprint)
     * X: E (Interact), Y: R (Reload)
     */
    static KeyboardMappingProfile createWASDPreset();
    
    /**
     * @brief Arrow Keys preset for retro games
     * DPad: Arrow Keys
     * A: Enter, B: Ctrl
     */
    static KeyboardMappingProfile createArrowKeysPreset();
    
    /**
     * @brief Numpad preset for fighting games
     * Right Stick: Numpad 8246
     * Buttons: Numpad numbers
     */
    static KeyboardMappingProfile createNumpadPreset();
};

DECKGAMEPAD_END_NAMESPACE
