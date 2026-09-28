"""按仓同步记录的调用方输入、仓库身份和可移植定位。"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Optional

from .artifacts import resolve_artifact_path
from .git_ops import canonical_repo, common_git_dir, read_json
from .schema import is_full_sha

ROLES = {"parent": "P / DeckShell", "child": "C / waylib-shared", "wlroots": "R / wlroots"}
LINKS = {"parent": ("3rdparty/waylib-shared", "child"), "child": ("3rdparty/wlroots", "wlroots")}


def require(condition: bool, message: str) -> None:
    """输入不满足记录合同就明确失败，不生成不完整的文档。"""
    if not condition:
        raise ValueError(message)


def relative_name(value: str) -> str:
    """验证文档和外部资料定位使用的安全相对路径。"""
    require(isinstance(value, str) and bool(value), "路径必须为非空字符串")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts
            and str(path) == value and value != "."
            and not any(ord(c) < 32 or ord(c) == 127 for c in value), f"路径越界或不规范：{value}")
    return value


@dataclass
class RecordContext:
    """一次纯记录生成调用；不携带 replay 或 ref 更新能力。"""

    source: Path
    repos: Dict[str, Path]
    batch: str
    evidence_root: Path
    evidence_label: str
    history: Dict[str, Any] = field(default_factory=dict)
    plan_documents: Dict[str, str] = field(default_factory=dict)

    def target(self, lane: str, old: Optional[str]) -> Optional[str]:
        """映射历史目标，区间外基线和无改写输入保持原身份。"""
        if old is None:
            return None
        require(is_full_sha(old), f"{lane} 不是完整目标 SHA：{old}")
        return self.history.get(lane, {}).get("mapping", {}).get(old, old)

    def external(self, node_path: str, file: str = "") -> str:
        """给出外层历史资料标识，不伪装成当前仓库链接。"""
        suffix = "/".join(v for v in (self.evidence_label, node_path, file) if v)
        return f"外层历史资料：`{suffix}`"

    def node_root(self, value: str) -> Path:
        """只允许读取显式证据根内的节点资料。"""
        return resolve_artifact_path(self.evidence_root, relative_name(value))

    def portable(self, text: str) -> str:
        """显示原证据文字时使用仓库/证据标识替代已知本机根。"""
        replacements = {str(self.evidence_root): self.evidence_label}
        replacements.update({str(repo): ROLES[lane] for lane, repo in self.repos.items()})
        replacements[str(self.source)] = "Treeland 来源仓库"
        shared = os.path.commonpath([str(self.evidence_root), str(self.source),
                                     *(str(repo) for repo in self.repos.values())])
        if len(Path(shared).parts) > 2:
            replacements[shared] = "外层工作区（历史）"
        for original in sorted(replacements, key=len, reverse=True):
            text = text.replace(original, replacements[original])
        return text


def make_context(source: Path, parent: Path, child: Path, wlroots: Optional[Path],
                 batch: str, evidence_root: Path, evidence_label: str,
                 history_map: Optional[Path]) -> RecordContext:
    """核对真正的仓库根及旧新映射输入；空子目录不能冒充 R。"""
    require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", batch))
            and ".." not in batch, "同步批次必须是安全的单目录标识")
    repos = {"parent": canonical_repo(parent), "child": canonical_repo(child)}
    if wlroots is not None:
        repos["wlroots"] = canonical_repo(wlroots)
    identities = [common_git_dir(repo) for repo in repos.values()]
    require(len(set(identities)) == len(identities), "P/C/R 必须是独立对象库")
    context = RecordContext(canonical_repo(source), repos, batch, evidence_root.resolve(),
                            relative_name(evidence_label))
    require(context.evidence_root.is_dir(), "证据根不存在")
    if history_map is not None:
        payload = read_json(history_map)
        require(payload.get("batch") == batch, "旧新映射的批次错配")
        require(set(payload.get("repositories", {})) == set(repos), "旧新映射的仓库集合错配")
        for lane, info in payload["repositories"].items():
            require(isinstance(info, dict), f"{lane} 映射必须为对象")
            pairs = info.get("commits")
            require(isinstance(pairs, list), f"{lane} 映射不是列表")
            require(all(isinstance(v, dict) and is_full_sha(v.get("old")) and is_full_sha(v.get("new")) for v in pairs),
                    f"{lane} 映射必须使用完整 SHA")
            mapping = {v["old"]: v["new"] for v in pairs}
            require(len(mapping) == len(pairs) == len(set(mapping.values())), f"{lane} 映射不是一一对应")
            require(all(is_full_sha(info.get(k)) for k in ("base", "old_head", "new_head")),
                    f"{lane} 映射端点无效")
            context.history[lane] = {**info, "mapping": mapping}
    return context


def check_identity(context: RecordContext, identity: dict) -> None:
    """旧 evidence 必须绑定调用方提供的真实对象库。"""
    require(common_git_dir(canonical_repo(Path(identity["source_repo"])))
            == common_git_dir(context.source), "来源仓库身份错配")
    for lane in ("parent", "child"):
        require(Path(identity[f"{lane}_common_git_dir"]).resolve()
                == common_git_dir(context.repos[lane]), f"{lane} 仓库身份错配")
    nested = identity.get("wlroots")
    if nested:
        require("wlroots" in context.repos, "缺少独立 R 仓库")
        require(Path(nested["common_git_dir"]).resolve() == common_git_dir(context.repos["wlroots"]),
                "R 仓库身份错配")
