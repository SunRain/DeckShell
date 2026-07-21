"""Strict raw Git commit object primitives for deterministic rewrites."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


SHA1_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
ALLOWED_COMMIT_HEADERS = (b"tree", b"parent", b"author", b"committer")


@dataclass(frozen=True)
class RawCommit:
    """A validated single-parent commit with raw identity headers."""

    tree: str
    parent: str
    author_header: bytes
    committer_header: bytes
    message: bytes
    payload: bytes


@dataclass(frozen=True)
class RenderedObject:
    """An object payload and the deterministic SHA-1 Git assigns to it."""

    kind: str
    payload: bytes
    object_id: str


def parse_raw_commit(payload: bytes) -> RawCommit:
    """Parse a strict, unsigned, UTF-8, single-parent commit payload."""

    if b"\r" in payload:
        raise ValueError("commit contains CR line endings")
    header_block, separator, message = payload.partition(b"\n\n")
    if not separator or not header_block:
        raise ValueError("commit has no header/message separator")
    _validate_message(message)
    headers = tuple(header_block.split(b"\n"))
    keys = tuple(header.partition(b" ")[0] for header in headers)
    if keys != ALLOWED_COMMIT_HEADERS:
        raise ValueError(f"unsupported commit headers: {keys!r}")
    values = [header.partition(b" ")[2] for header in headers]
    if any(not value for value in values):
        raise ValueError("commit contains an empty header value")
    tree = values[0].decode("ascii")
    parent = values[1].decode("ascii")
    _require_sha(tree, "tree")
    _require_sha(parent, "parent")
    return RawCommit(
        tree=tree,
        parent=parent,
        author_header=headers[2],
        committer_header=headers[3],
        message=message,
        payload=payload,
    )


def render_raw_commit(
    source: RawCommit, *, tree: str, parent: str, message: bytes
) -> RenderedObject:
    """Replace only tree, parent, and message in a validated raw commit."""

    _require_sha(tree, "tree")
    _require_sha(parent, "parent")
    _validate_message(message)
    payload = b"\n".join(
        (
            f"tree {tree}".encode("ascii"),
            f"parent {parent}".encode("ascii"),
            source.author_header,
            source.committer_header,
        )
    )
    payload += b"\n\n" + message
    return RenderedObject("commit", payload, git_object_id("commit", payload))


def git_object_id(kind: str, payload: bytes) -> str:
    """Calculate the SHA-1 object ID for an uncompressed Git payload."""

    if not kind or "\0" in kind:
        raise ValueError("invalid Git object kind")
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def _validate_message(message: bytes) -> None:
    if not message.endswith(b"\n") or message.endswith(b"\n\n"):
        raise ValueError("commit message must end with exactly one LF")
    try:
        message.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("commit message is not UTF-8") from error


def _require_sha(value: str, label: str) -> None:
    if SHA1_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a full lowercase SHA-1")
