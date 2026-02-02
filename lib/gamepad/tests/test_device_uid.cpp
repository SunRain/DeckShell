// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/backend/deviceuidgenerator.h>

#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

class TestDeviceUid : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void deterministicAndRedacted()
    {
        QHash<QString, QString> props;
        props.insert(QStringLiteral("ID_VENDOR_ID"), QStringLiteral("045e"));
        props.insert(QStringLiteral("ID_MODEL_ID"), QStringLiteral("028e"));
        props.insert(QStringLiteral("ID_BUS"), QStringLiteral("usb"));
        props.insert(QStringLiteral("ID_SERIAL_SHORT"), QStringLiteral("ABC123"));
        props.insert(QStringLiteral("ID_PATH"), QStringLiteral("pci-0000:00:14.0-usb-0:2:1.0"));

        const QString uid = DeckGamepadDeviceUidGenerator::generateFromUdevProperties(props);
        QCOMPARE(uid, QStringLiteral("evdev:8280bcc20ce18c56e58c1d06ce8383a2"));
        QVERIFY(!uid.contains(QStringLiteral("ABC123")));
        QVERIFY(!uid.contains(QStringLiteral("pci-0000")));
    }
};

QTEST_MAIN(TestDeviceUid)

#include "test_device_uid.moc"

