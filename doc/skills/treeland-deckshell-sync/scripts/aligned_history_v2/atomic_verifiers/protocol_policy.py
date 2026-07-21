"""Audited DeckShell ownership policy for frozen protocol components."""

from __future__ import annotations

from dataclasses import dataclass


class ProtocolOwnerError(ValueError):
    """Raised when a frozen component has no audited owner decision."""


@dataclass(frozen=True)
class ProtocolOwner:
    """One explicit owner decision and its consumer evidence."""

    owner_index: int
    consumer_paths: tuple[str, ...]
    basis: str


_CONSUMERS = {
    1: ("protocols/compositor/CMakeLists.txt",),
    78: (
        "compositor/src/modules/screensaver/CMakeLists.txt",
        "compositor/src/modules/screensaver/screensaverinterfacev1.cpp",
        "compositor/src/modules/screensaver/screensaverinterfacev1.h",
    ),
    81: (
        "compositor/src/modules/CMakeLists.txt",
        "compositor/src/modules/wine-window-state/CMakeLists.txt",
        "compositor/src/modules/wine-window-state/winewindowstate.cpp",
        "compositor/src/modules/wine-window-state/winewindowstate.h",
        "compositor/src/seat/helper.cpp",
        "compositor/src/seat/helper.h",
    ),
    83: (
        "compositor/src/core/shellhandler.cpp",
        "compositor/src/core/shellhandler.h",
        "compositor/src/modules/CMakeLists.txt",
        "compositor/src/modules/wine-window-management/CMakeLists.txt",
        "compositor/src/modules/wine-window-management/winewindowmanagement.cpp",
        "compositor/src/modules/wine-window-management/winewindowmanagement.h",
    ),
    105: (
        "compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp",
        "compositor/src/modules/foreign-toplevel/impl/foreign_toplevel_manager_impl.cpp",
        "compositor/src/modules/foreign-toplevel/impl/foreign_toplevel_manager_impl.h",
        "compositor/src/surface/surfacewrapper.cpp",
        "compositor/src/surface/surfacewrapper.h",
    ),
    136: (
        "compositor/examples/test_shortcut_capture/main.cpp",
        "compositor/src/modules/shortcut/shortcutcontroller.cpp",
        "compositor/src/modules/shortcut/shortcutcontroller.h",
        "compositor/src/modules/shortcut/shortcutmanager.cpp",
        "compositor/src/modules/shortcut/shortcutmanager.h",
        "compositor/src/seat/helper.cpp",
    ),
    138: (
        "compositor/src/modules/CMakeLists.txt",
        "compositor/src/modules/input-manager/CMakeLists.txt",
        "compositor/src/modules/input-manager/inputmanagerinterfacev1.cpp",
        "compositor/src/modules/input-manager/inputmanagerinterfacev1.h",
        "compositor/src/seat/helper.h",
    ),
    141: ("compositor/src/modules/wine-window-management/winewindowmanagement.cpp",),
    148: (
        "compositor/src/input/inputmanager.cpp",
        "compositor/src/input/inputmanager.h",
        "compositor/src/modules/input-manager/inputmanagerinterfacev1.cpp",
        "compositor/src/modules/input-manager/inputmanagerinterfacev1.h",
    ),
    152: (
        "compositor/src/modules/CMakeLists.txt",
        "compositor/src/modules/keyboard-state-notify/CMakeLists.txt",
        "compositor/src/modules/keyboard-state-notify/keyboardstatenotifymanagerinterfacev1.cpp",
        "compositor/src/modules/keyboard-state-notify/keyboardstatenotifymanagerinterfacev1.h",
        "compositor/src/seat/helper.cpp",
        "compositor/src/seat/helper.h",
    ),
    206: (
        "compositor/examples/test_window_cursor/personalization_manager.cpp",
        "compositor/examples/test_window_cursor/personalization_manager.h",
        "compositor/src/modules/personalization/personalizationmanagerinterfacev1.cpp",
        "compositor/src/modules/personalization/personalizationmanagerinterfacev1.h",
        "compositor/src/seat/helper.cpp",
    ),
    209: (
        "compositor/src/modules/wallpaper/wallpapershellinterfacev1.h",
    ),
    318: (),
}


def _component(commit: str, filename: str) -> tuple[str, str]:
    return commit, f"xml/{filename}"


_POLICY_DATA = (
    (_component("a4dfae77e76227ac82c05c9a334dd9e48217f24b", "treeland-dde-shell-v1.xml"), 318, "protocol-convergence"),
    (_component("a4dfae77e76227ac82c05c9a334dd9e48217f24b", "treeland-ddm-v1.xml"), 318, "protocol-convergence"),
    (_component("a4dfae77e76227ac82c05c9a334dd9e48217f24b", "treeland-personalization-manager-v1.xml"), 206, "source-prerequisite"),
    (_component("a4dfae77e76227ac82c05c9a334dd9e48217f24b", "treeland-screensaver-v1.xml"), 78, "source-prerequisite"),
    (_component("a4dfae77e76227ac82c05c9a334dd9e48217f24b", "treeland-shortcut-manager-v1.xml"), 318, "protocol-convergence"),
    (_component("a4dfae77e76227ac82c05c9a334dd9e48217f24b", "treeland-virtual-output-manager-v1.xml"), 318, "protocol-convergence"),
    (_component("1a55a4fc7ae13285e7b6f809720c02c1b1175f88", "treeland-wine-window-management-unstable-v1.xml"), 83, "first-consumer"),
    (_component("1a55a4fc7ae13285e7b6f809720c02c1b1175f88", "treeland-wine-window-state-unstable-v1.xml"), 81, "first-consumer"),
    (_component("4439beed371577c01090e4cb4bd91e34a054fecc", "treeland-wine-window-management-unstable-v1.xml"), 83, "first-consumer-post-image"),
    (_component("4439beed371577c01090e4cb4bd91e34a054fecc", "treeland-wine-window-state-unstable-v1.xml"), 81, "first-consumer-post-image"),
    (_component("a64cef35da000b62ab3248074bed3b640632b2d4", "treeland-wine-window-state-unstable-v1.xml"), 318, "protocol-convergence"),
    (_component("6ed6395f468bee12f72be6423bf37b9e965d0073", "treeland-capture-unstable-v1.xml"), 318, "protocol-convergence"),
    (_component("2ede9834259087ba768b44844abbc44f35e29562", "treeland-wine-window-management-unstable-v1.xml"), 141, "source-prerequisite"),
    (_component("ed69cd1713eb999f0f40182bf5acea8cc842bb97", "treeland-foreign-toplevel-manager-v1.xml"), 105, "first-consumer"),
    (_component("94faaa5510c5d142774129177376d0ba4ebefdd0", "treeland-virtual-output-manager-v1.xml"), 318, "protocol-convergence"),
    (_component("b46c4538e735331578b6bee390979f7e24592458", "treeland-shortcut-manager-v2.xml"), 136, "source-prerequisite"),
    (_component("6456001972fe13a95027d03013710a538dfe58fc", "treeland-input-manager-unstable-v1.xml"), 138, "first-consumer"),
    (_component("69225c60f3ed01d90e8cd1c70162168fd79684dc", "treeland-shortcut-manager-v2.xml"), 136, "first-consumer"),
    (_component("6ee4c0be57a6f4436324532d73b34be85772a10e", "treeland-wallpaper-shell-unstable-v1.xml"), 209, "first-consumer"),
    (_component("36027231fdff84f11c79616aeeaa59e9757c4368", "treeland-wine-window-management-unstable-v1.xml"), 141, "first-consumer"),
    (_component("ad07ed9662bf004ec5c66bd836991199f7d2d77e", "treeland-wallpaper-manager-unstable-v1.xml"), 318, "protocol-convergence"),
    (_component("37da9fb1912dd63046ba3bc5d31b863db551e957", "treeland-input-manager-unstable-v1.xml"), 148, "source-prerequisite"),
    (_component("b33863db09ba598c28254857b2da87dfb6fe61c8", "treeland-input-manager-unstable-v1.xml"), 148, "first-consumer"),
    (_component("26f58e4ca9311f1d8cda8257dcd032de01e0bc75", "treeland-input-manager-unstable-v1.xml"), 318, "protocol-convergence"),
    (_component("903e27b9af5b67f1103b31fa2816272a87acfaea", "treeland-keyboard-state-notify-unstable-v1.xml"), 152, "first-consumer"),
    (_component("8576b9cd2c05e7c7c95bc42b6d31fbfa381ce43b", "treeland-personalization-manager-v1.xml"), 206, "first-consumer"),
    (_component("89868f68aad45127f929e504e73c9715ebb2c182", "treeland-wallpaper-shell-unstable-v1.xml"), 209, "first-consumer"),
    (_component("becded8970ff0b7440a00e8c6d5c4f43867c55f1", "treeland-personalization-manager-v1.xml"), 318, "protocol-convergence"),
)

_POLICY = {
    identity: ProtocolOwner(owner, _CONSUMERS[owner], basis)
    for identity, owner, basis in _POLICY_DATA
}


def assign_protocol_owner(
    source_commit: str, source_path: str, *, anchor_absorbed: bool
) -> ProtocolOwner:
    """Return the audited owner or fail closed for an unclassified component."""

    if anchor_absorbed:
        return ProtocolOwner(1, _CONSUMERS[1], "self-contained-anchor")
    try:
        return _POLICY[(source_commit, source_path)]
    except KeyError as error:
        raise ProtocolOwnerError(
            f"no explicit protocol owner: {source_commit}:{source_path}"
        ) from error
