"""Exact message edits for an explicitly authorized relative-Refs rewrite."""

import re

from .refs import relative_reference

DEPENDENCY_LINE = re.compile(
    r"^(?:- Includes (?:waylib-shared|wlroots submodule) update to |"
    r"- commit: |\[treeland-unified-sync\] nested gitlink: ).*$"
)
SHA = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")


def mapped_message(message: bytes, old_ref: str, new_ref: str, lower: dict) -> bytes:
    """Change only the unique Refs and generated lower-repository references."""
    relative_reference(new_ref)
    lines = message.decode("utf-8").splitlines(keepends=True)
    refs = [line for line in lines if line.startswith("Refs:")]
    if len(refs) != 1 or refs[0].rstrip("\n") != "Refs: " + old_ref:
        raise ValueError("history rewrite requires the exact unique original Refs")
    result = []
    for line in lines:
        if line == refs[0]:
            line = "Refs: " + new_ref + ("\n" if line.endswith("\n") else "")
        elif DEPENDENCY_LINE.fullmatch(line.rstrip("\n")):
            line = SHA.sub(lambda match: lower.get(match[0], match[0]), line)
        result.append(line)
    return "".join(result).encode("utf-8")
