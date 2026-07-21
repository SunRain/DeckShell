from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


from aligned_history_v2.freeze_inputs import (
    CORRECTED_V1_HEAD,
    CORRECTED_V1_REF,
    FINAL_GITLINK,
    _verify_authority_links,
)


def test_corrected_v1_authority_is_bound_to_r6() -> None:
    assert CORRECTED_V1_HEAD == "ed032e12dca9a7f1efa09439eb1e094ba68bc97c"
    assert CORRECTED_V1_REF.endswith(
        "commit-aligned-history-corrected-v1-compile-atomic-r6-20260729"
    )


def test_v2_uses_remediation_atomic_replay_ref_checkpoint() -> None:
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

    assert module.input_paths(args).refs_before.name == (
        "remediation-atomic-replay-correction-refs-before.json"
    )


def test_r6_authority_accepts_signal_dependency_component() -> None:
    digest = "a" * 64
    current = {
        "protocol_lock": {
            "endpoint": "becded8970ff0b7440a00e8c6d5c4f43867c55f1",
            "endpoint_tree": "ab850b37bf123fad630318cff815586cb1bbd403",
            "history": [{"commit": "anchor"}],
        },
        "anchor": {"protocol_source_commit": "anchor"},
        "dependency_set": {"dependency_sensitive_indices": list(range(129))},
        "dependency_bundle": {"component_count": 670},
        "runtime_observations": {"observation_count": 1},
        "protocol_ledger": {"source_component_count": 97},
        "v1_history": {"outcome": "pass"},
        "task9": {"product_entries_sha256": digest},
        "master_product": {"entries_sha256": digest},
    }
    mapping = {"records": [{"gitlink": FINAL_GITLINK}]}

    _verify_authority_links(current, mapping)
