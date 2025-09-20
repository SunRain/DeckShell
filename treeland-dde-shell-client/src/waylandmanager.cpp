#include "waylandmanager.h"

#include <QDebug>

#include "shellsurface.h"

WaylandManager::WaylandManager(QObject *parent)
    : QWaylandClientExtensionTemplate<WaylandManager>(1)
    , QtWayland::treeland_dde_shell_manager_v1()
{
    connect(this, &QWaylandClientExtension::activeChanged,
            this, &WaylandManager::onActiveChanged);
}

WaylandManager::~WaylandManager()
{
}

bool WaylandManager::isReady() const
{
    return m_ready;
}

ShellSurface *WaylandManager::createShellSurface(struct wl_surface *surface)
{
    qDebug() << QStringLiteral("WaylandManager::createShellSurface called with surface:")
             << surface;

    if (!isActive()) {
        qWarning() << QStringLiteral("treeland-dde-shell-v1 protocol is not active yet. ")
                   << QStringLiteral("Protocol version:") << QWaylandClientExtension::version()
                   << QStringLiteral(", isActive:") << isActive()
                   << QStringLiteral(", m_ready:") << m_ready;
        qWarning() << QStringLiteral("This usually means the Wayland compositor does not "
                                     "support the treeland-dde-shell-v1 protocol ")
                   << QStringLiteral("or the protocol binding is still in progress.");
        return nullptr;
    }

    qDebug() << QStringLiteral("Protocol is active, calling get_shell_surface...");
    auto *shellSurface = get_shell_surface(surface);
    if (!shellSurface) {
        qWarning() << QStringLiteral("get_shell_surface() failed for surface:") << surface;
        qWarning() << QStringLiteral("This could mean:");
        qWarning() << QStringLiteral("  1. The Wayland compositor does not implement "
                                     "treeland-dde-shell-v1 protocol");
        qWarning() << QStringLiteral("  2. The surface is invalid or in an incorrect state");
        qWarning() << QStringLiteral("  3. The compositor has run out of resources");
        qWarning() << QStringLiteral("  4. Protocol version mismatch between client and server");
        return nullptr;
    }

    qDebug() << QStringLiteral("Successfully created shell surface:") << shellSurface;
    // 注意：返回裸指针是安全的，因为 ShellSurface 的 parent 是 this（WaylandManager）
    // Qt 的父子树机制会自动管理内存
    return new ShellSurface(shellSurface, this);
}

void WaylandManager::onActiveChanged()
{
    qDebug() << Q_FUNC_INFO << QStringLiteral(" activeChanged: isActive()=") << isActive();

    m_ready = isActive();
    if (m_ready) {
        emit ready();
    }
}
