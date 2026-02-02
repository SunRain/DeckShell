// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "deviceuidgenerator.h"

#include <QtCore/QCryptographicHash>

DECKGAMEPAD_BEGIN_NAMESPACE

static QString udevProp(const QHash<QString, QString> &props, const char *key)
{
    const auto it = props.constFind(QString::fromLatin1(key));
    return it == props.constEnd() ? QString{} : it.value();
}

QString DeckGamepadDeviceUidGenerator::generateFromUdevProperties(const QHash<QString, QString> &props)
{
    const QString vendorId = udevProp(props, "ID_VENDOR_ID");
    const QString productId = udevProp(props, "ID_MODEL_ID");
    const QString bus = udevProp(props, "ID_BUS");

    QString serial = udevProp(props, "ID_SERIAL_SHORT");
    if (serial.isEmpty()) {
        serial = udevProp(props, "ID_SERIAL");
    }

    QString path = udevProp(props, "ID_PATH");
    if (path.isEmpty()) {
        path = udevProp(props, "DEVPATH");
    }

    // 生成输入：vendor/product/bus（非敏感）+ serial/path（敏感，仅参与 hash）
    const QString seed = vendorId + QLatin1Char(':') + productId + QLatin1Char(':') + bus + QLatin1Char('|')
        + serial + QLatin1Char('|') + path;

    const QByteArray digest = QCryptographicHash::hash(seed.toUtf8(), QCryptographicHash::Sha256).toHex();
    return QStringLiteral("evdev:") + QString::fromLatin1(digest.left(32));
}

DECKGAMEPAD_END_NAMESPACE

