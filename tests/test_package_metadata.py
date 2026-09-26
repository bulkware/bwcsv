"""Test strict validation of release-note input."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/package_metadata.py"
MODULE_SPEC = importlib.util.spec_from_file_location("package_metadata", MODULE_PATH)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
PACKAGE_METADATA = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = PACKAGE_METADATA
MODULE_SPEC.loader.exec_module(PACKAGE_METADATA)


class PackageMetadataTests(unittest.TestCase):
    """Ensure native builds reject ambiguous release notes."""

    def test_current_changelog_is_a_valid_published_release(self):
        """The tracked changelog supplies the version and categorized package notes."""
        release = PACKAGE_METADATA.parse_changelog(ROOT / "CHANGELOG.md")

        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(release.version, project["project"]["version"])
        self.assertTrue(release.entries)
        self.assertTrue(all(category in PACKAGE_METADATA.CATEGORY_NAMES
                            for category, _ in release.entries))

    def test_rejects_unreleased_notes(self):
        """Draft notes cannot accidentally enter a native package."""
        changelog = """# Changelog

## [Unreleased]

### Fixed

- Pending change.

## [1.5.0] - 2026-09-23

### Changed

- Published change.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "CHANGELOG.md"
            path.write_text(changelog, encoding="utf-8")
            with self.assertRaisesRegex(PACKAGE_METADATA.ChangelogSyntaxError, "Unreleased"):
                PACKAGE_METADATA.parse_changelog(path)

    def test_rejects_unknown_categories(self):
        """Package release notes use a small, consistent category vocabulary."""
        changelog = """# Changelog

## [Unreleased]

## [1.5.0] - 2026-09-23

### Miscellaneous

- Published change.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "CHANGELOG.md"
            path.write_text(changelog, encoding="utf-8")
            with self.assertRaisesRegex(PACKAGE_METADATA.ChangelogSyntaxError, "unsupported"):
                PACKAGE_METADATA.parse_changelog(path)
