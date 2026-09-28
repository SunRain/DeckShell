"""将原方案准备成仓内只读副本；不改原文事实，不复制运行现场。"""

from __future__ import annotations

import re
from pathlib import Path

from .record_context import require


def plan_documents(context, directory):
    """在写任何仓库前准备两份副本，已有副本由统一写入预检保护。"""
    directory = Path(directory).resolve()
    documents = {}
    for name in ("plan.md", "prd.md"):
        path = directory / name
        require(path.is_file() and not path.is_symlink(), "原方案缺少普通 plan.md/prd.md 文件")
        source = path.read_text(encoding="utf-8")
        require(not source.startswith("\ufeff"), "原方案不应带 BOM")

        def link(match):
            label, href = match.groups()
            if href.startswith(("#", "https://", "http://", "mailto:")):
                return match[0]
            target, separator, anchor = href.partition("#")
            absolute = (directory / target).resolve()
            if absolute.parent == directory and absolute.name in ("plan.md", "prd.md"):
                return f"[{label}]({absolute.name}{separator}{anchor})"
            portable = context.portable(str(absolute)) + (separator + anchor if separator else "")
            return f"{label}（外层历史资料：`{portable}`；未随仓携带）"

        text = re.sub(r"\[([^\]\n]+)\]\(([^)\n]+)\)", link, source)
        text = context.portable(text)
        require(not re.search(r"/(?:home|Users)/[^\s`]+", text), "方案副本仍含本机个人路径")
        origin = context.portable(str(path))
        header = ("> 仓内参考副本；权威原文：`" + origin + "`。\n"
                  "> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。\n\n")
        documents[name] = header + text
    return documents
