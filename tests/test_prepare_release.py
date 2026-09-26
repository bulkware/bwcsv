"""Test changelog-driven release metadata synchronization."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "prepare_release.py"
MODULE_SPEC = importlib.util.spec_from_file_location("prepare_release", MODULE_PATH)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
PREPARE_RELEASE = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = PREPARE_RELEASE
MODULE_SPEC.loader.exec_module(PREPARE_RELEASE)


class PrepareReleaseTests(unittest.TestCase):
    """Keep changelog-driven release preparation synchronized and safe."""

    def test_updates_derived_metadata_from_latest_changelog_release(self):
        """The changelog is the only release version and date input."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n## [1.5.2] - 2026-09-26\n\n"
                "### Fixed\n\n- Correct release metadata.\n",
                encoding="utf-8",
            )
            (root / "pyproject.toml").write_text(
                "[project]\nversion = \"1.5.1\"\n", encoding="utf-8"
            )
            appstream = root / "data/org.bulkware.bwcsv.metainfo.xml"
            appstream.write_text(
                "<component>\n  <releases>\n    <release version=\"1.5.1\" date=\"2026-09-26\"/>\n"
                "  </releases>\n</component>\n",
                encoding="utf-8",
            )

            PREPARE_RELEASE.sync_release(root)

            self.assertIn('version = "1.5.2"', (root / "pyproject.toml").read_text())
            self.assertIn('release version="1.5.2" date="2026-09-26"', appstream.read_text())

    def test_rejects_draft_notes_before_writing_metadata(self):
        """A release entry must be published before derived metadata changes."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n### Fixed\n\n- Pending change.\n",
                encoding="utf-8",
            )
            pyproject = root / "pyproject.toml"
            pyproject.write_text("[project]\nversion = \"1.5.1\"\n", encoding="utf-8")
            (root / "data/org.bulkware.bwcsv.metainfo.xml").write_text(
                "<releases>\n</releases>\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(ValueError, "Unreleased"):
                PREPARE_RELEASE.sync_release(root)
            self.assertIn('version = "1.5.1"', pyproject.read_text())
