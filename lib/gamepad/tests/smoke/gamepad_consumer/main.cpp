// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QtCore/QString>

#include <deckshell/deckgamepad/core/deckgamepad.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcalibrationstore.h>

int main()
{
    deckshell::deckgamepad::DeckGamepadButtonEvent ev{0u, 0u, false};
    (void)ev;

    // Compatibility namespace (deprecated): still available for transition.
    deckshell::gamepad::GamepadAxis axis = deckshell::gamepad::GAMEPAD_AXIS_LEFT_X;
    (void)axis;

    // Ensure symbol is linkable in consumer project.
    deckshell::deckgamepad::JsonCalibrationStore store(QString{});
    (void)store;

    return 0;
}
