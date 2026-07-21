"""Frozen overlay policy and three-way product-oracle verification."""

from __future__ import annotations

import hashlib
from typing import Any, Iterable

from .artifacts import canonical_bytes
from .git_objects import git_object_id
from .product_projection import project_product_payload
from .repository import GitRepository
from .tree_manifest import tree_entries


OVERLAY_RULES_VERSION = "commit-aligned-product-overlay-v1"
EXPECTED_EXACT_EXCLUSIONS = {
    ".gitattributes",
    "doc/ai/deckshell_waylib_commit_aligned_history_rewrite_plan.md",
    "doc/ai/waylibshared_7dc11a_regression_audit.md",
    "doc/skills/treeland-deckshell-sync/scripts/aligned_history_v2.py",
}
EXPECTED_PREFIX_EXCLUSIONS = {
    "doc/skills/treeland-deckshell-sync/scripts/aligned_history_v2/",
    "doc/treeland-sync/adaptations/",
}
EXPECTED_BOUNDED_PATTERNS = {
    (
        "doc/skills/treeland-deckshell-sync/tests/"
        "test_aligned_history_v2_",
        ".py",
    )
}


def validate_overlay_rules(
    rules: dict[str, Any], *, expected_artifact_sha256: str | None = None
) -> dict[str, int]:
    """Require the exact include-by-default overlay contract."""

    if rules.get("version") != OVERLAY_RULES_VERSION:
        raise ValueError("overlay rules version drift")
    if rules.get("policy") != "include-by-default-explicit-exclusions-only":
        raise ValueError("overlay policy drift")
    exact = _string_set(rules.get("exact_exclusions"), "exact exclusions")
    prefixes = _string_set(rules.get("prefix_exclusions"), "prefix exclusions")
    patterns = rules.get("bounded_patterns")
    if not isinstance(patterns, list):
        raise ValueError("overlay bounded patterns are invalid")
    bounded = {
        (str(row.get("prefix")), str(row.get("suffix")))
        for row in patterns
        if isinstance(row, dict)
    }
    broad = {"*", "**", "doc", "doc/", "doc/**", "compositor", "compositor/"}
    if exact & broad or prefixes & broad:
        raise ValueError("broad overlay exclusion is forbidden")
    if exact != EXPECTED_EXACT_EXCLUSIONS:
        raise ValueError("overlay exact exclusions drift")
    if prefixes != EXPECTED_PREFIX_EXCLUSIONS:
        raise ValueError("overlay prefix exclusions drift")
    if bounded != EXPECTED_BOUNDED_PATTERNS or len(bounded) != len(patterns):
        raise ValueError("overlay bounded patterns drift")
    if rules.get("forbidden_patterns") != ["doc/**"]:
        raise ValueError("overlay forbidden-pattern declaration drift")
    actual_hash = _self_hash(rules, "artifact_sha256")
    expected_hash = rules.get("artifact_sha256")
    if expected_hash is not None and expected_hash != actual_hash:
        raise ValueError("overlay rules canonical hash drift")
    if expected_artifact_sha256 and actual_hash != expected_artifact_sha256:
        raise ValueError("overlay rules frozen hash drift")
    return {
        "exact_exclusions": len(exact),
        "prefix_exclusions": len(prefixes),
        "bounded_patterns": len(bounded),
    }


def path_is_excluded(path: str, rules: dict[str, Any]) -> bool:
    """Apply exact, directory-prefix, and bounded filename exclusions."""

    if path in rules["exact_exclusions"]:
        return True
    if any(path.startswith(prefix) for prefix in rules["prefix_exclusions"]):
        return True
    return any(
        path.startswith(str(row["prefix"])) and path.endswith(str(row["suffix"]))
        for row in rules["bounded_patterns"]
    )


def build_product_entries(
    repo: GitRepository, tree: str, rules: dict[str, Any]
) -> list[dict[str, str]]:
    """Read the product entry list from one immutable Git tree."""

    validate_overlay_rules(rules)
    return [
        {
            "mode": entry["mode"],
            "kind": entry["kind"],
            "object": entry["object_id"],
            "path": entry["path"],
        }
        for entry in tree_entries(repo, tree)
        if not path_is_excluded(entry["path"], rules)
    ]


def compare_three_way_product_entries(
    master: Iterable[dict[str, Any]],
    corrected_v1: Iterable[dict[str, Any]],
    corrected_v2: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Require corrected-v1 and corrected-v2 to equal frozen master bytes."""

    rows = {
        "master": _canonical_entries(master),
        "corrected-v1": _canonical_entries(corrected_v1),
        "corrected-v2": _canonical_entries(corrected_v2),
    }
    if rows["corrected-v1"] != rows["master"] or rows["corrected-v2"] != rows["master"]:
        by_source = {
            source: {entry["path"]: entry for entry in entries}
            for source, entries in rows.items()
        }
        paths = sorted(
            path
            for path in set().union(*(set(value) for value in by_source.values()))
            if by_source["master"].get(path) != by_source["corrected-v1"].get(path)
            or by_source["master"].get(path) != by_source["corrected-v2"].get(path)
        )
        raise ValueError("product mismatch against frozen master: " + ", ".join(paths))
    digest = hashlib.sha256(canonical_bytes(rows["master"])).hexdigest()
    return {"entry_count": len(rows["master"]), "entries_sha256": digest, "mismatches": 0}


def project_master_product_entries(
    repo: GitRepository, entries: Iterable[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Project frozen master blobs and record the bounded rewrite authority."""

    projected: list[dict[str, Any]] = []
    authority: list[dict[str, Any]] = []
    for source in _canonical_entries(entries):
        row = dict(source)
        if source.get("kind") == "blob":
            payload = repo.cat_file("blob", str(source["object"]))
            result, reasons = project_product_payload(str(source["path"]), payload)
            if result != payload:
                object_id = git_object_id("blob", result)
                row["object"] = object_id
                authority.append(
                    {
                        "path": source["path"],
                        "mode": source["mode"],
                        "master_object": source["object"],
                        "candidate_object": object_id,
                        "candidate_sha256": hashlib.sha256(result).hexdigest(),
                        "reasons": reasons,
                    }
                )
        projected.append(row)
    return projected, authority


def validate_master_manifest(
    manifest: dict[str, Any],
    rules: dict[str, Any],
    *,
    expected_artifact_sha256: str | None = None,
) -> dict[str, Any]:
    """Verify the self-hashed frozen master product manifest."""

    validate_overlay_rules(rules)
    artifact_hash = _self_hash(manifest, "artifact_sha256")
    if manifest.get("artifact_sha256") != artifact_hash:
        raise ValueError("master product manifest canonical hash drift")
    if expected_artifact_sha256 and artifact_hash != expected_artifact_sha256:
        raise ValueError("master product manifest frozen hash drift")
    entries = _canonical_entries(manifest.get("entries", []))
    if manifest.get("entry_count") != len(entries):
        raise ValueError("master product entry count drift")
    entries_hash = hashlib.sha256(canonical_bytes(entries)).hexdigest()
    if manifest.get("entries_sha256") != entries_hash:
        raise ValueError("master product entry hash drift")
    if manifest.get("overlay_rules_sha256") != rules.get("artifact_sha256"):
        raise ValueError("master product overlay binding drift")
    return {"entry_count": len(entries), "entries_sha256": entries_hash}


def validate_product_evidence(
    evidence: dict[str, Any],
    master_entries: list[dict[str, Any]],
    projected_entries: list[dict[str, Any]],
    rewrite_authority: list[dict[str, Any]],
    *,
    expected_artifact_sha256: str | None = None,
) -> None:
    """Bind prior corrected-v1 evidence to independently recomputed entries."""

    artifact_hash = _self_hash(evidence, "artifact_sha256")
    if evidence.get("artifact_sha256") != artifact_hash:
        raise ValueError("corrected-v1 product evidence canonical hash drift")
    if expected_artifact_sha256 and artifact_hash != expected_artifact_sha256:
        raise ValueError("corrected-v1 product evidence frozen hash drift")
    canonical_master = _canonical_entries(master_entries)
    canonical_projected = _canonical_entries(projected_entries)
    if evidence.get("entries") != canonical_master:
        raise ValueError("corrected-v1 master product evidence entry drift")
    if evidence.get("entry_count") != len(canonical_master):
        raise ValueError("corrected-v1 product evidence count drift")
    if evidence.get("entries_sha256") != hashlib.sha256(
        canonical_bytes(canonical_master)
    ).hexdigest():
        raise ValueError("corrected-v1 master product hash drift")
    if evidence.get("actual_entries_sha256") != hashlib.sha256(
        canonical_bytes(canonical_projected)
    ).hexdigest():
        raise ValueError("corrected-v1 projected product hash drift")
    if evidence.get("rewrite_authority") != rewrite_authority:
        raise ValueError("corrected-v1 product rewrite authority drift")
    if evidence.get("rewrite_authority_count") != len(rewrite_authority):
        raise ValueError("corrected-v1 product rewrite authority count drift")


def _canonical_entries(entries: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for entry in entries:
        row = dict(entry)
        if "object_id" in row and "object" not in row:
            row["object"] = row.pop("object_id")
        rows.append(row)
    if any(not isinstance(row.get("path"), str) for row in rows):
        raise ValueError("product entry lacks a path")
    paths = [row["path"] for row in rows]
    if len(paths) != len(set(paths)):
        raise ValueError("product entry paths are not unique")
    return sorted(rows, key=lambda row: row["path"].encode("utf-8"))


def _string_set(value: Any, label: str) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"overlay {label} are invalid")
    if len(value) != len(set(value)):
        raise ValueError(f"overlay {label} contain duplicates")
    return set(value)


def _self_hash(payload: dict[str, Any], field: str) -> str:
    unhashed = dict(payload)
    unhashed.pop(field, None)
    return hashlib.sha256(canonical_bytes(unhashed)).hexdigest()
