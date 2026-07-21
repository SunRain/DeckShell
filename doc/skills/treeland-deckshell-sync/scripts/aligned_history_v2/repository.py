"""Read-only source access and isolated Git object-directory operations."""

from __future__ import annotations

import os
import subprocess
import zlib
from pathlib import Path

from .git_objects import git_object_id
from .tree_transition import TreeChange


ZERO_OBJECT = "0" * 40


class GitRepository:
    """Run Git with an optional isolated writable object directory."""

    def __init__(
        self,
        repo: Path,
        *,
        object_directory: Path | None = None,
        alternates: tuple[Path, ...] = (),
    ) -> None:
        self.repo = repo.resolve()
        self._object_directory = object_directory.resolve() if object_directory else None
        self.alternates = tuple(path.resolve() for path in alternates)
        if self._object_directory is not None:
            self._object_directory.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        *args: str,
        input_data: bytes | None = None,
        index_file: Path | None = None,
    ) -> bytes:
        """Run Git under this repository's object and optional index boundary."""

        environment = os.environ.copy()
        if self._object_directory is not None:
            environment["GIT_OBJECT_DIRECTORY"] = str(self._object_directory)
            environment["GIT_ALTERNATE_OBJECT_DIRECTORIES"] = os.pathsep.join(
                str(path) for path in self.alternates
            )
        if index_file is not None:
            environment["GIT_INDEX_FILE"] = str(index_file.resolve())
        completed = subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
        )
        return completed.stdout

    def object_directory(self) -> Path:
        """Return the effective writable Git object directory."""

        if self._object_directory is not None:
            return self._object_directory
        raw = self.run("rev-parse", "--git-path", "objects").decode().strip()
        path = Path(raw)
        return (path if path.is_absolute() else self.repo / path).resolve()

    def cat_file(self, kind: str, object_id: str) -> bytes:
        """Read an object's uncompressed payload with strict type checking."""

        return self.run("cat-file", kind, object_id)

    def tree_id(self, revision: str) -> str:
        """Resolve a revision or commit to its tree object ID."""

        return self.run("rev-parse", f"{revision}^{{tree}}").decode().strip()

    def raw_transition(self, old: str, new: str) -> bytes:
        """Return the canonical no-rename raw transition between revisions."""

        return self.run(
            "diff-tree",
            "--no-commit-id",
            "--raw",
            "-r",
            "-z",
            "--no-renames",
            "--abbrev=40",
            old,
            new,
        )

    def replay_transition(
        self,
        parent_tree: str,
        changes: tuple[TreeChange, ...],
        index_file: Path,
    ) -> str:
        """Apply one exact transition to a parent tree using an isolated index."""

        self._require_isolated_objects()
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.unlink(missing_ok=True)
        self.run("read-tree", parent_tree, index_file=index_file)
        for change in changes:
            current = self._index_entry(index_file, change.path)
            expected = None
            if change.old_mode != "000000" or change.old_object != ZERO_OBJECT:
                expected = (change.old_mode, change.old_object)
            if current != expected:
                raise ValueError(
                    f"transition old value mismatch for {change.path}: "
                    f"expected {expected}, got {current}"
                )
            if change.new_mode == "000000" and change.new_object == ZERO_OBJECT:
                self.run(
                    "update-index",
                    "--force-remove",
                    "--",
                    change.path,
                    index_file=index_file,
                )
            else:
                self.run(
                    "update-index",
                    "--add",
                    "--cacheinfo",
                    f"{change.new_mode},{change.new_object},{change.path}",
                    index_file=index_file,
                )
        return self.run("write-tree", index_file=index_file).decode().strip()

    def apply_files(
        self,
        parent_tree: str,
        files: dict[str, bytes | None],
        index_file: Path,
    ) -> str:
        """Apply an exact file overlay to a parent tree in path order."""

        self._require_isolated_objects()
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.unlink(missing_ok=True)
        self.run("read-tree", parent_tree, index_file=index_file)
        for path, content in sorted(files.items(), key=lambda item: item[0].encode("utf-8")):
            if content is None:
                self.run(
                    "update-index", "--force-remove", "--", path, index_file=index_file
                )
                continue
            object_id = self.write_object("blob", content)
            self.run(
                "update-index",
                "--add",
                "--cacheinfo",
                f"100644,{object_id},{path}",
                index_file=index_file,
            )
        return self.run("write-tree", index_file=index_file).decode().strip()

    def write_object(self, kind: str, payload: bytes) -> str:
        """Write a loose object only to the configured isolated directory."""

        self._require_isolated_objects()
        object_id = git_object_id(kind, payload)
        destination = self._object_directory / object_id[:2] / object_id[2:]
        if destination.exists():
            existing = zlib.decompress(destination.read_bytes())
            expected = f"{kind} {len(payload)}\0".encode("ascii") + payload
            if existing != expected:
                raise ValueError(f"loose object collision: {object_id}")
            return object_id
        destination.parent.mkdir(parents=True, exist_ok=True)
        raw = f"{kind} {len(payload)}\0".encode("ascii") + payload
        temporary = destination.with_suffix(".tmp")
        temporary.write_bytes(zlib.compress(raw))
        temporary.replace(destination)
        return object_id

    def _index_entry(self, index_file: Path, path: str) -> tuple[str, str] | None:
        output = self.run("ls-files", "--stage", "-z", "--", path, index_file=index_file)
        if not output:
            return None
        records = output.rstrip(b"\0").split(b"\0")
        if len(records) != 1:
            raise ValueError(f"index contains multiple stages for {path}")
        metadata, separator, actual_path = records[0].partition(b"\t")
        if not separator or actual_path.decode("utf-8") != path:
            raise ValueError(f"invalid index record for {path}")
        mode, object_id, stage = metadata.decode("ascii").split(" ")
        if stage != "0":
            raise ValueError(f"index contains an unmerged entry for {path}")
        return mode, object_id

    def _require_isolated_objects(self) -> None:
        if self._object_directory is None:
            raise ValueError("operation requires an isolated object directory")
