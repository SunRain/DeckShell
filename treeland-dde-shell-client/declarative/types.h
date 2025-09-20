#ifndef DECKSHELL_QML_TYPES_H
#define DECKSHELL_QML_TYPES_H

#include "window.h"
#include "shellsurface.h"
#include <qqml.h>

// Declare that Window has attached properties
QML_DECLARE_TYPEINFO(Window, QML_HAS_ATTACHED_PROPERTIES)

// DShellClientSurface is the QML-facing name for Window attached properties
class DShellClientSurfaceForeign
{
    Q_GADGET
    QML_NAMED_ELEMENT(DShellClientSurface)
    QML_FOREIGN(Window)
    QML_UNCREATABLE("")
    QML_ATTACHED(Window)
};

// Register ShellSurface for accessing enums (like Role)
class ShellSurfaceForeign
{
    Q_GADGET
    QML_NAMED_ELEMENT(ShellSurface)
    QML_FOREIGN(ShellSurface)
    QML_UNCREATABLE("")
};

#endif // DECKSHELL_QML_TYPES_H
