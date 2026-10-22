// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "modules/dde-shell/ddeshellmanagerinterfacev1.h"
#include "modules/personalization/personalizationmanagerinterfacev1.h"
#include "modules/output-group/outputgroupmanagerinterfacev1.h"

#include <wserver.h>

#include <QTest>

#include <cerrno>
#include <cstring>
#include <memory>
#include <sys/socket.h>

extern "C" {
#include <wayland-client.h>
#include <wayland-server-core.h>
}

namespace {

constexpr wl_message DdeManagerRequests[] = {
    { "get_window_overlap_checker", "n", nullptr },
    { "get_shell_surface", "no", nullptr },
    { "get_treeland_dde_active", "no", nullptr },
    { "get_treeland_multitaskview", "n", nullptr },
    { "get_treeland_window_picker", "n", nullptr },
    { "get_treeland_lockscreen", "n", nullptr },
    { "set_xwindow_position_relative", "nuoff", nullptr },
    { "destroy", "2", nullptr },
};

constexpr wl_interface DdeManagerInterface = {
    .name = "treeland_dde_shell_manager_v1",
    .version = 2,
    .method_count = 8,
    .methods = DdeManagerRequests,
    .event_count = 0,
    .events = nullptr,
};

constexpr wl_message PersonalizationManagerRequests[] = {
    { "get_window_context", "no", nullptr },
    { "get_cursor_context", "n", nullptr },
    { "get_font_context", "n", nullptr },
    { "get_appearance_context", "n", nullptr },
    { "destroy", "2", nullptr },
};

constexpr wl_interface PersonalizationManagerInterface = {
    .name = "treeland_personalization_manager_v1",
    .version = 2,
    .method_count = 5,
    .methods = PersonalizationManagerRequests,
    .event_count = 0,
    .events = nullptr,
};

constexpr wl_message OutputGroupManagerRequests[] = {
    { "destroy", "", nullptr },
    { "create_group", "ns", nullptr },
    { "get_group", "ns", nullptr },
};

constexpr wl_message OutputGroupManagerEvents[] = {
    { "group_added", "s", nullptr },
    { "groups_done", "", nullptr },
    { "group_removed", "s", nullptr },
};

constexpr wl_interface OutputGroupManagerInterface = {
    .name = "treeland_output_group_manager_v1",
    .version = 1,
    .method_count = 3,
    .methods = OutputGroupManagerRequests,
    .event_count = 3,
    .events = OutputGroupManagerEvents,
};

void groupChanged(void *, wl_proxy *, const char *) { }
void groupsDone(void *, wl_proxy *) { }

struct OutputGroupManagerListener
{
    void (*groupAdded)(void *, wl_proxy *, const char *);
    void (*groupsDone)(void *, wl_proxy *);
    void (*groupRemoved)(void *, wl_proxy *, const char *);
};

constexpr OutputGroupManagerListener OutputGroupListener = {
    &groupChanged, &groupsDone, &groupChanged,
};

struct ClientState
{
    wl_display *display = nullptr;
    wl_registry *registry = nullptr;
    uint32_t ddeName = 0;
    uint32_t personalizationName = 0;
    uint32_t outputGroupName = 0;
    uint32_t ddeVersion = 0;
    uint32_t personalizationVersion = 0;
    uint32_t outputGroupVersion = 0;
};

void registryGlobal(void *data,
                    wl_registry *,
                    uint32_t name,
                    const char *interface,
                    uint32_t version)
{
    auto *state = static_cast<ClientState *>(data);
    if (std::strcmp(interface, DdeManagerInterface.name) == 0) {
        state->ddeName = name;
        state->ddeVersion = version;
    } else if (std::strcmp(interface, PersonalizationManagerInterface.name) == 0) {
        state->personalizationName = name;
        state->personalizationVersion = version;
    } else if (std::strcmp(interface, OutputGroupManagerInterface.name) == 0) {
        state->outputGroupName = name;
        state->outputGroupVersion = version;
    }
}

void registryGlobalRemove(void *, wl_registry *, uint32_t) { }

constexpr wl_registry_listener RegistryListener = {
    .global = registryGlobal,
    .global_remove = registryGlobalRemove,
};

void syncDone(void *data, wl_callback *callback, uint32_t)
{
    *static_cast<bool *>(data) = true;
    wl_callback_destroy(callback);
}

constexpr wl_callback_listener SyncListener = {
    .done = syncDone,
};

bool dispatchServer(WAYLIB_SERVER_NAMESPACE::WServer *server, wl_display *display)
{
    if (wl_display_flush(display) < 0)
        return false;
    if (wl_event_loop_dispatch(wl_display_get_event_loop(server->handle()), 0) != 0)
        return false;
    wl_display_flush_clients(server->handle());
    return true;
}

bool syncClient(WAYLIB_SERVER_NAMESPACE::WServer *server, wl_display *display)
{
    bool done = false;
    auto *callback = wl_display_sync(display);
    if (!callback)
        return false;
    wl_callback_add_listener(callback, &SyncListener, &done);

    while (!done) {
        if (!dispatchServer(server, display))
            return false;
        if (wl_display_dispatch(display) < 0)
            return false;
    }
    return true;
}

struct ResourceSearch
{
    const char *interfaceName = nullptr;
    wl_resource *resource = nullptr;
    int count = 0;
};

enum wl_iterator_result findResource(wl_resource *resource, void *data)
{
    auto *search = static_cast<ResourceSearch *>(data);
    if (std::strcmp(wl_resource_get_class(resource), search->interfaceName) == 0) {
        search->resource = resource;
        ++search->count;
    }
    return WL_ITERATOR_CONTINUE;
}

int resourceCount(wl_client *client, const char *interfaceName)
{
    ResourceSearch search{ .interfaceName = interfaceName };
    wl_client_for_each_resource(client, &findResource, &search);
    return search.count;
}

struct DestroyProbe
{
    wl_listener listener{ };
    int *count = nullptr;
};

void resourceDestroyed(wl_listener *listener, void *)
{
    auto *probe = reinterpret_cast<DestroyProbe *>(reinterpret_cast<char *>(listener)
                                                   - offsetof(DestroyProbe, listener));
    ++*probe->count;
    wl_list_remove(&probe->listener.link);
    delete probe;
}

void watchResource(wl_resource *resource, int *count)
{
    auto *probe = new DestroyProbe;
    probe->count = count;
    probe->listener.notify = &resourceDestroyed;
    wl_resource_add_destroy_listener(resource, &probe->listener);
}

} // namespace

class ManagerResourceLifecycleTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void managerResourcesAreDestroyed_data();
    void managerResourcesAreDestroyed();
};

void ManagerResourceLifecycleTest::managerResourcesAreDestroyed_data()
{
    QTest::addColumn<QString>("trigger");
    QTest::newRow("explicit destructor") << QStringLiteral("explicit");
    QTest::newRow("client disconnect") << QStringLiteral("disconnect");
    QTest::newRow("server stop") << QStringLiteral("server-stop");
}

void ManagerResourceLifecycleTest::managerResourcesAreDestroyed()
{
    QFETCH(QString, trigger);

    auto server = std::make_unique<WAYLIB_SERVER_NAMESPACE::WServer>();
    QVERIFY(server->attach<DDEShellManagerInterfaceV1>() != nullptr);
    QVERIFY(server->attach<PersonalizationManagerInterfaceV1>() != nullptr);
    QVERIFY(server->attach<OutputGroupManagerInterfaceV1>() != nullptr);
    server->start();
    QCoreApplication::processEvents();

    int sockets[2] = { -1, -1 };
    QCOMPARE(::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets), 0);
    auto *serverClient = wl_client_create(server->handle(), sockets[0]);
    QVERIFY2(serverClient != nullptr, std::strerror(errno));

    ClientState client;
    client.display = wl_display_connect_to_fd(sockets[1]);
    QVERIFY(client.display != nullptr);
    client.registry = wl_display_get_registry(client.display);
    wl_registry_add_listener(client.registry, &RegistryListener, &client);
    QVERIFY(syncClient(server.get(), client.display));

    QCOMPARE(client.ddeVersion, 2U);
    QCOMPARE(client.personalizationVersion, 2U);
    QCOMPARE(client.outputGroupVersion, 1U);

    auto *dde = wl_registry_bind(client.registry, client.ddeName, &DdeManagerInterface, 2);
    auto *personalization = wl_registry_bind(client.registry,
                                             client.personalizationName,
                                             &PersonalizationManagerInterface,
                                             2);
    auto *outputGroup = wl_registry_bind(client.registry,
                                         client.outputGroupName,
                                         &OutputGroupManagerInterface,
                                         1);
    QVERIFY(dde != nullptr);
    QVERIFY(personalization != nullptr);
    QVERIFY(outputGroup != nullptr);
    QCOMPARE(wl_proxy_add_listener(static_cast<wl_proxy *>(outputGroup),
                                   reinterpret_cast<void (**)(void)>(
                                       const_cast<OutputGroupManagerListener *>(&OutputGroupListener)),
                                   nullptr),
             0);
    QVERIFY(dispatchServer(server.get(), client.display));

    QCOMPARE(resourceCount(serverClient, DdeManagerInterface.name), 1);
    QCOMPARE(resourceCount(serverClient, PersonalizationManagerInterface.name), 1);
    QCOMPARE(resourceCount(serverClient, OutputGroupManagerInterface.name), 1);

    int ddeDestroyed = 0;
    int personalizationDestroyed = 0;
    int outputGroupDestroyed = 0;
    ResourceSearch ddeSearch{ .interfaceName = DdeManagerInterface.name };
    ResourceSearch personalizationSearch{ .interfaceName = PersonalizationManagerInterface.name };
    ResourceSearch outputGroupSearch{ .interfaceName = OutputGroupManagerInterface.name };
    wl_client_for_each_resource(serverClient, &findResource, &ddeSearch);
    wl_client_for_each_resource(serverClient, &findResource, &personalizationSearch);
    wl_client_for_each_resource(serverClient, &findResource, &outputGroupSearch);
    watchResource(ddeSearch.resource, &ddeDestroyed);
    watchResource(personalizationSearch.resource, &personalizationDestroyed);
    watchResource(outputGroupSearch.resource, &outputGroupDestroyed);

    if (trigger == QStringLiteral("explicit")) {
        wl_proxy_marshal_flags(static_cast<wl_proxy *>(dde),
                               7,
                               nullptr,
                               2,
                               WL_MARSHAL_FLAG_DESTROY);
        wl_proxy_marshal_flags(static_cast<wl_proxy *>(personalization),
                               4,
                               nullptr,
                               2,
                               WL_MARSHAL_FLAG_DESTROY);
        wl_proxy_marshal_flags(static_cast<wl_proxy *>(outputGroup),
                               0,
                               nullptr,
                               1,
                               WL_MARSHAL_FLAG_DESTROY);
        dde = nullptr;
        personalization = nullptr;
        outputGroup = nullptr;
        QVERIFY(dispatchServer(server.get(), client.display));
        QCOMPARE(resourceCount(serverClient, DdeManagerInterface.name), 0);
        QCOMPARE(resourceCount(serverClient, PersonalizationManagerInterface.name), 0);
        QCOMPARE(resourceCount(serverClient, OutputGroupManagerInterface.name), 0);
    } else if (trigger == QStringLiteral("disconnect")) {
        wl_display_disconnect(client.display);
        client.display = nullptr;
        QVERIFY(wl_event_loop_dispatch(wl_display_get_event_loop(server->handle()), 0)
                == 0);
    } else {
        server->stop();
        QVERIFY(!server->isRunning());
        QVERIFY(server->handle() == nullptr);
    }

    QCOMPARE(ddeDestroyed, 1);
    QCOMPARE(personalizationDestroyed, 1);
    QCOMPARE(outputGroupDestroyed, 1);

    if (client.display) {
        wl_registry_destroy(client.registry);
        client.registry = nullptr;
        wl_display_disconnect(client.display);
        client.display = nullptr;
        if (trigger != QStringLiteral("server-stop")) {
            QVERIFY(wl_event_loop_dispatch(wl_display_get_event_loop(server->handle()), 0)
                    == 0);
        }
    }

    if (trigger != QStringLiteral("server-stop"))
        server->stop();
}

QTEST_GUILESS_MAIN(ManagerResourceLifecycleTest)
#include "main.moc"
