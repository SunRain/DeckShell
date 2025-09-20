#ifndef SHELLSURFACE_H
#define SHELLSURFACE_H

#include "ddeshellclient_export.h"

#include <QObject>
#include <QPoint>
#include <qqml.h>

#include <QtWaylandClient/private/qwaylandclientextension_p.h>

#include "qwayland-treeland-dde-shell-v1.h"

class DDESHELLCLIENT_EXPORT ShellSurface : public QObject,
                                      public QtWayland::treeland_dde_shell_surface_v1
{
    Q_OBJECT
    QML_ANONYMOUS

public:
    enum class Role {
        Overlay = 1  // OVERLAY role from protocol
    };
    Q_ENUM(Role)

    explicit ShellSurface(struct ::treeland_dde_shell_surface_v1 *object,
                         QObject *parent = nullptr);
    ~ShellSurface() override;

    // Property getters
    [[nodiscard]] QPoint position() const { return m_position; }
    [[nodiscard]] Role role() const { return m_role; }
    [[nodiscard]] uint32_t yOffset() const { return m_yOffset; }
    [[nodiscard]] bool skipSwitcher() const { return m_skipSwitcher; }
    [[nodiscard]] bool skipDockPreview() const { return m_skipDockPreview; }
    [[nodiscard]] bool skipMultitaskview() const { return m_skipMultitaskview; }
    [[nodiscard]] bool acceptKeyboardFocus() const { return m_acceptKeyboardFocus; }

    // Property setters (send requests to compositor)
    void setSurfacePosition(const QPoint &pos);
    void setRole(Role role);
    void setAutoPlacement(uint32_t offset);
    void setSkipSwitcher(bool skip);
    void setSkipDockPreview(bool skip);
    void setSkipMultitaskview(bool skip);
    void setAcceptKeyboardFocus(bool accept);

Q_SIGNALS:
    void positionChanged(const QPoint &position);
    void roleChanged(Role role);
    void yOffsetChanged(uint32_t offset);
    void skipSwitcherChanged(bool skip);
    void skipDockPreviewChanged(bool skip);
    void skipMultitaskviewChanged(bool skip);
    void acceptKeyboardFocusChanged(bool accept);

private:
    // Current state
    QPoint m_position;
    Role m_role = Role::Overlay;
    uint32_t m_yOffset = 0;
    bool m_skipSwitcher = false;
    bool m_skipDockPreview = false;
    bool m_skipMultitaskview = false;
    bool m_acceptKeyboardFocus = true;

    bool m_positionValid = false;
    bool m_roleValid = false;
};

#endif // SHELLSURFACE_H
