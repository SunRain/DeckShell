// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
#include "treeland-foreign-toplevel-manager-v2.h"
#include "server-bridge-api.h"
#include "treeland-foreign-toplevel-manager-unstable-v2-client-protocol.h"

#include <errno.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern void ftm_read_server_state(void *data);
extern void ftm_render_and_settle(void *data);
extern void ftm_set_attention(void *data);
extern void ftm_clear_activation(void *data);

enum {
    WIRE_STATE_MAXIMIZED = 0,
    WIRE_STATE_MINIMIZED = 1,
    WIRE_STATE_ACTIVATED = 2,
    WIRE_STATE_FULLSCREEN = 3,
    WIRE_STATE_ATTENTION = 4,
    MAX_RECEIVED_STATES = 8,
};

static uint32_t received_states[MAX_RECEIVED_STATES];
static int received_state_count;
static int received_state_event;
static int received_state_overflow;

static void clear_received_states(void)
{
    received_state_count = 0;
    received_state_event = 0;
    received_state_overflow = 0;
}

static int received_state_matches(uint32_t expected, int present)
{
    if (!received_state_event || received_state_overflow)
        return 0;

    int found = 0;
    for (int i = 0; i < received_state_count; ++i) {
        if (received_states[i] > WIRE_STATE_ATTENTION)
            return 0;
        for (int j = 0; j < i; ++j) {
            if (received_states[j] == received_states[i])
                return 0;
        }
        found |= received_states[i] == expected;
    }

    return found == present;
}

struct test_case {
    const char *name;
    int (*run)(struct test_ctx *ctx);
};

void test_init(struct test_ctx *ctx)
{
    memset(ctx, 0, sizeof(*ctx));
    ctx->result_cap = 32;
    ctx->results = calloc(ctx->result_cap, sizeof(*ctx->results));
}

void test_destroy(struct test_ctx *ctx)
{
    free(ctx->results);
    memset(ctx, 0, sizeof(*ctx));
}

int test_add(struct test_ctx *ctx, const char *name)
{
    if (ctx->result_count == ctx->result_cap) {
        ctx->result_cap *= 2;
        ctx->results = realloc(ctx->results, (size_t)ctx->result_cap * sizeof(*ctx->results));
    }
    const int index = ctx->result_count++;
    ctx->results[index] = (struct test_result) { .name = name };
    return index;
}

void test_fail(struct test_ctx *ctx, int index, const char *format, ...)
{
    va_list arguments;
    va_start(arguments, format);
    vsnprintf(ctx->results[index].message, TEST_MSG_MAX, format, arguments);
    va_end(arguments);
    ctx->results[index].failed = 1;
}

void test_pass(struct test_ctx *ctx, int index)
{
    ctx->results[index].failed = 0;
}

int test_print_results(struct test_ctx *ctx)
{
    int failed = 0;
    printf("\n=== results ===\n");
    for (int i = 0; i < ctx->result_count; ++i) {
        printf("  [%s] %s", ctx->results[i].failed ? "FAIL" : "PASS", ctx->results[i].name);
        if (ctx->results[i].failed) {
            printf(" -- %s", ctx->results[i].message);
            ++failed;
        }
        printf("\n");
    }
    printf("%d/%d passed\n", ctx->result_count - failed, ctx->result_count);
    return failed == 0;
}

static void handle_pid(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                       uint32_t pid)
{
    (void)data;
    (void)handle;
    (void)pid;
}

static void handle_title(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                         const char *title)
{
    (void)data;
    (void)handle;
    (void)title;
}

static void handle_app_id(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                          const char *app_id)
{
    (void)data;
    (void)handle;
    (void)app_id;
}

static void handle_identifier(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                              uint32_t identifier)
{
    (void)handle;
    ((struct test_ctx *)data)->handle_identifier = identifier;
}

static void handle_output_enter(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                                struct wl_output *output)
{
    (void)data;
    (void)handle;
    (void)output;
}

static void handle_output_leave(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                                struct wl_output *output)
{
    (void)data;
    (void)handle;
    (void)output;
}

static void handle_state(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                         struct wl_array *state)
{
    (void)data;
    (void)handle;
    clear_received_states();
    received_state_event = 1;
    uint32_t *value;
    wl_array_for_each(value, state) {
        if (received_state_count == MAX_RECEIVED_STATES) {
            received_state_overflow = 1;
            continue;
        }
        received_states[received_state_count++] = *value;
    }
}

static void handle_done(void *data, struct treeland_foreign_toplevel_handle_v2 *handle)
{
    (void)data;
    (void)handle;
}

static void handle_closed(void *data, struct treeland_foreign_toplevel_handle_v2 *handle)
{
    struct test_ctx *ctx = data;
    if (ctx->handle == handle)
        ctx->handle = NULL;
    ++ctx->handle_closed_count;
    treeland_foreign_toplevel_handle_v2_destroy(handle);
}

static void handle_parent(void *data, struct treeland_foreign_toplevel_handle_v2 *handle,
                          struct treeland_foreign_toplevel_handle_v2 *parent)
{
    (void)data;
    (void)handle;
    (void)parent;
}

static const struct treeland_foreign_toplevel_handle_v2_listener handle_listener = {
    .pid = handle_pid,
    .title = handle_title,
    .app_id = handle_app_id,
    .identifier = handle_identifier,
    .output_enter = handle_output_enter,
    .output_leave = handle_output_leave,
    .state = handle_state,
    .done = handle_done,
    .closed = handle_closed,
    .parent = handle_parent,
};

static void manager_toplevel(void *data, struct treeland_foreign_toplevel_manager_v2 *manager,
                             struct treeland_foreign_toplevel_handle_v2 *toplevel)
{
    (void)manager;
    struct test_ctx *ctx = data;
    ctx->handle = toplevel;
    ++ctx->handle_count;
    treeland_foreign_toplevel_handle_v2_add_listener(toplevel, &handle_listener, ctx);
}

static void manager_finished(void *data, struct treeland_foreign_toplevel_manager_v2 *manager)
{
    (void)manager;
    ((struct test_ctx *)data)->manager_finished_received = 1;
}

static const struct treeland_foreign_toplevel_manager_v2_listener manager_listener = {
    .toplevel = manager_toplevel,
    .finished = manager_finished,
};

static void context_enter(void *data, struct treeland_dock_preview_context_v2 *context)
{
    (void)context;
    ((struct test_ctx *)data)->context_enter_received = 1;
}

static void context_leave(void *data, struct treeland_dock_preview_context_v2 *context)
{
    (void)context;
    ((struct test_ctx *)data)->context_leave_received = 1;
}

static const struct treeland_dock_preview_context_v2_listener context_listener = {
    .enter = context_enter,
    .leave = context_leave,
};

static int connect_client(struct test_ctx *ctx, const char *socket_name)
{
    if (!client_connect(&ctx->connection, socket_name))
        return 0;
    ctx->display = ctx->connection.display;
    ctx->seat = client_bind(&ctx->connection, "wl_seat", &wl_seat_interface, 1);
    ctx->manager = client_bind(&ctx->connection, "treeland_foreign_toplevel_manager_v2",
                                      &treeland_foreign_toplevel_manager_v2_interface, 1);
    if (ctx->manager)
        treeland_foreign_toplevel_manager_v2_add_listener(ctx->manager, &manager_listener, ctx);
    return ctx->seat != NULL && ctx->manager != NULL;
}

static int read_server_state(struct test_ctx *ctx, struct ftm_server_state *state)
{
    (void)ctx;
    memset(state, 0, sizeof(*state));
    return invoke_on_server_thread(ftm_read_server_state, state);
}

static int settle_geometry_animation(struct test_ctx *ctx)
{
    (void)ctx;
    return invoke_on_server_thread(ftm_render_and_settle, NULL);
}

static int create_xdg_toplevel(struct test_ctx *ctx)
{
    if (!xdg_toplevel_client_create(&ctx->connection, &ctx->xdg_toplevel))
        return 0;
    struct ftm_server_state state;
    return wl_display_roundtrip(ctx->display) >= 0
           && ctx->xdg_toplevel.configured
           && ctx->handle
           && ctx->handle_count == 1
           && ctx->handle_identifier
           && settle_geometry_animation(ctx)
           && read_server_state(ctx, &state)
           && state.wrapper_created
           && state.wrapper_in_workspace;
}

static int create_context(struct test_ctx *ctx)
{
    if (!ctx->xdg_toplevel.surface)
        return 0;
    ctx->context = treeland_foreign_toplevel_manager_v2_get_dock_preview_context(
        ctx->manager, ctx->xdg_toplevel.surface);
    if (ctx->context)
        treeland_dock_preview_context_v2_add_listener(ctx->context, &context_listener, ctx);
    return ctx->context != NULL;
}

static int show_preview(struct test_ctx *ctx)
{
    if (!ctx->context || !ctx->handle_identifier)
        return 0;
    struct wl_array surfaces;
    wl_array_init(&surfaces);
    uint32_t *slot = wl_array_add(&surfaces, sizeof(uint32_t));
    if (!slot) {
        wl_array_release(&surfaces);
        return 0;
    }
    *slot = ctx->handle_identifier;
    treeland_dock_preview_context_v2_show(ctx->context, &surfaces, 10, 20,
                                          TREELAND_DOCK_PREVIEW_CONTEXT_V2_DIRECTION_BOTTOM);
    wl_array_release(&surfaces);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    if (!read_server_state(ctx, &state))
        return 0;
    return state.preview_fired
           && state.preview_x == 10
           && state.preview_y == 20
           && state.preview_direction == TREELAND_DOCK_PREVIEW_CONTEXT_V2_DIRECTION_BOTTOM
           && state.preview_surface_count == 1;
}

static int show_unknown_identifier(struct test_ctx *ctx)
{
    if (!ctx->context)
        return 0;
    struct wl_array surfaces;
    wl_array_init(&surfaces);
    uint32_t *slot = wl_array_add(&surfaces, sizeof(uint32_t));
    if (!slot)
        return 0;
    *slot = 0xDEADBEEFu;

    treeland_dock_preview_context_v2_show(ctx->context, &surfaces, 1, 2,
                                          TREELAND_DOCK_PREVIEW_CONTEXT_V2_DIRECTION_TOP);
    wl_array_release(&surfaces);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    if (!read_server_state(ctx, &state))
        return 0;
    return state.preview_fired && state.preview_surface_count == 0;
}

static int show_tooltip(struct test_ctx *ctx)
{
    if (!ctx->context)
        return 0;
    treeland_dock_preview_context_v2_show_tooltip(ctx->context, "dock-tooltip", 5, 6,
                                                  TREELAND_DOCK_PREVIEW_CONTEXT_V2_DIRECTION_TOP);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    if (!read_server_state(ctx, &state))
        return 0;
    return state.tooltip_fired
           && strcmp(state.tooltip, "dock-tooltip") == 0
           && state.tooltip_x == 5
           && state.tooltip_y == 6
           && state.tooltip_direction == TREELAND_DOCK_PREVIEW_CONTEXT_V2_DIRECTION_TOP;
}

static int close_preview(struct test_ctx *ctx)
{
    if (!ctx->context)
        return 0;
    treeland_dock_preview_context_v2_close(ctx->context);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    if (!read_server_state(ctx, &state))
        return 0;
    return state.close_fired;
}

static int minimize_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    clear_received_states();
    treeland_foreign_toplevel_handle_v2_set_minimized(ctx->handle);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    return read_server_state(ctx, &state) && state.wrapper_minimized
           && received_state_matches(WIRE_STATE_MINIMIZED, 1);
}

static int restore_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    clear_received_states();
    treeland_foreign_toplevel_handle_v2_unset_minimized(ctx->handle);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    return read_server_state(ctx, &state) && !state.wrapper_minimized
           && received_state_matches(WIRE_STATE_MINIMIZED, 0);
}

static int render_ack_and_read_server_state(struct test_ctx *ctx, struct ftm_server_state *state)
{
    return settle_geometry_animation(ctx)
           && xdg_toplevel_client_ack_latest_configure(&ctx->connection, &ctx->xdg_toplevel)
           && settle_geometry_animation(ctx)
           && read_server_state(ctx, state);
}

static int maximize_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    clear_received_states();
    treeland_foreign_toplevel_handle_v2_set_maximized(ctx->handle);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    return render_ack_and_read_server_state(ctx, &state) && state.wrapper_maximized
           && received_state_matches(WIRE_STATE_MAXIMIZED, 1);
}

static int unmaximize_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    clear_received_states();
    treeland_foreign_toplevel_handle_v2_unset_maximized(ctx->handle);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    return render_ack_and_read_server_state(ctx, &state) && !state.wrapper_maximized
           && received_state_matches(WIRE_STATE_MAXIMIZED, 0);
}

static int fullscreen_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    clear_received_states();
    treeland_foreign_toplevel_handle_v2_set_fullscreen(ctx->handle, NULL);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    return render_ack_and_read_server_state(ctx, &state) && state.wrapper_fullscreen
           && received_state_matches(WIRE_STATE_FULLSCREEN, 1);
}

static int unfullscreen_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    clear_received_states();
    treeland_foreign_toplevel_handle_v2_unset_fullscreen(ctx->handle);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    return render_ack_and_read_server_state(ctx, &state) && !state.wrapper_fullscreen
           && received_state_matches(WIRE_STATE_FULLSCREEN, 0);
}

static int activate_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle || !ctx->seat)
        return 0;
    /* A restored window can already be active; test a real state transition. */
    if (!invoke_on_server_thread(ftm_clear_activation, NULL)
        || wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    if (!read_server_state(ctx, &state) || state.wrapper_activated || state.wrapper_focused)
        return 0;
    clear_received_states();
    treeland_foreign_toplevel_handle_v2_activate(ctx->handle, ctx->seat);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    return read_server_state(ctx, &state) && state.wrapper_activated && state.wrapper_focused
           && received_state_matches(WIRE_STATE_ACTIVATED, 1);
}

static int set_attention(struct test_ctx *ctx, int attention)
{
    int request[2] = { attention, 0 };
    clear_received_states();
    if (!invoke_on_server_thread(ftm_set_attention, request) || !request[1])
        return 0;
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    return received_state_matches(WIRE_STATE_MINIMIZED, 1)
           && received_state_matches(WIRE_STATE_ATTENTION, attention);
}

static int attention_real_toplevel(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    struct ftm_server_state state;
    if (!read_server_state(ctx, &state) || !state.wrapper_minimized)
        return 0;
    return set_attention(ctx, 1) && set_attention(ctx, 0);
}

static int set_icon_geometry_changes_icon_geometry(struct test_ctx *ctx)
{
    if (!ctx->handle || !ctx->xdg_toplevel.surface)
        return 0;
    treeland_foreign_toplevel_handle_v2_set_icon_geometry(ctx->handle,
                                                       ctx->xdg_toplevel.surface,
                                                       11, 12, 130, 140);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    struct ftm_server_state state;
    return read_server_state(ctx, &state)
           && state.icon_x == state.wrapper_x + 11 && state.icon_y == state.wrapper_y + 12
           && state.icon_width == 130 && state.icon_height == 140;
}

static int request_close(struct test_ctx *ctx)
{
    if (!ctx->handle)
        return 0;
    treeland_foreign_toplevel_handle_v2_close(ctx->handle);
    return wl_display_roundtrip(ctx->display) >= 0 && ctx->xdg_toplevel.close_received;
}

static int destroy_context(struct test_ctx *ctx)
{
    if (!ctx->context)
        return 0;
    treeland_dock_preview_context_v2_destroy(ctx->context);
    ctx->context = NULL;
    return wl_display_roundtrip(ctx->display) >= 0;
}

static int stop_manager(struct test_ctx *ctx)
{
    if (!ctx->manager)
        return 0;
    treeland_foreign_toplevel_manager_v2_stop(ctx->manager);
    if (wl_display_roundtrip(ctx->display) < 0)
        return 0;
    return ctx->manager_finished_received;
}

static int duplicate_context_rejected(const char *socket_name)
{
    struct test_ctx duplicate;
    test_init(&duplicate);
    int rejected = 0;
    if (connect_client(&duplicate, socket_name)
        && xdg_toplevel_client_create(&duplicate.connection, &duplicate.xdg_toplevel)
        && wl_display_roundtrip(duplicate.display) >= 0
        && create_context(&duplicate)
        && wl_display_roundtrip(duplicate.display) >= 0) {
        const uint32_t manager_id = wl_proxy_get_id((struct wl_proxy *)duplicate.manager);
        struct treeland_dock_preview_context_v2 *second =
            treeland_foreign_toplevel_manager_v2_get_dock_preview_context(
                duplicate.manager, duplicate.xdg_toplevel.surface);
        if (second) {
            const struct wl_interface *interface = NULL;
            uint32_t object_id = 0;
            if (wl_display_roundtrip(duplicate.display) < 0
                && wl_display_get_error(duplicate.display) == EPROTO) {
                const uint32_t code = wl_display_get_protocol_error(
                    duplicate.display, &interface, &object_id);
                /* 07d3368 定义的独立 expected，不能与生产端共用生成枚举。 */
                rejected = code == 1 && object_id == manager_id
                           && interface == &treeland_foreign_toplevel_manager_v2_interface;
            }
            wl_proxy_destroy((struct wl_proxy *)second);
        }
    }
    test_cleanup(&duplicate);
    test_destroy(&duplicate);
    return rejected;
}

static const struct test_case cases[] = {
    { "client.create_xdg_toplevel", create_xdg_toplevel },
    { "manager.get_dock_preview_context", create_context },
    { "context.show", show_preview },
    { "context.show_unknown_identifier", show_unknown_identifier },
    { "context.show_tooltip", show_tooltip },
    { "context.close", close_preview },
    { "handle.minimize_changes_wrapper", minimize_real_toplevel },
    { "handle.attention_uses_v2_wire_state", attention_real_toplevel },
    { "handle.restore_changes_wrapper", restore_real_toplevel },
    { "handle.maximize_changes_wrapper", maximize_real_toplevel },
    { "handle.unmaximize_changes_wrapper", unmaximize_real_toplevel },
    { "handle.fullscreen_changes_wrapper", fullscreen_real_toplevel },
    { "handle.unfullscreen_changes_wrapper", unfullscreen_real_toplevel },
    { "handle.activate_focuses_wrapper", activate_real_toplevel },
    { "handle.set_icon_geometry_changes_icon_geometry", set_icon_geometry_changes_icon_geometry },
    { "handle.close_requests_xdg_close", request_close },
    { "context.destroy", destroy_context },
    { "context.recreate_after_destroy", create_context },
    { "context.destroy_recreated", destroy_context },
    { "manager.stop", stop_manager },
};

void test_cleanup(struct test_ctx *ctx)
{
    if (ctx->context) treeland_dock_preview_context_v2_destroy(ctx->context);
    xdg_toplevel_client_destroy(&ctx->xdg_toplevel);
    if (ctx->handle) treeland_foreign_toplevel_handle_v2_destroy(ctx->handle);
    if (ctx->manager) treeland_foreign_toplevel_manager_v2_destroy(ctx->manager);
    if (ctx->seat) wl_seat_destroy(ctx->seat);
    client_disconnect(&ctx->connection);
}

int protocol_test_run(const char *socket_name)
{
    struct test_ctx ctx;
    test_init(&ctx);
    if (!connect_client(&ctx, socket_name)) {
        fprintf(stderr, "failed to connect to or bind treeland_foreign_toplevel_manager_v2\n");
        test_cleanup(&ctx);
        test_destroy(&ctx);
        return 1;
    }

    for (size_t i = 0; i < sizeof(cases) / sizeof(cases[0]); ++i) {
        const int result = test_add(&ctx, cases[i].name);
        if (!cases[i].run(&ctx))
            test_fail(&ctx, result, "assertion failed");
        if (wl_display_roundtrip(ctx.display) < 0)
            test_fail(&ctx, result, "Wayland connection failed");
    }

    test_cleanup(&ctx);
    const int duplicate_result = test_add(&ctx, "context.duplicate_is_protocol_error");
    if (!duplicate_context_rejected(socket_name))
        test_fail(&ctx, duplicate_result, "expected manager context_already_exists error 1");
    const int success = test_print_results(&ctx);
    test_destroy(&ctx);
    return success ? 0 : 1;
}
