// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "modules/foreign-toplevel/foreigntoplevelmanagerv2.h"

#include <wserver.h>

#include <QCoreApplication>
#include <QFile>
#include <QTest>
#include <QXmlStreamReader>

#include <cerrno>
#include <cstring>
#include <memory>
#include <sys/socket.h>

extern "C" {
#include <wayland-client.h>
#include <wayland-server-core.h>
}

namespace {

constexpr wl_interface ForeignToplevelManagerInterface = {
    .name = "treeland_foreign_toplevel_manager_v2",
    .version = 1,
    .method_count = 0,
    .methods = nullptr,
    .event_count = 0,
    .events = nullptr,
};

struct ClientState
{
    wl_display *display = nullptr;
    wl_registry *registry = nullptr;
    uint32_t foreignToplevelName = 0;
    uint32_t foreignToplevelVersion = 0;
};

void registryGlobal(void *data,
                    wl_registry *,
                    uint32_t name,
                    const char *interface,
                    uint32_t version)
{
    auto *state = static_cast<ClientState *>(data);
    if (std::strcmp(interface, ForeignToplevelManagerInterface.name) != 0)
        return;

    state->foreignToplevelName = name;
    state->foreignToplevelVersion = version;
}

void registryGlobalRemove(void *, wl_registry *, uint32_t) { }

const wl_registry_listener RegistryListener = {
    .global = registryGlobal,
    .global_remove = registryGlobalRemove,
};

void syncDone(void *data, wl_callback *callback, uint32_t)
{
    *static_cast<bool *>(data) = true;
    wl_callback_destroy(callback);
}

const wl_callback_listener SyncListener = {
    .done = syncDone,
};

struct ProtocolContract
{
    int managerVersion = 0;
    int handleVersion = 0;
    int maximizedValue = -1;
    int minimizedValue = -1;
    int activatedValue = -1;
    int fullscreenValue = -1;
    int attentionValue = -1;
};

ProtocolContract readProtocolContract()
{
    QFile file(QString::fromUtf8(PROTOCOL_XML));
    if (!file.open(QIODevice::ReadOnly))
        return { };

    ProtocolContract contract;
    QXmlStreamReader xml(&file);
    QString currentInterface;
    bool inStateEnum = false;

    while (!xml.atEnd()) {
        xml.readNext();
        if (xml.isStartElement()) {
            if (xml.name() == QStringView(u"interface")) {
                currentInterface = xml.attributes().value(QStringView(u"name")).toString();
                const int version = xml.attributes().value(QStringView(u"version")).toInt();
                if (currentInterface == QStringLiteral("treeland_foreign_toplevel_manager_v2"))
                    contract.managerVersion = version;
                if (currentInterface == QStringLiteral("treeland_foreign_toplevel_handle_v2"))
                    contract.handleVersion = version;
            } else if (currentInterface == QStringLiteral("treeland_foreign_toplevel_handle_v2")
                       && xml.name() == QStringView(u"enum")
                       && xml.attributes().value(QStringView(u"name")) == QStringView(u"state")) {
                inStateEnum = true;
            } else if (inStateEnum && xml.name() == QStringView(u"entry")) {
                const auto name = xml.attributes().value(QStringView(u"name"));
                const int value = xml.attributes().value(QStringView(u"value")).toInt();
                if (name == QStringView(u"maximized"))
                    contract.maximizedValue = value;
                else if (name == QStringView(u"minimized"))
                    contract.minimizedValue = value;
                else if (name == QStringView(u"activated"))
                    contract.activatedValue = value;
                else if (name == QStringView(u"fullscreen"))
                    contract.fullscreenValue = value;
                else if (name == QStringView(u"attention"))
                    contract.attentionValue = value;
            }
        } else if (xml.isEndElement() && xml.name() == QStringView(u"enum") && inStateEnum) {
            inStateEnum = false;
        }
    }

    return contract;
}

} // namespace

class ForeignToplevelProtocolTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void initTestCase();
    void advertisesV2InterfaceAtVersionOne();
    void clientsCanBindV2Interface();
    void protocolDefinesV2StateValues();
    void cleanupTestCase();

private:
    void dispatchServerRequests();
    void dispatchClientEvents();
    void syncClient();

    std::unique_ptr<WAYLIB_SERVER_NAMESPACE::WServer> m_server;
    ForeignToplevelManagerInterfaceV2 *m_protocol = nullptr;
    wl_client *m_serverClient = nullptr;
    ClientState m_client;
};

void ForeignToplevelProtocolTest::dispatchServerRequests()
{
    QVERIFY(wl_display_flush(m_client.display) >= 0);
    QCOMPARE(wl_event_loop_dispatch(wl_display_get_event_loop(m_server->handle()), 0), 0);
    wl_display_flush_clients(m_server->handle());
}

void ForeignToplevelProtocolTest::dispatchClientEvents()
{
    QVERIFY(wl_display_dispatch(m_client.display) >= 0);
}

void ForeignToplevelProtocolTest::syncClient()
{
    bool done = false;
    auto *callback = wl_display_sync(m_client.display);
    wl_callback_add_listener(callback, &SyncListener, &done);
    dispatchServerRequests();
    while (!done)
        dispatchClientEvents();
}

void ForeignToplevelProtocolTest::initTestCase()
{
    m_server = std::make_unique<WAYLIB_SERVER_NAMESPACE::WServer>();
    m_protocol = m_server->attach<ForeignToplevelManagerInterfaceV2>();
    QVERIFY(m_protocol != nullptr);
    m_server->start();

    int sockets[2] = { -1, -1 };
    QCOMPARE(::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets), 0);
    m_serverClient = wl_client_create(m_server->handle(), sockets[0]);
    QVERIFY2(m_serverClient != nullptr, std::strerror(errno));
    m_client.display = wl_display_connect_to_fd(sockets[1]);
    QVERIFY(m_client.display != nullptr);
    m_client.registry = wl_display_get_registry(m_client.display);
    wl_registry_add_listener(m_client.registry, &RegistryListener, &m_client);
    syncClient();
}

void ForeignToplevelProtocolTest::advertisesV2InterfaceAtVersionOne()
{
    QVERIFY(m_client.foreignToplevelName != 0);
    QCOMPARE(m_client.foreignToplevelVersion, 1U);
}

void ForeignToplevelProtocolTest::clientsCanBindV2Interface()
{
    QVERIFY(m_client.foreignToplevelName != 0);

    auto *manager = wl_registry_bind(m_client.registry,
                                     m_client.foreignToplevelName,
                                     &ForeignToplevelManagerInterface,
                                     1);
    QVERIFY(manager != nullptr);

    syncClient();
    QCOMPARE(wl_display_get_error(m_client.display), 0);

    wl_proxy_destroy(static_cast<wl_proxy *>(manager));
}

void ForeignToplevelProtocolTest::protocolDefinesV2StateValues()
{
    const ProtocolContract contract = readProtocolContract();
    QCOMPARE(contract.managerVersion, 1);
    QCOMPARE(contract.handleVersion, 1);
    QCOMPARE(contract.maximizedValue, 0);
    QCOMPARE(contract.minimizedValue, 1);
    QCOMPARE(contract.activatedValue, 2);
    QCOMPARE(contract.fullscreenValue, 3);
    QCOMPARE(contract.attentionValue, 4);
}

void ForeignToplevelProtocolTest::cleanupTestCase()
{
    if (m_client.display) {
        if (m_client.registry)
            wl_registry_destroy(m_client.registry);
        wl_display_flush(m_client.display);
        wl_display_disconnect(m_client.display);
        m_client = { };
        wl_event_loop_dispatch(wl_display_get_event_loop(m_server->handle()), 0);
    }

    m_serverClient = nullptr;
    m_protocol = nullptr;
    m_server->stop();
    m_server.reset();
}

QTEST_GUILESS_MAIN(ForeignToplevelProtocolTest)
#include "main.moc"
