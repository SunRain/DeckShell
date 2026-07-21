// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QObject>

#include <functional>
#include <utility>

namespace DeckShell {

namespace detail {

class SingleMatchConnection final : public QObject
{
public:
    using QObject::QObject;

    ~SingleMatchConnection() override
    {
        QObject::disconnect(m_connection);
    }

    void setConnection(QMetaObject::Connection connection)
    {
        m_connection = std::move(connection);
    }

    void finish()
    {
        QObject::disconnect(m_connection);
        m_connection = { };
        deleteLater();
    }

private:
    QMetaObject::Connection m_connection;
};

} // namespace detail

template<typename Sender, typename Signal, typename Predicate, typename Handler>
// Connects until the predicate accepts one signal emission, then disconnects only this listener.
void connectUntilMatch(Sender *sender,
                       Signal signal,
                       QObject *context,
                       Predicate predicate,
                       Handler handler)
{
    Q_ASSERT(sender);
    Q_ASSERT(context);
    if (!sender || !context)
        return;

    auto *connection = new detail::SingleMatchConnection(context);
    connection->setConnection(QObject::connect(
        sender,
        signal,
        connection,
        [connection, predicate = std::move(predicate), handler = std::move(handler)](
            auto &&...arguments) mutable {
            if (!std::invoke(predicate, std::forward<decltype(arguments)>(arguments)...))
                return;

            connection->finish();
            std::invoke(handler, std::forward<decltype(arguments)>(arguments)...);
        }));
}

} // namespace DeckShell
