"""Types shared by replay orchestration modules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


GITLINK_PATH = "3rdparty/waylib-shared"


class ReplayBlocked(RuntimeError):
    """Raised after a replay safety or deterministic execution gate blocks."""


@dataclass
class ReplayRequest:
    """Immutable-input request for a child-first replay run."""

    source_repo: Path
    parent_worktree: Path
    child_worktree: Path
    parent_base: str
    child_base: str
    inventory: Dict[str, Any]
    artifact_root: Path
    journal_path: Path
    manifest_path: Path
    waylib_evidence_path: Path
    parent_evidence_path: Path
    run_id: str
    refs_doc: str
    decisions: Dict[str, Any]
    allow_ephemeral_artifacts: bool = False
    gitlink_path: str = GITLINK_PATH
    wlroots_repo: Optional[Path] = None
    wlroots_worktree: Optional[Path] = None
    wlroots_base: Optional[str] = None
    wlroots_target_ref: Optional[str] = None
    wlroots_submodule_url: Optional[str] = None
    wlroots_baseline_proof: Optional[Dict[str, Any]] = None

    @property
    def wlroots_evidence_path(self) -> Path:
        return self.artifact_root / "wlroots-evidence.json"
