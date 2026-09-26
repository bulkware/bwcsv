"""Check identity and packaging metadata without native package toolchains."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from xml.etree import ElementTree

from bwcsv.resources import asset_path


ROOT = Path(__file__).resolve().parents[1]


class MetadataTests(unittest.TestCase):
    """Keep package metadata and release inputs synchronized."""

    def test_application_version_matches_project_and_appstream_metadata(self):
        """One release version must describe all user-visible package inputs."""
        # These three public-facing version sources must describe one release.
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        appstream = ElementTree.parse(ROOT / "data/org.bulkware.bwcsv.metainfo.xml")
        release = appstream.find("releases/release")

        self.assertIsNotNone(release)
        version = project["project"]["version"]
        self.assertEqual(release.attrib["version"], version)
        self.assertIn(f"## [{version}]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_runtime_assets_are_available_without_the_working_directory(self):
        """Icons are resolved from package data rather than process state."""
        # Resource lookup must be independent of the directory used to launch.
        for name in ("icon.png", "about.png", "open_file.png"):
            self.assertTrue(Path(asset_path(name)).is_file(), name)

    def test_native_metadata_generator_updates_staged_files(self):
        """Native package builds derive versions and notes from tracked metadata."""
        # Packaging generation must operate on copies, never tracked templates.
        with tempfile.TemporaryDirectory() as directory:
            staging = Path(directory)
            changelog = staging / "changelog"
            spec = staging / "bwcsv.spec"
            changelog.write_text("bwcsv (1.4.0-1) unstable; urgency=medium\n", encoding="utf-8")
            shutil.copy2(ROOT / "packaging/rpm/bwcsv.spec", spec)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/package_metadata.py"),
                    "--debian-changelog", str(changelog),
                    "--rpm-spec", str(spec),
                ],
                check=True,
                cwd=ROOT,
            )

            project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
            version = project["project"]["version"]
            generated_changelog = changelog.read_text(encoding="utf-8")
            self.assertIn(f"bwcsv ({version}-1)", generated_changelog)
            self.assertTrue(
                generated_changelog.endswith("bwcsv (1.4.0-1) unstable; urgency=medium\n")
            )
            self.assertIn(f"Version:        {version}", spec.read_text(encoding="utf-8"))

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/package_metadata.py"),
                    "--debian-changelog", str(changelog),
                ],
                check=True,
                cwd=ROOT,
            )
            self.assertEqual(generated_changelog, changelog.read_text(encoding="utf-8"))

    def test_native_metadata_generator_rejects_invalid_revisions(self):
        """Native package revisions must remain valid package-version components."""
        # argparse returns a non-zero status before writing a requested output.
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/package_metadata.py"),
                    "--debian-changelog", str(Path(directory) / "changelog"),
                    "--revision", "0",
                ],
                capture_output=True,
                check=False,
                text=True,
                cwd=ROOT,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("positive integer", result.stderr)
