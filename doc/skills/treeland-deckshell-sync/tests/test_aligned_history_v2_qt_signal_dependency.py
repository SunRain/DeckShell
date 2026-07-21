"""Independent v2 dependency discovery for bare Qt signal emits."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.atomic_verifiers.cpp_symbols import (
    definition_matches,
    qt_signal_emits,
)
from aligned_history_v2.atomic_verifiers.dependency_scanner import (
    scan_static_dependencies,
)
from aligned_history_v2.atomic_rebuild import rebuild_atomic_ledgers
from aligned_history_v2.repository import GitRepository


def test_bare_q_emit_is_a_complete_use_not_a_method_declaration() -> None:
    line = "Q_EMIT windowMenuRequested(position);"

    assert qt_signal_emits(line) == {"windowMenuRequested"}
    assert definition_matches(line, path="surfacewrapper.cpp") == []


def test_discovers_qt_signal_emit_before_same_file_family_declaration() -> None:
    transitions = [
        {"ordered_index": 159, "entry_id": "treeland:consumer"},
        {"ordered_index": 213, "entry_id": "treeland:provider"},
    ]
    patches = {
        159: """diff --git a/compositor/src/surface/surfacewrapper.cpp b/compositor/src/surface/surfacewrapper.cpp
+++ b/compositor/src/surface/surfacewrapper.cpp
@@ -1,0 +2 @@
+Q_EMIT windowMenuRequested(position);
""",
        213: """diff --git a/compositor/src/surface/surfacewrapper.h b/compositor/src/surface/surfacewrapper.h
+++ b/compositor/src/surface/surfacewrapper.h
@@ -1,0 +2 @@
+    void windowMenuRequested(QPointF pos);
""",
    }

    result = scan_static_dependencies(
        transitions,
        patch_provider=lambda entry: patches[entry["ordered_index"]],
    )

    assert result["symbol_edges"] == [
        {
            "kind": "symbol-cross-entry",
            "symbol": "windowMenuRequested",
            "owner_index": 213,
            "required_owner_index": 159,
            "observed_member_indices": [159, 213],
            "first_member_index": 159,
            "last_member_index": 213,
            "early_member_indices": [],
            "roles": {
                "159": ["complete-use"],
                "213": ["definition"],
            },
            "member_paths": {
                "159": ["compositor/src/surface/surfacewrapper.cpp"],
                "213": ["compositor/src/surface/surfacewrapper.h"],
            },
            "definition_kinds": {"213": ["method"]},
            "definition_lines": {
                "213": {
                    "compositor/src/surface/surfacewrapper.h": [
                        "    void windowMenuRequested(QPointF pos);"
                    ]
                }
            },
            "use_lines": {
                "159": {
                    "compositor/src/surface/surfacewrapper.cpp": [
                        "Q_EMIT windowMenuRequested(position);"
                    ]
                }
            },
            "provider_new_file_paths": [],
            "use_kinds": {"159": ["qt-signal-emit"]},
        }
    ]


def test_does_not_join_qt_signal_from_unrelated_file_family() -> None:
    transitions = [
        {"ordered_index": 10, "entry_id": "treeland:consumer"},
        {"ordered_index": 20, "entry_id": "treeland:provider"},
    ]
    patches = {
        10: """diff --git a/compositor/src/widget.cpp b/compositor/src/widget.cpp
+++ b/compositor/src/widget.cpp
@@ -1,0 +2 @@
+Q_EMIT completed();
""",
        20: """diff --git a/compositor/src/controller.h b/compositor/src/controller.h
+++ b/compositor/src/controller.h
@@ -1,0 +2 @@
+    void completed();
""",
    }

    result = scan_static_dependencies(
        transitions,
        patch_provider=lambda entry: patches[entry["ordered_index"]],
    )

    assert result["symbol_edges"] == []


def test_r6_dependency_ledgers_recompute_exactly_with_670_components() -> None:
    entrypoint = SCRIPTS_DIR / "aligned_history_v2.py"
    spec = importlib.util.spec_from_file_location("r6_v2_entrypoint", entrypoint)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    artifact_root = Path(__file__).resolve().parents[4]
    workspace = artifact_root.parents[5]
    args = module.build_parser().parse_args(
        [
            "--mode",
            "commit-aligned-history-rewrite-v2",
            "--workspace",
            str(workspace),
            "--plan",
            str(
                workspace
                / ".helloagents/plans/"
                "202607262338_commit-aligned-history-compile-atomic-protocol-alignment/"
                "plan.md"
            ),
            "--output",
            str(artifact_root / "corrected-v2/formal"),
            "candidate",
        ]
    )
    paths = module.input_paths(args)

    rebuilt = rebuild_atomic_ledgers(paths, GitRepository(paths.repo))

    assert rebuilt["dependency"]["artifact_sha256"] == (
        "3ef492f6bd548e51c2eadbad5b0ad0233319f1ebe26281ddfc2ab5ed9bfdfedf"
    )
    assert rebuilt["bundle"]["component_count"] == 670
    assert rebuilt["rebuilt_bundle"]["component_count"] == 670
