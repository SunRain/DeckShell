from __future__ import annotations

import hashlib
import re
import unittest

from test_adaptation_docs import _Fixture


class AdaptationContentDeltaCliTests(unittest.TestCase):
    def test_generate_appends_canonical_post_image_diff(self) -> None:
        with _Fixture() as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", content
            )
            self.assertIn("不等同于本次提交的纯 adaptation delta", content)
            self.assertIn("Comparison result: `content-different`", content)
            self.assertIn("Treeland source path: `src/feature.txt`", content)
            self.assertIn("DeckShell target path: `compositor/feature.txt`", content)
            self.assertIn(
                "diff --git a/upstream/src/feature.txt "
                "b/deckshell/compositor/feature.txt",
                content,
            )
            self.assertIn("-source upstream", content)
            self.assertIn("+target adapted", content)
            self.assertRegex(content, r"Content diff SHA-256: `[0-9a-f]{64}`")

    def test_generate_hashes_the_exact_embedded_content_diff(self) -> None:
        with _Fixture() as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            digest = re.search(r"Content diff SHA-256: `([0-9a-f]{64})`", delta)
            embedded = re.search(r"```diff\n(.*?)\n```", delta, re.DOTALL)
            self.assertIsNotNone(digest)
            self.assertIsNotNone(embedded)
            expected = hashlib.sha256(
                f"{embedded.group(1)}\n".encode("utf-8")
            ).hexdigest()
            self.assertEqual(digest.group(1), expected)

    def test_generate_records_identical_post_images_without_a_fake_diff(self) -> None:
        with _Fixture(target_content="source upstream\n") as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.split(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `identical`", delta)
            self.assertIn("Content diff: `none`", delta)
            self.assertNotIn("```diff", delta)

    def test_generate_uses_dev_null_for_upstream_only_post_image(self) -> None:
        with _Fixture(kind="omitted") as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `upstream-only`", delta)
            self.assertIn(
                "diff --git a/upstream/src/feature.txt "
                "b/deckshell/compositor/src/feature.txt",
                delta,
            )
            self.assertIn("--- a/upstream/src/feature.txt", delta)
            self.assertIn("+++ /dev/null", delta)
            self.assertIn("-source upstream", delta)

    def test_generate_distinguishes_empty_blob_from_absent_path(self) -> None:
        with _Fixture(kind="omitted", source_content="") as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Treeland post-image: state `present`", delta)
            self.assertIn("size `0` bytes", delta)
            self.assertIn("Comparison result: `upstream-only`", delta)
            self.assertIn("deleted file mode 100644", delta)

    def test_generate_records_both_absent_after_upstream_delete(self) -> None:
        with _Fixture(kind="omitted", source_content=None) as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Treeland post-image: state `absent`", delta)
            self.assertIn("DeckShell post-image: state `absent`", delta)
            self.assertIn("Comparison result: `both-absent`", delta)
            self.assertIn("Content diff: `none`", delta)
            self.assertNotIn("```diff", delta)

    def test_generate_keeps_target_delete_diff_when_both_post_images_are_absent(self) -> None:
        with _Fixture(
            source_content=None,
            target_content=None,
        ) as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("deleted file mode 100644", content)
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `both-absent`", delta)
            self.assertIn("Content diff: `none`", delta)

    def test_generate_uses_dev_null_for_deckshell_only_post_image(self) -> None:
        with _Fixture(source_content=None) as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `deckshell-only`", delta)
            self.assertIn("--- /dev/null", delta)
            self.assertIn("+++ b/deckshell/compositor/feature.txt", delta)
            self.assertIn("+target adapted", delta)

    def test_generate_records_mode_only_difference(self) -> None:
        with _Fixture(
            source_content="shared content\n",
            target_content="shared content\n",
            target_executable=True,
        ) as fixture:
            fixture._git("config", "core.filemode", "false")
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `mode-only`", delta)
            self.assertIn("old mode 100644", delta)
            self.assertIn("new mode 100755", delta)

    def test_generate_embeds_binary_patch_for_binary_post_images(self) -> None:
        with _Fixture(
            source_content=b"\x00source payload\n",
            target_content=b"\x00target payload\n",
        ) as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `content-different`", delta)
            self.assertIn("GIT binary patch", delta)
            self.assertNotIn("\x00", delta)

    def test_generate_fails_closed_for_non_utf8_text_diff(self) -> None:
        with _Fixture(
            source_content=b"\xffsource payload\n",
            target_content="target adapted\n",
        ) as fixture:
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("post-image diff is not UTF-8", result.stderr)

    def test_generate_compares_symlink_blob_targets(self) -> None:
        with _Fixture(
            source_link_target="source-target",
            target_link_target="target-target",
        ) as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("mode `120000`", delta)
            self.assertIn("Comparison result: `content-different`", delta)
            self.assertIn("-source-target", delta)
            self.assertIn("+target-target", delta)

    def test_generate_fails_closed_for_gitlink_post_image(self) -> None:
        with _Fixture(target_gitlink=True) as fixture:
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported post-image object type", result.stderr)
            self.assertIn("commit", result.stderr)

    def test_generate_prefers_rename_new_side_for_source_post_image(self) -> None:
        with _Fixture() as fixture:
            fixture.update_source_changes(
                [
                    {
                        "status": "R100",
                        "old": {
                            "source": "src/old-feature.txt",
                            "target": fixture.adaptation_path,
                        },
                        "new": {
                            "source": "src/feature.txt",
                            "target": fixture.adaptation_path,
                        },
                    }
                ]
            )
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Treeland source path: `src/feature.txt`", content)
            self.assertNotIn("Treeland source path: `src/old-feature.txt`", content)

    def test_generate_rejects_multiple_source_post_images(self) -> None:
        with _Fixture() as fixture:
            fixture.update_source_changes(
                [
                    {
                        "status": "M",
                        "old": None,
                        "new": {
                            "source": "src/feature.txt",
                            "target": fixture.adaptation_path,
                        },
                    },
                    {
                        "status": "M",
                        "old": None,
                        "new": {
                            "source": "src/other-feature.txt",
                            "target": fixture.adaptation_path,
                        },
                    },
                ]
            )
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("multiple source post-images", result.stderr)

    def test_generate_compares_retained_target_for_omitted_path(self) -> None:
        with _Fixture(
            kind="omitted",
            omitted_baseline_content="DeckShell retained content\n",
        ) as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `content-different`", delta)
            self.assertIn("-source upstream", delta)
            self.assertIn("+DeckShell retained content", delta)

    def test_generate_records_identical_materialized_post_image(self) -> None:
        with _Fixture(
            kind="materialized",
            target_content="source upstream\n",
        ) as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("new file mode 100644", content)
            delta = content.rsplit(
                "#### 提交后文件状态差异（Treeland 与 DeckShell）", 1
            )[1].split("## 输入证据", 1)[0]
            self.assertIn("Comparison result: `identical`", delta)
            self.assertIn("Content diff: `none`", delta)


if __name__ == "__main__":
    unittest.main()
