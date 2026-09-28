"""读取已发生的报告/收口和限定例外；不重新授予产品验收。"""

from __future__ import annotations

import json

from .artifacts import read_verified_artifact
from .ctest_results import discovery_errors, parse_ctest
from .git_ops import canonical_json_sha256, read_json
from .record_context import relative_name, require


def accepted_report(root, requested=None):
    """有收口时只选择其绑定报告，不能按文件名或时间猜接受版本。"""
    journal = root / "closeout-journal.json"
    require(not journal.is_symlink(), "接受收口不能为符号链接")
    if not journal.exists():
        name = relative_name(requested or "sync-report.json")
        return read_json(root / name), name, None
    closeout = read_json(journal)
    require(closeout.get("kind") == "treeland-unified-closeout-journal"
            and closeout.get("outcome") == "pass", "节点尚未完整收口")
    digest = closeout["identity"]["report_sha256"]
    candidates = []
    for path in sorted(root.glob("sync-report*.json")):
        require(not path.is_symlink(), "接受报告不能为符号链接")
        report = read_json(path)
        if canonical_json_sha256(report) == digest:
            candidates.append((report, path.name))
    if requested:
        candidates = [pair for pair in candidates if pair[1] == relative_name(requested)]
    require(len(candidates) == 1, "收口绑定的接受报告缺失或不唯一")
    report, name = candidates[0]
    require(report.get("outcome") == "pass", "收口未绑定通过报告")
    return report, name, closeout


def check_closeout(closeout, manifest):
    """复核原节点收口的两端身份；不依赖今天的浮动分支 tip。"""
    if closeout is None:
        return
    identity = closeout["identity"]
    original = manifest["identity"]
    for lane in ("parent", "child", "wlroots"):
        head = manifest.get(f"final_{lane}_head")
        if head is None:
            continue
        base = original[f"{lane}_base"] if lane != "wlroots" else original["wlroots"]["base"]
        require(identity.get(f"{lane}_new") == head
                and identity.get(f"{lane}_expected_old") == base
                and closeout.get(f"{lane}_updated") is True, f"{lane} 收口与原候选不符")


def original_report(root, name, accepted):
    """授权后报告之外保留原阻断事实，不将补充报告冒充再次收口。"""
    if name == "sync-report.json":
        return None
    before = read_json(root / "sync-report.json")
    for key in ("replay_identity", "inventory_sha256", "manifest_sha256", "validations_sha256"):
        require(before.get(key) == accepted.get(key), "原报告与接受报告不是同一候选")
    return {"path": "sync-report.json", "outcome": before["outcome"]}


def _exception_entry(root, auth, manifest, validation):
    scope = auth["scope"]
    entries = [e for e in validation["entries"] if e["id"] == scope["validation_id"]]
    require(len(entries) == 1, "限定例外未唯一定位验证项")
    entry = entries[0]
    require(entry.get("attempt") == scope["validation_attempt"]
            and entry.get("manifest_sha256") == canonical_json_sha256(manifest), "例外验证身份错误")
    _, raw = read_verified_artifact(entry["log"], root, "exception CTest log")
    actual = parse_ctest(raw, entry["exit_code"])
    require(all(actual[k] == entry[k] for k in ("outcome", "tests", "test_results"))
            and not actual.get("parse_error"), "例外原始日志与验证记录不符")
    require(entry["outcome"] == "fail" and entry["exit_code"] == 0
            and entry["tests"]["failed"] == 0, "例外不能覆盖真实失败")
    skipped = [t["name"] for t in entry["test_results"] if t["status"] == "skipped"]
    require(skipped and skipped == scope["allowed_skips"], "跳过集合超出原授权")
    filters = ("-R", "-E", "-L", "-LE", "-I", "--tests-regex", "--exclude-regex", "--label-regex",
               "--label-exclude", "--tests-information", "--rerun-failed", "--tests-from-file", "--exclude-from-file")
    require(not any(arg == flag or arg.startswith(flag + "=") or
                    (flag.startswith("-") and not flag.startswith("--") and arg.startswith(flag))
                    for arg in entry["command"][1:] for flag in filters), "例外不能用于过滤后的测试命令")
    require(not discovery_errors(entry, root), "例外缺少完整测试发现或含过滤")
    evidence = auth["evidence"]
    require(evidence["raw_ctest_log"] == entry["log"]["path"]
            and evidence["full_test_discovery"] == entry["test_discovery"]["log"]["path"], "例外日志定位错配")
    acceptance = auth["acceptance"]
    require(acceptance.get("status") == "authorized-non-blocking-skip"
            and acceptance.get("full_unfiltered_test_set") is True
            and acceptance.get("drm_behavior_proven") is False
            and acceptance.get("exit_code") == 0, "例外接受边界错误")
    require(all(acceptance.get("tests_" + k) == v for k, v in entry["tests"].items()), "例外计数错误")


def exception_record(context, descriptor, root, report, inventory, manifest, validation, closeout):
    """只展示被原收口绑定的授权，复核范围和日志，不修改通用 SKIP 策略。"""
    bundle = report.get("skip_exception")
    if bundle is None:
        return None
    require(closeout is not None, "限定例外须有原接受收口")
    require(set(bundle) == {"skip_authorization", "inventory", "manifest", "validations"}, "例外资料不完整")
    data = {key: json.loads(read_verified_artifact(value, root, key)[1]) for key, value in bundle.items()}
    require(data["inventory"] == inventory and data["manifest"] == manifest
            and data["validations"] == validation, "例外与节点原始输入错配")
    auth = data["skip_authorization"]
    require(auth.get("kind") == "treeland-plan-specific-ctest-skip-exception"
            and auth.get("schema_version") == 1 and auth.get("authorization", "").strip(), "例外授权缺失")
    require(auth.get("plan") == context.batch and auth.get("node") == descriptor["name"]
            and auth["scope"]["source_head"] == inventory["range"]["head"], "例外属于其它批次或节点")
    require(manifest["identity"]["refs_doc"] == context.batch + "/plan.md", "例外方案身份不符")
    _exception_entry(root, auth, manifest, validation)
    return {"authorization": auth, "path": bundle["skip_authorization"]["path"]}


def check_accepted_results(closeout, gates, validation, exception):
    """原接受凭据不能替实际 gate 和原命令结果掩盖失败。"""
    if closeout is None:
        return
    require(all(gate.get("outcome") == "pass" for gate in gates.values()), "接受报告包含未通过的 gate")
    allowed = exception["authorization"]["scope"]["validation_id"] if exception else None
    require(all(entry.get("outcome") in ("pass", "no-tests", "not-applicable") or entry["id"] == allowed
                for entry in validation["entries"]), "接受报告存在未经原授权的验证失败")
