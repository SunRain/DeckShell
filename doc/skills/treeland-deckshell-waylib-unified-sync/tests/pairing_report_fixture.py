"""Synthetic pairing records for unrelated report/CAS unit tests, never product evidence."""

from unified_sync_lib.git_ops import canonical_json_sha256
from unified_sync_lib.protocol_pairing import PAIRING_KIND
from unified_sync_lib.protocol_sources import PROVENANCE_PATH

PAIR = {
    "implementation": {"repository": "fixture", "commit": "0" * 40, "paths": ["waylib/server.cpp"]},
    "protocol": {"repository": "fixture", "commit": "0" * 40, "path": "xml/remote.xml"},
}


def report_pairing(inventory, manifest, validations):
    """Supply a complete synthetic upstream-review input to report serialization tests."""
    selected = {"build": "waylib-candidate-build", "consumer": "waylib-package-consumer", "interaction": "waylib-ctest"}
    entries = {row["id"]: row for row in validations["entries"]}
    for name in selected.values():
        row = entries[name]
        if row["command"][0] == "ctest" and "--no-tests=error" not in row["command"]:
            row["command"].append("--no-tests=error")
        if "checkout_identity" not in row:
            source = {**row["git_identity"]["before"], "linked_worktree": True,
                      "common_git_dir": manifest["identity"]["child_common_git_dir"]}
            row["checkout_identity"] = {phase: {"source": source, "dependencies": {}} for phase in ("before", "after")}
        row["manifest_sha256"] = canonical_json_sha256(manifest)
    inspection = {"outcome": "pass", "implementation": inventory["range"],
                  "protocol": {"base": "0" * 40, "head": "0" * 40, "head_path": "xml/remote.xml", "wire_changed": False},
                  "last_accepted_pair": PAIR, "proposed_pair": PAIR}
    review = {"implementation": {"disposition": "unchanged", "reason": "Synthetic serialization fixture"},
              "wire_review": "Synthetic unchanged contract", "behavior_review": "Synthetic test record",
              "client_upgrade": "None in fixture", "compatibility": "direct-switch", "breaking": False,
              "clients": [], "validations": selected, "expectations": [{
                  "source": "0" * 40 + ":xml/remote.xml", "case": entries[selected["interaction"]]["test_results"][0]["name"],
                  "kind": "interaction", "assertion": "Synthetic expectation, not remote-subsurface validation"}]}
    return {"schema_version": 2, "kind": PAIRING_KIND, "outcome": "pass", "status": "paired",
            "blocked_reasons": [], "unfinished": [], "failure_stage": None,
            "inventory_sha256": canonical_json_sha256(inventory), "manifest_sha256": canonical_json_sha256(manifest),
            "final_parent_head": manifest["final_parent_head"], "final_child_head": manifest["final_child_head"],
            "last_accepted_pair": PAIR, "candidate_pair": PAIR, "inspection": inspection, "review": review,
            "affected_clients": [], "target_ranges": {"implementation": {key: inventory["range"][key] for key in ("base", "head")},
                                                       "protocol": {"base": "0" * 40, "head": "0" * 40}},
            "validation_results": [{"id": row["id"], "outcome": row["outcome"]} for row in validations["entries"]]}
