"""Path-normalized semantic patch section comparison."""

from __future__ import annotations

import hashlib
import json
import shlex
from typing import Any


def _section_digest(tokens: list[str]) -> str:
    encoded = json.dumps(tokens, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _header_path(line: str) -> str:
    fields = shlex.split(line)
    if len(fields) != 4:
        raise ValueError(f"malformed patch header: {line}")
    path = fields[3]
    return path[2:] if path.startswith("b/") else path


def _semantic_token(line: str, in_binary: bool) -> str | None:
    if line.startswith(("new file mode ", "deleted file mode ", "old mode ", "new mode ")):
        return line
    if line == "GIT binary patch":
        return line
    if in_binary:
        return line
    if line.startswith("+") and not line.startswith("+++"):
        return line
    if line.startswith("-") and not line.startswith("---"):
        return line
    return None


def parse_patch_sections(content: str) -> dict[str, dict[str, Any]]:
    """Parse a Git patch into path-keyed semantic change tokens."""

    sections: dict[str, dict[str, Any]] = {}
    path = ""
    tokens: list[str] = []
    in_binary = False

    def finish() -> None:
        if path:
            sections[path] = {
                "tokens": list(tokens),
                "sha256": _section_digest(tokens),
            }

    for line in content.splitlines():
        if line.startswith("diff --git "):
            finish()
            path = _header_path(line)
            tokens = []
            in_binary = False
            continue
        token = _semantic_token(line, in_binary)
        if token is not None:
            tokens.append(token)
        if line == "GIT binary patch":
            in_binary = True
    finish()
    return sections


def compare_patch_sections(
    source_sections: dict[str, dict[str, Any]],
    target_sections: dict[str, dict[str, Any]],
    path_map: dict[str, str],
) -> dict[str, dict[str, Any]]:
    """Compare mapped source and target sections without auto-approving results."""

    comparisons = {}
    for source_path, target_path in path_map.items():
        source = source_sections.get(source_path)
        target = target_sections.get(target_path)
        comparisons[target_path] = {
            "source_path": source_path,
            "source_patch_sha256": source.get("sha256") if source else None,
            "target_patch_sha256": target.get("sha256") if target else None,
            "delta_equivalent": bool(
                source and target and source.get("tokens") == target.get("tokens")
            ),
        }
    return comparisons
