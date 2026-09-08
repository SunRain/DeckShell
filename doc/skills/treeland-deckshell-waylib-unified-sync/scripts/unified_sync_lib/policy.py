"""DeckShell path-policy loading and deterministic path decisions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Set, Tuple


@dataclass(frozen=True)
class PathDecision:
    """Describe one source path's DeckShell destination decision."""

    source: str
    category: str
    target: Optional[str]
    policy_key: Optional[str]


def load_policy(path: Path) -> Dict[str, Any]:
    """Load the first fenced JSON object from a DeckShell path policy."""

    content = path.read_text(encoding="utf-8")
    marker = "```json\n"
    start = content.find(marker)
    if start < 0:
        raise ValueError(f"path policy has no fenced JSON object: {path}")
    start += len(marker)
    end = content.find("\n```", start)
    if end < 0:
        raise ValueError(f"path policy JSON fence is not closed: {path}")
    policy = json.loads(content[start:end])
    if not isinstance(policy, dict) or policy.get("version") != 1:
        raise ValueError(f"unsupported path policy version: {policy.get('version')}")
    return policy


def _match(
    path: str,
    directories: Mapping[str, str],
    files: Mapping[str, str],
) -> Optional[Tuple[str, str]]:
    if path in files:
        return path, str(files[path])
    for source_root, target_root in directories.items():
        if path == source_root:
            return str(source_root), str(target_root)
        prefix = f"{source_root}/"
        if path.startswith(prefix):
            return str(source_root), f"{target_root}/{path[len(prefix):]}"
    return None


def decide_path(path: str, policy: Mapping[str, Any], approvals: Set[str]) -> PathDecision:
    """Classify one source path and calculate its canonical parent target."""

    for section_name, category in (("mapped", "mapped"), ("root_owned", "root-owned")):
        section = policy.get(section_name, {})
        match = _match(path, section.get("directories", {}), section.get("files", {}))
        if match:
            return PathDecision(path, category, match[1], match[0])

    excluded = policy.get("excluded", {})
    if path in set(excluded.get("files", [])):
        return PathDecision(path, "excluded", None, path)
    for root in excluded.get("directories", []):
        if path == root or path.startswith(f"{root}/"):
            return PathDecision(path, "excluded", None, str(root))

    review = policy.get("review_only", {})
    match = _match(path, review.get("directories", {}), review.get("files", {}))
    if match:
        category = "root-owned" if match[0] in approvals else "review-only"
        return PathDecision(path, category, match[1], match[0])
    return PathDecision(path, "unknown", None, None)


def decision_payload(decision: Optional[PathDecision]) -> Optional[Dict[str, Any]]:
    """Serialize a path decision for inventory evidence."""

    if decision is None:
        return None
    return {
        "source": decision.source,
        "category": decision.category,
        "target": decision.target,
        "policy_key": decision.policy_key,
    }
