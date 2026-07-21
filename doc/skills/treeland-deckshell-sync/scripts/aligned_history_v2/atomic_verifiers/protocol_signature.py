"""Normalize Wayland XML into scanner-relevant generated signatures."""

from __future__ import annotations

import json
from xml.etree import ElementTree


class ProtocolSignatureError(ValueError):
    """Raised when protocol XML cannot be normalized."""


_GENERATED_ATTRIBUTES = {
    "protocol": ("name",),
    "interface": ("name", "version"),
    "request": ("name", "type", "since", "deprecated-since"),
    "event": ("name", "type", "since", "deprecated-since"),
    "enum": ("name", "bitfield", "since"),
    "arg": ("name", "type", "interface", "allow-null", "enum"),
    "entry": ("name", "value", "since", "deprecated-since"),
}


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def generated_signatures(xml: str | bytes) -> tuple[str, ...]:
    """Return ordered canonical records for XML fields that affect generated code."""

    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError as error:
        raise ProtocolSignatureError(f"invalid protocol XML: {error}") from error

    signatures: list[str] = []

    def visit(element: ElementTree.Element, scope: tuple[str, ...]) -> None:
        kind = _local_name(element.tag)
        attributes = _GENERATED_ATTRIBUTES.get(kind)
        next_scope = scope
        if attributes is not None:
            record = {
                "attributes": {
                    name: element.attrib[name]
                    for name in attributes
                    if name in element.attrib
                },
                "kind": kind,
                "scope": list(scope),
            }
            signatures.append(
                json.dumps(record, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
            )
            name = element.attrib.get("name")
            if name and kind in {"protocol", "interface", "request", "event", "enum"}:
                next_scope = (*scope, f"{kind}:{name}")
        for child in element:
            visit(child, next_scope)

    visit(root, ())
    return tuple(signatures)
