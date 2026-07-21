"""Derive v2 message inputs from frozen v1 manifest entries."""

from __future__ import annotations

from typing import Any

from .message import parse_message, render_message


def build_treeland_message_input(
    entry: dict[str, Any], source_changed_paths: list[str]
) -> dict[str, Any]:
    """Build one self-contained Treeland message input."""

    source = str(entry.get("normalized_treeland_commit", ""))
    classification = str(entry.get("target_kind", "")).removeprefix("treeland-")
    if entry.get("legacy_deckshell_target") is not None:
        result = _upgrade_legacy_treeland_message(entry, source)
    else:
        if classification != "dependency-only":
            raise ValueError(f"Treeland entry lacks legacy target: {source}")
        metadata = entry.get("metadata", {})
        result = {
            "schema": "treeland",
            "subject_body": str(metadata.get("message", "")),
            "source_commit": source,
            "classification": classification,
            "action": "dependency-gitlink",
            "drop_files": source_changed_paths,
            "path_mapping": ["none"],
            "adaptation_paths": ["none"],
            "adaptation_notes": [
                "Dependency changes are represented by WaylibShared commit "
                f"{entry.get('waylib_target')} through the DeckShell gitlink."
            ],
        }
    result["legacy_treeland_commit"] = entry.get("legacy_treeland_commit")
    result["treeland_patch_id"] = entry.get("treeland_patch_id")
    result["waylib_commit"] = entry.get("waylib_target")
    if result["legacy_treeland_commit"] is None:
        result.pop("legacy_treeland_commit")
        result.pop("treeland_patch_id")
    if result["waylib_commit"] is None:
        result.pop("waylib_commit")
    if result["classification"] != classification:
        raise ValueError(f"Treeland classification drift: {source}")
    return parse_message(render_message(result), "treeland")


def build_waylib_message_input(entry: dict[str, Any]) -> dict[str, Any]:
    """Build a local or convergence WaylibShared message input."""

    classification = entry.get("local_node_kind", "dependency-convergence")
    result: dict[str, Any] = {
        "schema": "waylib",
        "subject_body": str(entry.get("metadata", {}).get("message", "")),
        "classification": classification,
        "action": "local-gitlink",
        "waylib_commit": entry.get("waylib_target"),
    }
    absorbed = entry.get("absorbed_waylib_commits", [])
    if absorbed:
        if len(absorbed) != 1:
            raise ValueError("WaylibShared local entry must absorb at most one parent")
        result["absorbed_waylib_commit"] = absorbed[0]
    return parse_message(render_message(result), "waylib")


def build_adaptation_message_input(
    entry: dict[str, Any], paths: list[str]
) -> dict[str, Any]:
    """Build an adaptation message without retired-branch source trailers."""

    index = int(entry["ordered_index"])
    classification = str(entry["action"])
    if index == 329:
        classification = "regenerate"
    derivation = "patch-equivalent"
    if index == 329:
        derivation = "selective-composite"
    elif classification == "regenerate":
        derivation = "regenerate"
    notes = {
        316: "Regenerate the WaylibShared regression audit from the sealed Treeland target prefix.",
        329: "Persist the exact v2 renderer, parser, verifier, generators, and tests used by both object previews.",
        330: "Regenerate the implementation contract, Git attributes, and 58 SHA-named adaptation records from the sealed Treeland target prefix.",
    }
    note = notes.get(index)
    if note is None and classification == "paired-dependency-fix":
        note = "Preserve the paired WaylibShared gitlink and keyboard-group lifecycle regression fix."
    if note is None:
        note = "Preserve the verified tree transition and its product or tooling behavior."
    result: dict[str, Any] = {
        "schema": "adaptation",
        "subject_body": str(entry.get("metadata", {}).get("message", "")),
        "classification": classification,
        "action": classification,
        "paths": paths,
        "notes": [note],
        "derivation": derivation,
    }
    if classification == "paired-dependency-fix":
        result["waylib_commit"] = entry.get("waylib_target")
    return parse_message(render_message(result), "adaptation")


def _upgrade_legacy_treeland_message(
    entry: dict[str, Any], source: str
) -> dict[str, Any]:
    metadata = entry.get("metadata", {})
    message = str(metadata.get("message", ""))
    trailer = f"Treeland-Commit: {source}\n"
    if message.count(trailer) != 1:
        raise ValueError(f"legacy Treeland source trailer is not unique: {source}")
    trailers = [
        "Treeland-Remote: treeland",
        "Treeland-Remote-Branch: master",
        "Treeland-Tracking-Ref: refs/remotes/treeland/master",
        f"Treeland-Commit: {source}",
    ]
    for key, label in (
        ("legacy_treeland_commit", "Legacy-Treeland-Commit"),
        ("treeland_patch_id", "Treeland-Patch-ID"),
        ("waylib_target", "WaylibShared-Commit"),
    ):
        value = entry.get(key)
        if value is not None:
            trailers.append(f"{label}: {value}")
    replacement = "\n".join((*trailers, ""))
    upgraded = message.replace(trailer, replacement)
    return parse_message(upgraded.encode("utf-8"), "treeland")
