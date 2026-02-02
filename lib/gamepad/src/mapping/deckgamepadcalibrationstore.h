// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QDateTime>
#include <QtCore/QHash>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

enum class AxisCalibrationMode {
    MinMax,
    CenterMinMax,
};

struct AxisCalibration {
    AxisCalibrationMode mode = AxisCalibrationMode::CenterMinMax;
    float min = -1.0f;
    float max = 1.0f;
    float centerOffset = 0.0f;
};

struct DeviceCalibration {
    QString name;
    QString backend;
    QDateTime updatedAt;
    QHash<GamepadAxis, AxisCalibration> axes;
};

struct CalibrationData {
    QString schemaVersion = "1.0";
    QHash<QString, DeviceCalibration> devices; // GUID -> calibration
};

class ICalibrationStore
{
public:
    virtual ~ICalibrationStore() = default;

    virtual QString errorString() const = 0;
    virtual bool load(CalibrationData &out) = 0;
    virtual bool save(const CalibrationData &data) = 0;
};

class DECKGAMEPAD_EXPORT JsonCalibrationStore final : public ICalibrationStore
{
public:
    explicit JsonCalibrationStore(QString filePath);

    QString errorString() const override;
    bool load(CalibrationData &out) override;
    bool save(const CalibrationData &data) override;

    QString filePath() const;
    void setFilePath(const QString &filePath);

private:
    QString m_filePath;
    QString m_error;
};

DECKGAMEPAD_END_NAMESPACE
