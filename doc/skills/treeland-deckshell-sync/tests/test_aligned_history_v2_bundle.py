from __future__ import annotations

import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


from aligned_history_v2.bundle import bundle_files


def test_bundle_excludes_pytest_cache(tmp_path: Path) -> None:
    source = tmp_path / "scripts/tool.py"
    cache = tmp_path / ".pytest_cache/CACHEDIR.TAG"
    source.parent.mkdir()
    cache.parent.mkdir()
    source.write_text("pass\n", encoding="utf-8")
    cache.write_text("cache\n", encoding="utf-8")

    assert bundle_files(tmp_path, "doc/skill") == {
        "doc/skill/scripts/tool.py": b"pass\n"
    }
