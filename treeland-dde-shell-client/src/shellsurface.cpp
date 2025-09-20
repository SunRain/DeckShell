#include "shellsurface.h"

#include <QDebug>

ShellSurface::ShellSurface(struct ::treeland_dde_shell_surface_v1 *object,
                         QObject *parent)
    : QObject(parent)
    , QtWayland::treeland_dde_shell_surface_v1(object)
{
    qDebug() << QStringLiteral("ShellSurface created with object:") << object;
}

ShellSurface::~ShellSurface()
{
    qDebug() << QStringLiteral("ShellSurface destroyed");
    destroy();
}

void ShellSurface::setSurfacePosition(const QPoint &pos)
{
    if (pos == m_position && m_positionValid) {
        return;
    }

    qDebug() << QStringLiteral("ShellSurface: Setting position to") << pos;

    set_surface_position(pos.x(), pos.y());

    m_position = pos;
    m_positionValid = true;
    emit positionChanged(pos);
}

void ShellSurface::setRole(Role role)
{
    if (role == m_role && m_roleValid) {
        return;
    }

    qDebug() << QStringLiteral("ShellSurface: Setting role to")
             << static_cast<uint32_t>(role);

    set_role(static_cast<uint32_t>(role));

    m_role = role;
    m_roleValid = true;
    emit roleChanged(role);
}

void ShellSurface::setAutoPlacement(uint32_t offset)
{
    if (offset == m_yOffset) {
        return;
    }

    qDebug() << QStringLiteral("ShellSurface: Setting auto placement with Y offset") << offset;

    set_auto_placement(offset);

    m_yOffset = offset;
    emit yOffsetChanged(offset);
}

void ShellSurface::setSkipSwitcher(bool skip)
{
    if (skip == m_skipSwitcher) {
        return;
    }

    qDebug() << QStringLiteral("ShellSurface: Setting skip switcher to") << skip;

    set_skip_switcher(skip ? 1 : 0);

    m_skipSwitcher = skip;
    emit skipSwitcherChanged(skip);
}

void ShellSurface::setSkipDockPreview(bool skip)
{
    if (skip == m_skipDockPreview) {
        return;
    }

    qDebug() << QStringLiteral("ShellSurface: Setting skip dock preview to") << skip;

    set_skip_dock_preview(skip ? 1 : 0);

    m_skipDockPreview = skip;
    emit skipDockPreviewChanged(skip);
}

void ShellSurface::setSkipMultitaskview(bool skip)
{
    if (skip == m_skipMultitaskview) {
        return;
    }

    qDebug() << QStringLiteral("ShellSurface: Setting skip multitaskview to") << skip;

    set_skip_muti_task_view(skip ? 1 : 0);

    m_skipMultitaskview = skip;
    emit skipMultitaskviewChanged(skip);
}

void ShellSurface::setAcceptKeyboardFocus(bool accept)
{
    if (accept == m_acceptKeyboardFocus) {
        return;
    }

    qDebug() << QStringLiteral("ShellSurface: Setting accept keyboard focus to") << accept;

    set_accept_keyboard_focus(accept ? 1 : 0);

    m_acceptKeyboardFocus = accept;
    emit acceptKeyboardFocusChanged(accept);
}
