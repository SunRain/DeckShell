from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.contracts import build_install_snapshot, compare_contract_snapshots


PC = (
    "prefix=${pcfiledir}/../..\nincludedir=${prefix}/include\nlibdir=${prefix}/lib\n"
    "api_name=WaylibFixture\napi_level=1\napi_cflags=-DAPI_LEVEL=${api_level}\n"
    "private_libs=-lPrivateOne\napi_requires=\n"
    "Name: ${api_name}\nDescription: Installed contract fixture\nVersion: 1.0\n"
    "Requires: ${api_requires}\nLibs: -L${libdir} -lWaylibFixture\n"
    "Libs.private: ${private_libs}\nCflags: -I${includedir} ${api_cflags}\n"
)


class PkgConfigContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self, label, content=PC):
        root = self.root / label
        directory = root / "lib/pkgconfig"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "WaylibFixture.pc").write_text(content, encoding="utf-8")
        return build_install_snapshot(root)

    def test_compares_recursive_cflags_variables_instead_of_field_spelling(self):
        before = self.snapshot("before")
        after = self.snapshot("after", PC.replace("api_level=1", "api_level=2"))
        self.assertNotEqual(before["pkg_config"], after["pkg_config"])
        self.assertIn("-DAPI_LEVEL=1", before["pkg_config"]["lib/pkgconfig/WaylibFixture.pc"]["Cflags"])
        self.assertIn("-DAPI_LEVEL=2", after["pkg_config"]["lib/pkgconfig/WaylibFixture.pc"]["Cflags"])

    def test_compares_private_link_and_name_variable_changes(self):
        before = self.snapshot("before")
        for name, old, new in (("private", "-lPrivateOne", "-lPrivateTwo"),
                               ("name", "api_name=WaylibFixture", "api_name=ChangedFixture")):
            with self.subTest(field=name):
                after = self.snapshot(name, PC.replace(old, new))
                self.assertNotEqual(before["pkg_config"], after["pkg_config"])

    def test_relocation_and_unreferenced_variables_do_not_change_contract(self):
        before = self.snapshot("before")
        after = self.snapshot("after", PC + "unused=changed\n")
        self.assertEqual(before["pkg_config"], after["pkg_config"])

    def test_relocation_handles_spaces_and_does_not_normalize_neighboring_prefixes(self):
        before = self.snapshot("before with spaces")
        after = self.snapshot("after with spaces")
        self.assertEqual(before["pkg_config"], after["pkg_config"])
        one = PC.replace("Cflags: -I${includedir} ${api_cflags}", f"Cflags: -I{self.root}/one-extra/include")
        two = PC.replace("Cflags: -I${includedir} ${api_cflags}", f"Cflags: -I{self.root}/two-extra/include")
        self.assertNotEqual(self.snapshot("one", one)["pkg_config"], self.snapshot("two", two)["pkg_config"])

    def test_ambient_pkg_config_overrides_cannot_replace_the_installed_package(self):
        before = self.snapshot("before")
        poison = self.root / "poison"
        poison.mkdir()
        (poison / "WaylibFixture.pc").write_text(PC.replace("api_level=1", "api_level=99"), encoding="utf-8")
        with patch.dict(os.environ, {"PKG_CONFIG_PATH": str(poison), "PKG_CONFIG_LIBDIR": str(poison),
                                     "PKG_CONFIG_SYSROOT_DIR": "/unrelated-sysroot"}):
            after = self.snapshot("after")
        self.assertEqual(before["pkg_config"], after["pkg_config"])

    def test_invalid_package_and_missing_dependency_do_not_fall_back_to_text(self):
        for name, content in (("invalid", PC.replace("Description: Installed contract fixture\n", "")),
                              ("dependency", PC.replace("api_requires=", "api_requires=missing-unified-fixture-package"))):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "pkg-config"):
                self.snapshot(name, content)

    def test_legacy_unevaluated_pkg_config_snapshot_must_be_regenerated(self):
        snapshot = self.snapshot("before")
        snapshot["pkg_config"] = {"lib/pkgconfig/WaylibFixture.pc": {"Cflags": "${api_cflags}"}}
        result = compare_contract_snapshots(snapshot, snapshot, None, self.root)
        self.assertTrue(any("pkg-config" in error and "regenerate" in error for error in result["blocked_reasons"]), result)


if __name__ == "__main__":
    unittest.main()
