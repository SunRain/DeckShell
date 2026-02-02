// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/mapping/deckgamepadcalibrationstore.h>

#include <QtCore/QDir>
#include <QtCore/QFile>
#include <QtCore/QFileInfo>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QSaveFile>

DECKGAMEPAD_BEGIN_NAMESPACE

namespace {

constexpr auto kSchemaVersion = "1.0";

QString axisKey(GamepadAxis axis)
{
    switch (axis) {
    case GAMEPAD_AXIS_LEFT_X:
        return "left_x";
    case GAMEPAD_AXIS_LEFT_Y:
        return "left_y";
    case GAMEPAD_AXIS_RIGHT_X:
        return "right_x";
    case GAMEPAD_AXIS_RIGHT_Y:
        return "right_y";
    case GAMEPAD_AXIS_TRIGGER_LEFT:
        return "trigger_left";
    case GAMEPAD_AXIS_TRIGGER_RIGHT:
        return "trigger_right";
    default:
        return {};
    }
}

GamepadAxis axisFromKey(const QString &key)
{
    if (key == QLatin1String("left_x"))
        return GAMEPAD_AXIS_LEFT_X;
    if (key == QLatin1String("left_y"))
        return GAMEPAD_AXIS_LEFT_Y;
    if (key == QLatin1String("right_x"))
        return GAMEPAD_AXIS_RIGHT_X;
    if (key == QLatin1String("right_y"))
        return GAMEPAD_AXIS_RIGHT_Y;
    if (key == QLatin1String("trigger_left"))
        return GAMEPAD_AXIS_TRIGGER_LEFT;
    if (key == QLatin1String("trigger_right"))
        return GAMEPAD_AXIS_TRIGGER_RIGHT;
    return GAMEPAD_AXIS_INVALID;
}

QString modeToString(AxisCalibrationMode mode)
{
    switch (mode) {
    case AxisCalibrationMode::MinMax:
        return "minmax";
    case AxisCalibrationMode::CenterMinMax:
        return "center_minmax";
    }
    return "center_minmax";
}

AxisCalibrationMode modeFromString(const QString &mode)
{
    if (mode == QLatin1String("minmax"))
        return AxisCalibrationMode::MinMax;
    return AxisCalibrationMode::CenterMinMax;
}

} // namespace

JsonCalibrationStore::JsonCalibrationStore(QString filePath)
    : m_filePath(std::move(filePath))
{
}

QString JsonCalibrationStore::errorString() const
{
    return m_error;
}

QString JsonCalibrationStore::filePath() const
{
    return m_filePath;
}

void JsonCalibrationStore::setFilePath(const QString &filePath)
{
    m_filePath = filePath;
}

bool JsonCalibrationStore::load(CalibrationData &out)
{
    m_error.clear();

    if (m_filePath.isEmpty()) {
        m_error = "calibration store: empty filePath";
        return false;
    }

    const QFileInfo info(m_filePath);
    if (!info.exists()) {
        out = CalibrationData{};
        out.schemaVersion = kSchemaVersion;
        return true;
    }

    QFile file(m_filePath);
    if (!file.open(QIODevice::ReadOnly)) {
        m_error = QString("calibration store: failed to open %1").arg(m_filePath);
        return false;
    }

    const QByteArray payload = file.readAll();
    if (payload.trimmed().isEmpty()) {
        out = CalibrationData{};
        out.schemaVersion = kSchemaVersion;
        return true;
    }

    const QJsonDocument doc = QJsonDocument::fromJson(payload);
    if (!doc.isObject()) {
        m_error = QString("calibration store: invalid json object %1").arg(m_filePath);
        return false;
    }

    const QJsonObject root = doc.object();
    const QString schemaVersion = root.value("schema_version").toString();
    if (schemaVersion.isEmpty()) {
        m_error = QString("calibration store: missing schema_version in %1").arg(m_filePath);
        return false;
    }
    if (schemaVersion != QLatin1String(kSchemaVersion)) {
        m_error = QString("calibration store: unsupported schema_version %1 in %2")
                      .arg(schemaVersion, m_filePath);
        return false;
    }

    CalibrationData data;
    data.schemaVersion = schemaVersion;

    const QJsonObject devicesObj = root.value("devices").toObject();
    for (auto it = devicesObj.begin(); it != devicesObj.end(); ++it) {
        const QString guid = it.key();
        const QJsonObject devObj = it.value().toObject();

        DeviceCalibration device;
        device.name = devObj.value("name").toString();
        device.backend = devObj.value("backend").toString();
        device.updatedAt = QDateTime::fromString(devObj.value("updated_at").toString(), Qt::ISODate);

        const QJsonObject axesObj = devObj.value("axes").toObject();
        for (auto axisIt = axesObj.begin(); axisIt != axesObj.end(); ++axisIt) {
            const GamepadAxis axis = axisFromKey(axisIt.key());
            if (axis == GAMEPAD_AXIS_INVALID)
                continue;

            const QJsonObject axisObj = axisIt.value().toObject();
            AxisCalibration cal;
            cal.mode = modeFromString(axisObj.value("mode").toString());
            cal.min = float(axisObj.value("min").toDouble(-1.0));
            cal.max = float(axisObj.value("max").toDouble(1.0));
            cal.centerOffset = float(axisObj.value("center_offset").toDouble(0.0));
            device.axes.insert(axis, cal);
        }

        if (!guid.isEmpty())
            data.devices.insert(guid, device);
    }

    out = data;
    return true;
}

bool JsonCalibrationStore::save(const CalibrationData &data)
{
    m_error.clear();

    if (m_filePath.isEmpty()) {
        m_error = "calibration store: empty filePath";
        return false;
    }

    if (!data.schemaVersion.isEmpty() && data.schemaVersion != QLatin1String(kSchemaVersion)) {
        m_error = QString("calibration store: refuse to write schema_version %1 (supported: %2)")
                      .arg(data.schemaVersion, QLatin1String(kSchemaVersion));
        return false;
    }

    const QFileInfo info(m_filePath);
    QDir().mkpath(info.dir().absolutePath());

    QJsonObject root;
    root["schema_version"] = QLatin1String(kSchemaVersion);

    QJsonObject devicesObj;
    for (auto it = data.devices.constBegin(); it != data.devices.constEnd(); ++it) {
        const QString &guid = it.key();
        const DeviceCalibration &device = it.value();

        QJsonObject devObj;
        if (!device.name.isEmpty())
            devObj["name"] = device.name;
        if (!device.backend.isEmpty())
            devObj["backend"] = device.backend;
        if (device.updatedAt.isValid())
            devObj["updated_at"] = device.updatedAt.toUTC().toString(Qt::ISODateWithMs);

        QJsonObject axesObj;
        for (auto axisIt = device.axes.constBegin(); axisIt != device.axes.constEnd(); ++axisIt) {
            const QString key = axisKey(axisIt.key());
            if (key.isEmpty())
                continue;

            const AxisCalibration &cal = axisIt.value();
            QJsonObject axisObj;
            axisObj["mode"] = modeToString(cal.mode);
            if (cal.mode == AxisCalibrationMode::CenterMinMax)
                axisObj["center_offset"] = double(cal.centerOffset);
            axisObj["min"] = double(cal.min);
            axisObj["max"] = double(cal.max);
            axesObj[key] = axisObj;
        }
        if (!axesObj.isEmpty())
            devObj["axes"] = axesObj;

        if (!guid.isEmpty())
            devicesObj[guid] = devObj;
    }

    root["devices"] = devicesObj;

    QSaveFile file(m_filePath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        m_error = QString("calibration store: failed to open for write %1").arg(m_filePath);
        return false;
    }

    const QJsonDocument doc(root);
    file.write(doc.toJson(QJsonDocument::Indented));

    if (!file.commit()) {
        m_error = QString("calibration store: failed to commit %1").arg(m_filePath);
        return false;
    }

    return true;
}

DECKGAMEPAD_END_NAMESPACE
