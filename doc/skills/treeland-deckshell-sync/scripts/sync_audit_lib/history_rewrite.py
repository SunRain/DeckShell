"""Deterministically render raw commit objects for metadata-only migrations."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_HEADERS = (b"tree", b"parent", b"author", b"committer")
SYNC_PREFIX = b"[treeland-sync] "
ZERO_OBJECT_ID = "0" * 40


@dataclass(frozen=True)
class ParsedCommit:
    """Raw commit headers and message after strict validation."""

    headers: tuple[bytes, ...]
    tree: str
    parent: str
    author: bytes
    committer: bytes
    message: bytes


@dataclass(frozen=True)
class RenderedCommit:
    """One legacy commit and its deterministic metadata-only replacement."""

    ordinal: int
    source: str
    legacy_target: str
    rewritten_target: str
    legacy_parent: str
    rewritten_parent: str
    tree: str
    content: bytes
    payload_sha256: str
    old_message_sha256: str
    new_message_sha256: str


def _run_git_bytes(repo: Path, *args: str, input_data: bytes | None = None) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def read_raw_commit(repo: Path, commit: str) -> bytes:
    """Read unformatted commit content without mutating the object database."""

    return _run_git_bytes(repo, "cat-file", "commit", commit)


def parse_raw_commit(raw: bytes) -> ParsedCommit:
    """Reject unsupported commit encoding or header shapes before rendering."""

    if b"\r" in raw:
        raise ValueError("commit contains CR line endings")
    header_bytes, separator, message = raw.partition(b"\n\n")
    if not separator or not header_bytes:
        raise ValueError("commit has no header/message separator")
    if not message.endswith(b"\n") or message.endswith(b"\n\n"):
        raise ValueError("commit message must have exactly one trailing LF")
    try:
        message.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("commit message is not UTF-8") from error

    headers = tuple(header_bytes.split(b"\n"))
    keys = tuple(line.partition(b" ")[0] for line in headers)
    if keys != ALLOWED_HEADERS:
        raise ValueError(f"unsupported commit headers: {keys!r}")
    values = {key: line.partition(b" ")[2] for key, line in zip(keys, headers)}
    for key, value in values.items():
        if not value:
            raise ValueError(f"empty commit header: {key.decode('ascii')}")
    return ParsedCommit(
        headers=headers,
        tree=values[b"tree"].decode("ascii"),
        parent=values[b"parent"].decode("ascii"),
        author=values[b"author"],
        committer=values[b"committer"],
        message=message,
    )


def _line_positions(lines: list[bytes], needle: bytes) -> list[int]:
    return [index for index, line in enumerate(lines) if line.rstrip(b"\n") == needle]


def _single_position(lines: list[bytes], needle: bytes, label: str) -> int:
    positions = _line_positions(lines, needle)
    if len(positions) != 1:
        raise ValueError(f"expected exactly one {label}, found {len(positions)}")
    return positions[0]


def _field_values(lines: list[bytes], start: int, end: int, field: str) -> list[str]:
    values = []
    for line in lines[start + 1 : end]:
        stripped = line.rstrip(b"\n")
        if not stripped:
            continue
        if not stripped.startswith(b"- "):
            raise ValueError(f"malformed {field} entry: {stripped!r}")
        values.append(stripped[2:].decode("utf-8"))
    if not values:
        raise ValueError(f"empty {field} field")
    return values


def _manifest_notes(entry: dict[str, Any]) -> list[str]:
    notes = entry.get("adaptation_notes")
    if not isinstance(notes, str) or not notes.strip():
        raise ValueError("manifest has invalid adaptation_notes")
    return [line.strip() for line in notes.splitlines() if line.strip()]


def _manifest_paths(entry: dict[str, Any]) -> list[str]:
    paths = entry.get("adaptation_paths")
    if not isinstance(paths, list):
        raise ValueError("manifest adaptation_paths must be a list")
    rendered = [f"{item.get('kind')}: {item.get('path')}" for item in paths]
    if entry.get("action") == "adapted" and not rendered:
        raise ValueError("adapted manifest entry has no adaptation paths")
    if entry.get("action") != "adapted" and rendered:
        raise ValueError("non-adapted manifest entry has adaptation paths")
    return rendered or ["none"]


def render_message(old_message: bytes, entry: dict[str, Any]) -> bytes:
    """Replace one complete legacy sync block with canonical v2 fields."""

    if b"\r" in old_message:
        raise ValueError("commit message contains CR line endings")
    try:
        old_message.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("commit message is not UTF-8") from error
    if not old_message.endswith(b"\n") or old_message.endswith(b"\n\n"):
        raise ValueError("commit message must have exactly one trailing LF")

    lines = old_message.splitlines(keepends=True)
    classification = _single_position(
        lines, b"[treeland-sync] classification: " + str(entry["classification"]).encode(), "classification"
    )
    action = _single_position(
        lines, b"[treeland-sync] action: " + str(entry["action"]).encode(), "action"
    )
    drop_files = _single_position(lines, b"[treeland-sync] drop files:", "drop files")
    path_mapping = _single_position(lines, b"[treeland-sync] path mapping:", "path mapping")
    paths_header = _line_positions(lines, b"[treeland-sync] adaptation paths:")
    if paths_header:
        raise ValueError("legacy message already has adaptation paths")
    notes = _single_position(lines, b"[treeland-sync] adaptation notes:", "adaptation notes")
    trailer = _single_position(
        lines,
        b"Treeland-Commit: " + str(entry["source_commit"]).encode(),
        "Treeland-Commit trailer",
    )
    if not classification < action < drop_files < path_mapping < notes < trailer:
        raise ValueError("sync block fields are not in canonical legacy order")
    sync_lines = [line for line in lines[classification:trailer] if line.startswith(SYNC_PREFIX)]
    if len(sync_lines) != 5:
        raise ValueError("sync block contains an unknown or duplicate field")
    _field_values(lines, drop_files, path_mapping, "drop files")
    _field_values(lines, path_mapping, notes, "path mapping")
    old_notes = _field_values(lines, notes, trailer, "adaptation notes")
    manifest_notes = _manifest_notes(entry)
    if entry.get("action") == "adapted":
        old_text = " ".join(" ".join(old_notes).split())
        manifest_text = " ".join(" ".join(manifest_notes).split())
        if old_text != manifest_text:
            raise ValueError("legacy adaptation notes differ from manifest")
    elif manifest_notes != ["none"]:
        raise ValueError("non-adapted manifest notes must be none")

    paths_lines = [b"[treeland-sync] adaptation paths:\n"]
    paths_lines.extend(f"- {value}\n".encode("utf-8") for value in _manifest_paths(entry))
    notes_lines = [b"[treeland-sync] adaptation notes:\n"]
    notes_lines.extend(f"- {value}\n".encode("utf-8") for value in manifest_notes)
    result = b"".join(lines[:notes] + paths_lines + notes_lines + [b"\n"] + lines[trailer:])
    if not result.endswith(b"\n") or result.endswith(b"\n\n"):
        raise ValueError("rendered message does not have exactly one trailing LF")
    return result


def _object_id(content: bytes) -> str:
    prefix = f"commit {len(content)}\0".encode("ascii")
    return hashlib.sha1(prefix + content).hexdigest()


def render_commit(raw: bytes, entry: dict[str, Any], rewritten_parent: str) -> tuple[ParsedCommit, bytes, str]:
    """Render one commit while retaining its tree and author/committer bytes."""

    parsed = parse_raw_commit(raw)
    if len(rewritten_parent) != 40:
        raise ValueError("rewritten parent must be a 40-character object ID")
    headers = (
        parsed.headers[0],
        f"parent {rewritten_parent}".encode("ascii"),
        parsed.headers[2],
        parsed.headers[3],
    )
    message = render_message(parsed.message, entry)
    content = b"\n".join(headers) + b"\n\n" + message
    return parsed, content, _object_id(content)


def tool_bundle_sha256(tool_root: Path) -> str:
    """Hash the Python tool bundle and skill contract used to render the chain."""

    files = sorted(
        path
        for path in tool_root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    if not files:
        raise ValueError("tool bundle contains no regular files")
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(tool_root).as_posix().encode("utf-8")
        digest.update(relative + b"\0" + path.read_bytes())
    return digest.hexdigest()


def render_chain(repo: Path, manifest: dict[str, Any], tool_root: Path) -> tuple[list[RenderedCommit], str]:
    """Render the complete ordered migration chain without writing objects."""

    records = []
    seen_sources = set()
    previous_legacy = ""
    previous_rewritten = ""
    for ordinal, entry in enumerate(manifest.get("entries", []), 1):
        if entry.get("ordinal") != ordinal:
            raise ValueError(f"manifest ordinal mismatch at position {ordinal}")
        source = str(entry.get("source_commit", ""))
        legacy_target = str(entry.get("legacy_target_commit", ""))
        if source in seen_sources or len(source) != 40 or len(legacy_target) != 40:
            raise ValueError(f"invalid or duplicate mapping at ordinal {ordinal}")
        seen_sources.add(source)
        raw = read_raw_commit(repo, legacy_target)
        parsed = parse_raw_commit(raw)
        if previous_legacy:
            if parsed.parent != previous_legacy:
                raise ValueError(f"legacy parent chain breaks at {legacy_target}")
        rewritten_parent = previous_rewritten or parsed.parent
        try:
            parsed, content, rewritten_target = render_commit(raw, entry, rewritten_parent)
        except ValueError as error:
            raise ValueError(
                f"render failed at ordinal {ordinal} ({source} -> {legacy_target}): {error}"
            ) from error
        record = RenderedCommit(
            ordinal=ordinal,
            source=source,
            legacy_target=legacy_target,
            rewritten_target=rewritten_target,
            legacy_parent=parsed.parent,
            rewritten_parent=rewritten_parent,
            tree=parsed.tree,
            content=content,
            payload_sha256=hashlib.sha256(content).hexdigest(),
            old_message_sha256=hashlib.sha256(parsed.message).hexdigest(),
            new_message_sha256=hashlib.sha256(content.partition(b"\n\n")[2]).hexdigest(),
        )
        records.append(record)
        previous_legacy, previous_rewritten = legacy_target, rewritten_target
    if not records:
        raise ValueError("manifest has no entries")
    return records, tool_bundle_sha256(tool_root)


def mapping_payload(
    records: list[RenderedCommit], tool_bundle: str, manifest_sha256: str
) -> dict[str, Any]:
    """Return canonical JSON data for dry-run comparison and later object audit."""

    mappings = [
        {
            "ordinal": record.ordinal,
            "source_commit": record.source,
            "legacy_target_commit": record.legacy_target,
            "rewritten_target_commit": record.rewritten_target,
            "legacy_parent": record.legacy_parent,
            "rewritten_parent": record.rewritten_parent,
            "tree": record.tree,
            "payload_sha256": record.payload_sha256,
            "old_message_sha256": record.old_message_sha256,
            "new_message_sha256": record.new_message_sha256,
        }
        for record in records
    ]
    digest_source = json.dumps(mappings, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "schema_version": 1,
        "tool_bundle_sha256": tool_bundle,
        "manifest_sha256": manifest_sha256,
        "count": len(mappings),
        "plan_digest_sha256": hashlib.sha256(digest_source.encode("utf-8")).hexdigest(),
        "mappings": mappings,
    }


def write_commit_objects(repo: Path, records: list[RenderedCommit], rewrite_ref: str) -> None:
    """Write verified objects only to an isolated mirror and create a new ref once."""

    if not rewrite_ref.startswith("refs/migrations/"):
        raise ValueError("rewrite ref must be under refs/migrations/")
    for record in records:
        written = _run_git_bytes(repo, "hash-object", "-t", "commit", "-w", "--stdin", input_data=record.content)
        if written.decode("ascii").strip() != record.rewritten_target:
            raise ValueError(f"object hash mismatch for {record.legacy_target}")
    _run_git_bytes(repo, "update-ref", rewrite_ref, records[-1].rewritten_target, ZERO_OBJECT_ID)
