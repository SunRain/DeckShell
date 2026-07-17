from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sync_audit_lib.patch_delta import compare_patch_sections, parse_patch_sections


class PatchDeltaTests(unittest.TestCase):
    def test_equivalent_change_ignores_path_prefix_and_hunk_position(self) -> None:
        source = """diff --git a/src/item.cpp b/src/item.cpp
--- a/src/item.cpp
+++ b/src/item.cpp
@@ -10,1 +10,1 @@
-old
+new
"""
        target = """diff --git a/compositor/src/item.cpp b/compositor/src/item.cpp
--- a/compositor/src/item.cpp
+++ b/compositor/src/item.cpp
@@ -40,1 +40,1 @@
-old
+new
"""

        result = compare_patch_sections(
            parse_patch_sections(source),
            parse_patch_sections(target),
            {"src/item.cpp": "compositor/src/item.cpp"},
        )

        self.assertTrue(result["compositor/src/item.cpp"]["delta_equivalent"])

    def test_changed_added_lines_are_not_equivalent(self) -> None:
        source = """diff --git a/src/item.cpp b/src/item.cpp
--- a/src/item.cpp
+++ b/src/item.cpp
@@ -1 +1 @@
-old
+upstream
"""
        target = """diff --git a/compositor/src/item.cpp b/compositor/src/item.cpp
--- a/compositor/src/item.cpp
+++ b/compositor/src/item.cpp
@@ -1 +1 @@
-old
+adapted
"""

        result = compare_patch_sections(
            parse_patch_sections(source),
            parse_patch_sections(target),
            {"src/item.cpp": "compositor/src/item.cpp"},
        )

        self.assertFalse(result["compositor/src/item.cpp"]["delta_equivalent"])

    def test_materialized_target_is_not_equal_to_source_modification(self) -> None:
        source = """diff --git a/CMakePresets.json b/CMakePresets.json
--- a/CMakePresets.json
+++ b/CMakePresets.json
@@ -1 +1 @@
-old
+new
"""
        target = """diff --git a/compositor/CMakePresets.json b/compositor/CMakePresets.json
new file mode 100644
--- /dev/null
+++ b/compositor/CMakePresets.json
@@ -0,0 +1 @@
+new
"""

        result = compare_patch_sections(
            parse_patch_sections(source),
            parse_patch_sections(target),
            {"CMakePresets.json": "compositor/CMakePresets.json"},
        )

        self.assertFalse(result["compositor/CMakePresets.json"]["delta_equivalent"])


if __name__ == "__main__":
    unittest.main()
