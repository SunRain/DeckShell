"""用保留项目 include、条件和宏作用域的预处理投影核验公共命名空间。"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Mapping, Sequence


HEADERS = {".h", ".hh", ".hpp", ".hxx"}
LEXICAL = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*.*?\*/|//[^\n]*', re.S)
DEFINE = re.compile(r"^[ \t]*#[ \t]*define[ \t]+([A-Za-z_]\w*)(\([^\n)]*\))?[ \t]*(.*)$")
DIRECTIVE = re.compile(r"^[ \t]*#[ \t]*(\w+)[ \t]*(.*)$")
IDENTIFIER = re.compile(r"[A-Za-z_]\w*")
INCLUDE = re.compile(r'^[<"]([^>"]+)[>"]$')
LINE_MARKER = re.compile(r'^#\s+\d+\s+("(?:\\.|[^"\\])*")')


def _without_comments(content: str) -> str:
    return LEXICAL.sub(
        lambda match: "\n" * match[0].count("\n") if match[0].startswith(("//", "/*")) else match[0],
        content.replace("\\\n", ""),
    )


def _include_path(path: str, argument: str, contents: Mapping[str, str], include_roots=()):
    match = INCLUDE.fullmatch(argument.strip())
    if match is None:
        return None
    name = match[1]
    relative = (PurePosixPath(path).parent / name).as_posix()
    if relative in contents:
        return relative
    public_matches = sorted({(PurePosixPath(root) / name).as_posix() for root in include_roots}
                            .intersection(contents))
    if len(public_matches) == 1:
        return public_matches[0]
    if len(public_matches) > 1:
        raise ValueError(f"ambiguous project namespace include: {path}: {name}")
    matches = [key for key in contents if key == name or key.endswith("/" + name)]
    if len(matches) > 1:
        raise ValueError(f"ambiguous project namespace include: {path}: {name}")
    return matches[0] if matches else None


def _header_lines(path: str, content: str, contents: Mapping[str, str], include_roots=()):
    rows, stack, groups = [], [], {}
    for index, line in enumerate(content.splitlines()):
        match = DIRECTIVE.match(line)
        kind, argument = match.groups() if match else (None, "")
        if kind in {"if", "ifdef", "ifndef"}:
            stack.append(index)
            groups[index] = {"lines": [], "tokens": set()}
        if kind in {"if", "ifdef", "ifndef", "elif", "else", "endif"} and stack:
            groups[stack[-1]]["lines"].append(index)
            groups[stack[-1]]["tokens"].update(IDENTIFIER.findall(argument))
        include = _include_path(path, argument, contents, include_roots) if kind == "include" else None
        rows.append({"line": line, "kind": kind, "argument": argument,
                     "guards": tuple(stack), "include": include})
        if kind == "endif" and stack:
            stack.pop()
    if stack:
        raise ValueError(f"unterminated namespace preprocessor conditional: {path}")
    return rows, groups


def _relevant_macros(headers):
    definitions, relevant = {}, {"namespace"}
    for rows, _ in headers.values():
        for row in rows:
            match = DEFINE.match(row["line"])
            if match:
                name, _, body = match.groups()
                definitions.setdefault(name, set()).update(IDENTIFIER.findall(body))
                if "NAMESPACE" in name or re.search(r"\bnamespace\b", body):
                    relevant.add(name)
            elif row["kind"] is None:
                relevant.update(re.findall(r"\bnamespace\s+([A-Za-z_]\w*)", row["line"]))
    while True:
        before = set(relevant)
        for name in list(relevant):
            relevant.update(definitions.get(name, set()))
        for rows, groups in headers.values():
            guards = _required_guards(rows, relevant)
            relevant.update(token for guard in guards for token in groups[guard]["tokens"])
        if relevant == before:
            return relevant & definitions.keys()


def _required_guards(rows, relevant):
    selected = set()
    for row in rows:
        if row["kind"] in {"define", "undef"}:
            tokens = IDENTIFIER.findall(row["argument"])
            needed = bool(tokens and tokens[0] in relevant)
        elif row["kind"] is None:
            needed = bool(set(IDENTIFIER.findall(row["line"])) & (relevant | {"namespace"}))
        else:
            needed = row["include"] is not None
        if needed:
            selected.update(row["guards"])
    return selected


def _project_header(path, rows, groups, relevant, filenames):
    guards = _required_guards(rows, relevant)
    conditional_lines = {index for guard in guards for index in groups[guard]["lines"]}
    projected = [f"#line 1 {json.dumps(path)}"]
    for index, row in enumerate(rows):
        kind = row["kind"]
        if row["include"] is not None:
            projected.append(f'#include "{filenames[row["include"]]}"')
        elif kind in {"define", "undef"}:
            tokens = IDENTIFIER.findall(row["argument"])
            if tokens and tokens[0] in relevant:
                if "_Pragma" in tokens:
                    raise ValueError(f"unsupported namespace macro pragma: {path}")
                projected.append(row["line"])
        elif kind is None or index in conditional_lines or (kind == "pragma" and row["argument"] == "once"):
            projected.append(row["line"])
        elif kind in {"error", "warning"} and row["guards"] and row["guards"][-1] in guards:
            projected.append(row["line"])
    return "\n".join(projected) + "\n"


def _preprocess(contents, headers, relevant):
    with tempfile.TemporaryDirectory(prefix="unified-namespace-") as directory:
        root = Path(directory)
        filenames = {path: f"header-{index}.h" for index, path in enumerate(contents)}
        for path, (rows, groups) in headers.items():
            (root / filenames[path]).write_text(
                _project_header(path, rows, groups, relevant, filenames), encoding="utf-8",
            )
        source = "\n".join(f'#include "{name}"' for name in filenames.values()) + "\n"
        result = subprocess.run(
            ["c++", "-E", "-x", "c++", "-I", str(root), "-"], input=source,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
    errors = []
    if result.returncode or "redefined" in result.stderr:
        errors.append("public namespace preprocessing failed: " + result.stderr.strip())
    return result.stdout, errors


def _tokens_with_headers(output: str, paths):
    tokens, path = [], None
    for line in output.splitlines():
        marker = LINE_MARKER.match(line)
        if marker:
            value = json.loads(marker[1])
            path = value if value in paths else None
        elif path is not None:
            code = LEXICAL.sub('""', line)
            tokens.extend((path, token) for token in re.findall(r"[A-Za-z_]\w*|::|[{}=;]", code))
    return tokens


def _namespace_at(tokens, index, stack):
    end = index + 1
    parts = []
    while end < len(tokens) and tokens[end][1] not in {"{", "}", ";", "="}:
        parts.append(tokens[end][1])
        end += 1
    if not parts or end == len(tokens) or tokens[end][1] not in {"{", "="}:
        return None, index
    prefix = next((value for value in reversed(stack) if value), "")
    name = (prefix + "::" if prefix else "") + "".join(parts)
    if tokens[end][1] == "{":
        stack.append(name)
        return name, end
    target = end + 1
    while target < len(tokens) and tokens[target][1] != ";":
        target += 1
    return name + "=" + "".join(token for _, token in tokens[end + 1:target]), target


def _namespace_headers(output, paths):
    tokens = _tokens_with_headers(output, paths)
    headers, stack, index = {}, [], 0
    while index < len(tokens):
        path, token = tokens[index]
        if token == "namespace" and (index == 0 or tokens[index - 1][1] != "using"):
            name, index = _namespace_at(tokens, index, stack)
            if name:
                headers.setdefault(path, set()).add(name)
        elif token == "{":
            stack.append(None)
        elif token == "}" and stack:
            stack.pop()
        index += 1
    return {path: sorted(values) for path, values in sorted(headers.items())}


def namespace_contract(contents: Mapping[str, str], include_roots: Sequence[str] = ()) -> Dict[str, Any]:
    """展开项目命名空间宏；保留条件/undef，外部依赖由最终安装编译探针验证。"""

    cleaned = {path: _without_comments(text) for path, text in sorted(contents.items())}
    definitions, namespaces, errors = [], {}, []
    try:
        headers = {path: _header_lines(path, text, cleaned, include_roots) for path, text in cleaned.items()}
        relevant = _relevant_macros(headers)
        definitions = [f'{path}:{row["line"].strip()}' for path, (rows, _) in headers.items()
                       for row in rows if row["kind"] == "define"
                       and IDENTIFIER.findall(row["argument"])[0] in relevant]
        if relevant or any(re.search(r"\bnamespace\b", text) for text in cleaned.values()):
            output, errors = _preprocess(cleaned, headers, relevant)
            namespaces = _namespace_headers(output, cleaned)
    except (OSError, ValueError) as error:
        errors.append(str(error))
    return {"namespaces": sorted({value for values in namespaces.values() for value in values}),
            "headers": namespaces, "macro_definitions": definitions, "errors": sorted(set(errors))}
