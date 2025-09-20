#ifndef WAYLANDMANAGER_H
#define WAYLANDMANAGER_H

#include "ddeshellclient_export.h"

#include <QObject>
#include <QWaylandClientExtension>

#include <QtWaylandClient/private/qwaylandclientextension_p.h>

#include "qwayland-treeland-dde-shell-v1.h"

class ShellSurface;

class DDESHELLCLIENT_EXPORT WaylandManager : public QWaylandClientExtensionTemplate<WaylandManager>,
                                        public QtWayland::treeland_dde_shell_manager_v1
{
    Q_OBJECT

public:
    explicit WaylandManager(QObject *parent = nullptr);
    ~WaylandManager() override;

    [[nodiscard]] bool isReady() const;
    [[nodiscard]] ShellSurface *createShellSurface(struct wl_surface *surface);

Q_SIGNALS:
    void ready();

private:
    void onActiveChanged();
    bool m_ready = false;
};

#endif // WAYLANDMANAGER_H
