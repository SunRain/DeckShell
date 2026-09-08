from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional


def run(repo: Path, *args: str, env: Optional[Dict[str, str]] = None) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, **(env or {})},
    )
    return completed.stdout.strip()


def init_repo(path: Path) -> Path:
    path.mkdir(parents=True)
    subprocess.run(
        ["git", "init", "--initial-branch=main", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    run(path, "config", "user.name", "Test User")
    run(path, "config", "user.email", "test@example.invalid")
    return path


def init_repo_with_separate_git_dir(path: Path, git_dir: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "git",
            "init",
            "--initial-branch=main",
            f"--separate-git-dir={git_dir}",
            str(path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    run(path, "config", "user.name", "Test User")
    run(path, "config", "user.email", "test@example.invalid")
    return path


def add_worktree(repo: Path, path: Path, branch: str, start: str) -> Path:
    run(repo, "worktree", "add", "-b", branch, str(path), start)
    run(path, "config", "user.name", "Test User")
    run(path, "config", "user.email", "test@example.invalid")
    return path


def commit_files(
    repo: Path,
    files: Dict[str, Optional[str]],
    message: str,
    *,
    timestamp: str = "2026-01-01T00:00:00+00:00",
) -> str:
    for name, content in files.items():
        target = repo / name
        if content is None:
            target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    run(repo, "add", "-A")
    env = {"GIT_AUTHOR_DATE": timestamp, "GIT_COMMITTER_DATE": timestamp}
    run(repo, "commit", "-m", message, env=env)
    return run(repo, "rev-parse", "HEAD")


def write_policy(path: Path) -> Path:
    policy = {
        "version": 1,
        "mapped": {
            "directories": {"src": "compositor/src", "tests": "compositor/tests"},
            "files": {"CMakeLists.txt": "compositor/CMakeLists.txt"},
        },
        "root_owned": {
            "directories": {"protocols": "protocols"},
            "files": {".clang-format": ".clang-format"},
        },
        "excluded": {"directories": ["qwlroots", "waylib", "vendor"], "files": []},
        "review_only": {
            "directories": {".github": ".github"},
            "files": {".gitmodules": ".gitmodules"},
        },
    }
    path.write_text(
        "# Policy\n\n```json\n" + json.dumps(policy, indent=2) + "\n```\n",
        encoding="utf-8",
    )
    return path


def ctest_fixture(root: Path, name: str, command, cwd: str, total: int = 1):
    """生成报告单测的明确合成工件；真实 CTest 行为另有集成测试覆盖。"""
    from unified_sync_lib.artifacts import write_artifact
    from unified_sync_lib.ctest_results import parse_ctest, discovery_command

    cases = "".join(f"{i}/{total} Test #{i}: case_{i} ........ Passed 0.01 sec\n" for i in range(1, total + 1))
    output = (cases + f"100% tests passed out of {total}\n").encode() if total else b"No tests were found!!!\n"
    tests = [{"id": i, "name": f"case_{i}"} for i in range(1, total + 1)]
    discovery = json.dumps({"kind": "ctestInfo", "tests": [{"name": v["name"]} for v in tests]}).encode()
    return {
        **parse_ctest(output, 0),
        "log": write_artifact(root, f"logs/{name}.log", output),
        "test_discovery": {
            "command": discovery_command(command, Path(cwd)), "cwd": cwd,
            "exit_code": 0, "tests": tests,
            "log": write_artifact(root, f"logs/{name}-discovery.json", discovery),
        },
    }
