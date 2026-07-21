"""Bind compile-atomic ledgers to actual v1 and v2 Git objects."""

from __future__ import annotations

import hashlib
import subprocess
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from .atomic_verifiers.protocol_signature import generated_signatures
from .repository import GitRepository
from .tree_manifest import gitlink_object, tree_diff_paths


def verify_protocol_bindings(
    repo: GitRepository,
    records: Sequence[Mapping[str, Any]],
    ledger: Mapping[str, Any],
) -> dict[str, int]:
    """Verify protocol blobs, signatures, consumers, and terminal state."""

    by_index = _records(records)
    grouped: dict[tuple[int, str], list[Mapping[str, Any]]] = defaultdict(list)
    by_path: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for component in ledger.get("components", ()):
        path = str(component["target_path"])
        grouped[(int(component["owner_index"]), path)].append(component)
        by_path[path].append(component)
    for (owner, path), components in sorted(grouped.items()):
        record = _require_record(by_index, owner)
        commit = _commit(record)
        changed = set(tree_diff_paths(repo, _parent(record), commit))
        expected = _terminal_component(components)
        missing_consumers = set(expected.get("consumer_paths", ())) - changed
        if missing_consumers:
            raise ValueError(
                f"protocol consumer paths differ at {owner}: {sorted(missing_consumers)}"
            )
        _verify_protocol_blob(repo, commit, path, expected, owner)
    head = _commit(by_index[max(by_index)])
    for path, components in sorted(by_path.items()):
        terminal = _terminal_component(components)
        if _blob_id(repo, head, path) != terminal.get("result_blob"):
            raise ValueError(f"protocol terminal result differs: {path}")
    return {
        "component_count": len(ledger.get("components", ())),
        "owner_path_binding_count": len(grouped),
        "terminal_path_binding_count": len(by_path),
        "blob_mismatch": 0,
        "signature_mismatch": 0,
        "consumer_path_mismatch": 0,
    }


def verify_waylib_bindings(
    repo: GitRepository,
    waylib_repo: GitRepository,
    records: Sequence[Mapping[str, Any]],
    ledger: Mapping[str, Any],
) -> dict[str, int]:
    """Verify every capability is reachable from its owner's exact gitlink."""

    by_index = _records(records)
    components = [
        component
        for component in ledger.get("components", ())
        if component.get("kind") == "waylib-capability"
    ]
    for component in components:
        owner = int(component["owner_index"])
        commit = _commit(_require_record(by_index, owner))
        actual = gitlink_object(repo, commit, "3rdparty/waylib-shared")
        required = str(component["payload"]["gitlink_after"])
        if not is_ancestor(waylib_repo, required, actual):
            raise ValueError(
                f"Waylib capability is unavailable at {owner}: {required}"
            )
    return {
        "component_count": len(components),
        "owner_count": len({int(item["owner_index"]) for item in components}),
        "ancestry_failure": 0,
    }


def verify_gitlink_bindings(
    repo: GitRepository,
    records: Sequence[Mapping[str, Any]],
    manifest_entries: Sequence[Mapping[str, Any]],
) -> dict[str, int]:
    """Require each actual v2 node to carry the candidate's exact gitlink."""

    for entry, record in zip(manifest_entries, records, strict=True):
        actual = gitlink_object(repo, _commit(record), "3rdparty/waylib-shared")
        if actual != entry.get("gitlink_after"):
            raise ValueError(f"v2 gitlink drift at {entry['ordered_index']}: {actual}")
    return {"node_count": len(records), "gitlink_mismatch": 0}


def verify_protocol_source_policy(
    repo: GitRepository, records: Sequence[Mapping[str, Any]]
) -> dict[str, int]:
    """Scan each actual history node for executable external protocol lookup."""

    patterns = (
        r"find_package[[:space:]]*\([[:space:]]*TreelandProtocols",
        r"TREELAND_PROTOCOLS_DATA_DIR",
        r"/usr/share/treeland-protocols",
    )
    exclusions = (
        ":!doc/**",
        ":!compositor-bak/**",
        ":!compositor/tests/test_protocol_source_policy/**",
        ":!**/*.md",
        ":!**/*.txt",
        ":!**/*.json",
        ":!**/*.yaml",
        ":!**/*.yml",
        ":!**/*.patch",
    )
    for record in records:
        commit = _commit(record)
        arguments = ["grep", "-I", "-n", "-E"]
        for pattern in patterns:
            arguments.extend(("-e", pattern))
        try:
            output = repo.run(*arguments, commit, "--", *exclusions)
        except subprocess.CalledProcessError as error:
            if error.returncode == 1:
                continue
            raise ValueError(f"protocol source scan failed at {commit}") from error
        detail = output.decode("utf-8", errors="replace").splitlines()[0]
        raise ValueError(f"external protocol source at {commit}: {detail}")
    return {
        "scanned_commit_count": len(records),
        "external_protocol_lookup_count": 0,
    }


def verify_remediation_bindings(
    repo: GitRepository,
    v1_records: Sequence[Mapping[str, Any]],
    v2_records: Sequence[Mapping[str, Any]],
    ownership: Mapping[str, Any],
    bundle_ledger: Mapping[str, Any],
) -> dict[str, int]:
    """Recheck remediation coverage and final local/obsolete contracts."""

    expected = {str(item["component_id"]) for item in ownership["components"]}
    observed: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for record in v1_records:
        for item in record.get("remediation_components", ()):
            observed[str(item["component_id"])].append(
                (int(record["ordered_index"]), str(item["status"]))
            )
    if set(observed) != expected:
        raise ValueError("remediation component coverage differs")
    atomic_owners = {
        str(item["payload"]["component_id"]): int(item["owner_index"])
        for item in bundle_ledger.get("components", ())
        if item.get("kind") == "remediation-component"
    }
    if set(atomic_owners) != expected:
        raise ValueError("remediation atomic owner coverage differs")
    terminal = {"applied", "already-applied", "already-absent", "obsolete-satisfied"}
    for component_id in expected:
        if not any(
            status in terminal and index >= atomic_owners[component_id]
            for index, status in observed[component_id]
        ):
            raise ValueError(f"remediation terminal proof differs: {component_id}")
    head = _commit(v2_records[-1])
    for gate in ownership.get("occurrence_gates", ()):
        text = _blob(repo, head, str(gate["path"])).decode("utf-8")
        if text.count(str(gate["needle"])) > int(gate["maximum"]):
            raise ValueError(f"obsolete occurrence remains: {gate['gate_id']}")
    for component in ownership.get("local_contract_components", ()):
        text = _blob(repo, head, str(component["path"])).decode("utf-8")
        before = str(component.get("before_text", ""))
        after = str(component.get("after_text", ""))
        if after and after not in text:
            raise ValueError(f"local contract post-image is missing: {component['component_id']}")
        if not after and before and before in text:
            raise ValueError(f"local contract cleanup is missing: {component['component_id']}")
    return {
        "component_count": len(expected),
        "atomic_owner_binding_count": len(atomic_owners),
        "occurrence_gate_count": len(ownership.get("occurrence_gates", ())),
        "local_contract_component_count": len(
            ownership.get("local_contract_components", ())
        ),
        "obsolete_occurrences": 0,
        "local_contract_loss": 0,
    }


def is_ancestor(repo: GitRepository, older: str, newer: str) -> bool:
    """Return ancestry without treating a negative query as a Git failure."""

    try:
        repo.run("merge-base", "--is-ancestor", older, newer)
        return True
    except subprocess.CalledProcessError as error:
        if error.returncode == 1:
            return False
        raise


def _verify_protocol_blob(
    repo: GitRepository,
    commit: str,
    path: str,
    component: Mapping[str, Any],
    owner: int,
) -> None:
    expected_blob = component.get("result_blob")
    if _blob_id(repo, commit, path) != expected_blob:
        raise ValueError(f"protocol result blob differs at {owner}: {path}")
    if expected_blob is None:
        return
    payload = _blob(repo, commit, path)
    if hashlib.sha256(payload).hexdigest() != component.get("result_sha256"):
        raise ValueError(f"protocol result hash differs at {owner}: {path}")
    expected = component.get(
        "generated_signatures_after", component.get("generated_signatures", ())
    )
    if list(generated_signatures(payload)) != list(expected):
        raise ValueError(f"protocol signature differs at {owner}: {path}")


def _records(
    records: Sequence[Mapping[str, Any]],
) -> dict[int, Mapping[str, Any]]:
    result = {int(record["ordered_index"]): record for record in records}
    if len(result) != len(records):
        raise ValueError("history mapping has duplicate indices")
    return result


def _require_record(
    records: Mapping[int, Mapping[str, Any]], index: int
) -> Mapping[str, Any]:
    if index not in records:
        raise ValueError(f"history owner is missing: {index}")
    return records[index]


def _commit(record: Mapping[str, Any]) -> str:
    return str(record.get("new_commit") or record["commit"])


def _parent(record: Mapping[str, Any]) -> str:
    return str(record.get("new_parent") or record["parent"])


def _terminal_component(
    components: Sequence[Mapping[str, Any]],
) -> Mapping[str, Any]:
    return max(
        components,
        key=lambda item: (
            int(item.get("source_sequence", 0)),
            int(item.get("component_sequence", 0)),
        ),
    )


def _blob_id(repo: GitRepository, commit: str, path: str) -> str | None:
    payload = repo.run("ls-tree", "-z", commit, "--", path).rstrip(b"\0")
    if not payload:
        return None
    metadata, separator, raw_path = payload.partition(b"\t")
    if not separator or raw_path.decode("utf-8") != path:
        raise ValueError(f"tree path lookup is ambiguous: {commit}:{path}")
    mode, kind, object_id = metadata.decode("ascii").split()
    if kind != "blob" or mode not in {"100644", "100755"}:
        raise ValueError(f"tree path is not a blob: {commit}:{path}")
    return object_id


def _blob(repo: GitRepository, commit: str, path: str) -> bytes:
    return repo.run("show", f"{commit}:{path}")
