// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/mapping/deckgamepadcalibrationstore.h>

#include <QtCore/QFile>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QTemporaryDir>
#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

class TestCalibrationStoreJson final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void load_missingFile_returnsDefault()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("calibration.json"));
        QVERIFY(!QFile::exists(path));

        JsonCalibrationStore store(path);
        CalibrationData out;
        QVERIFY(store.load(out));
        QCOMPARE(out.schemaVersion, QStringLiteral("1.0"));
        QVERIFY(out.devices.isEmpty());
    }

    void load_emptyFile_returnsDefault()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("calibration.json"));
        QFile file(path);
        QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate));
        file.close();

        JsonCalibrationStore store(path);
        CalibrationData out;
        QVERIFY(store.load(out));
        QCOMPARE(out.schemaVersion, QStringLiteral("1.0"));
        QVERIFY(out.devices.isEmpty());
    }

    void load_invalidJson_returnsError()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("calibration.json"));
        QFile file(path);
        QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate));
        file.write("not-json");
        file.close();

        JsonCalibrationStore store(path);
        CalibrationData out;
        QVERIFY(!store.load(out));
        QVERIFY(!store.errorString().isEmpty());
    }

    void load_unknownFields_areIgnored()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("calibration.json"));

        QJsonObject axisObj;
        axisObj[QStringLiteral("mode")] = QStringLiteral("center_minmax");
        axisObj[QStringLiteral("min")] = -0.9;
        axisObj[QStringLiteral("max")] = 0.9;
        axisObj[QStringLiteral("center_offset")] = 0.1;
        axisObj[QStringLiteral("extra")] = true;

        QJsonObject axesObj;
        axesObj[QStringLiteral("left_x")] = axisObj;
        axesObj[QStringLiteral("unknown_axis")] = QJsonObject{{QStringLiteral("min"), 0.0}, {QStringLiteral("max"), 1.0}};

        const QString guid = QStringLiteral("03000000deadbeef0000000000000000");

        QJsonObject devObj;
        devObj[QStringLiteral("name")] = QStringLiteral("Pad");
        devObj[QStringLiteral("backend")] = QStringLiteral("evdev");
        devObj[QStringLiteral("updated_at")] = QStringLiteral("2026-01-26T00:00:00.000Z");
        devObj[QStringLiteral("unknown_field")] = 123;
        devObj[QStringLiteral("axes")] = axesObj;

        QJsonObject root;
        root[QStringLiteral("schema_version")] = QStringLiteral("1.0");
        root[QStringLiteral("devices")] = QJsonObject{{guid, devObj}};
        root[QStringLiteral("root_unknown")] = QStringLiteral("ignored");

        QFile file(path);
        QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate));
        file.write(QJsonDocument(root).toJson(QJsonDocument::Compact));
        file.close();

        JsonCalibrationStore store(path);
        CalibrationData out;
        QVERIFY(store.load(out));

        QVERIFY(out.devices.contains(guid));
        const DeviceCalibration dev = out.devices.value(guid);
        QCOMPARE(dev.name, QStringLiteral("Pad"));
        QCOMPARE(dev.backend, QStringLiteral("evdev"));
        QVERIFY(dev.updatedAt.isValid());
        QVERIFY(dev.axes.contains(GAMEPAD_AXIS_LEFT_X));
        QVERIFY(!dev.axes.contains(GAMEPAD_AXIS_INVALID));

        const AxisCalibration cal = dev.axes.value(GAMEPAD_AXIS_LEFT_X);
        QCOMPARE(static_cast<int>(cal.mode), static_cast<int>(AxisCalibrationMode::CenterMinMax));
        QCOMPARE(cal.min, -0.9f);
        QCOMPARE(cal.max, 0.9f);
        QCOMPARE(cal.centerOffset, 0.1f);
    }

    void save_writesStableSchema()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("calibration.json"));
        JsonCalibrationStore store(path);

        const QString guid = QStringLiteral("03000000deadbeef0000000000000000");

        CalibrationData data;
        data.schemaVersion = QStringLiteral("1.0");

        DeviceCalibration dev;
        dev.name = QStringLiteral("Pad");
        dev.backend = QStringLiteral("evdev");
        dev.updatedAt = QDateTime::fromString(QStringLiteral("2026-01-26T00:00:00.000Z"), Qt::ISODate);
        AxisCalibration cal;
        cal.mode = AxisCalibrationMode::CenterMinMax;
        cal.min = -0.75f;
        cal.max = 0.75f;
        cal.centerOffset = 0.05f;
        dev.axes.insert(GAMEPAD_AXIS_LEFT_X, cal);
        data.devices.insert(guid, dev);

        QVERIFY(store.save(data));

        QFile file(path);
        QVERIFY(file.open(QIODevice::ReadOnly));
        const QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
        QVERIFY(doc.isObject());

        const QJsonObject root = doc.object();
        QCOMPARE(root.value(QStringLiteral("schema_version")).toString(), QStringLiteral("1.0"));

        const QJsonObject devicesObj = root.value(QStringLiteral("devices")).toObject();
        QVERIFY(devicesObj.contains(guid));

        const QJsonObject devObj = devicesObj.value(guid).toObject();
        QCOMPARE(devObj.value(QStringLiteral("name")).toString(), QStringLiteral("Pad"));
        QCOMPARE(devObj.value(QStringLiteral("backend")).toString(), QStringLiteral("evdev"));
        QVERIFY(devObj.value(QStringLiteral("axes")).isObject());

        const QJsonObject axesObj = devObj.value(QStringLiteral("axes")).toObject();
        QVERIFY(axesObj.contains(QStringLiteral("left_x")));
    }
};

QTEST_MAIN(TestCalibrationStoreJson)
#include "test_calibration_store_json.moc"

