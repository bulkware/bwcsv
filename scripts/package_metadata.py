#!/usr/bin/env python3
"""Generate native-package changelog entries from project metadata."""

from __future__ import annotations

import argparse
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
import re
import tomllib


RELEASE = re.compile(r"^## \[(?P<version>\d+\.\d+\.\d+)\] - (?P<date>\d{4}-\d{2}-\d{2})$")
BULLET = re.compile(r"^- (?P<text>\S.*)$")


def latest_release(changelog: Path) -> tuple[str, date, list[str]]:
    """Read the first dated release and its user-facing notes."""
    # CHANGELOG is newest-first, so the first matching heading is the release
    # that native package metadata must describe.
    lines = changelog.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        match = RELEASE.fullmatch(line)
        if match is None:
            continue
        notes: list[str] = []
        for entry in lines[index + 1:]:
            if entry.startswith("## "):
                break
            bullet = BULLET.fullmatch(entry)
            if bullet:
                notes.append(bullet["text"])
        if not notes:
            raise ValueError(f"{changelog} has no entries for {match['version']}")
        return match["version"], date.fromisoformat(match["date"]), notes
    raise ValueError(f"{changelog} has no dated releases")


def project_metadata(project_file: Path) -> tuple[str, str, str, str]:
    """Return the package identity and maintainer from PEP 621 metadata."""
    project = tomllib.loads(project_file.read_text(encoding="utf-8"))["project"]
    author = project["authors"][0]
    return project["name"].lower(), project["version"], author["name"], author["email"]


def debian_changelog(
    path: Path, package: str, version: str, revision: str, release_date: date,
    notes: list[str], maintainer: str, email: str,
) -> None:
    """Prepend the current Debian-native changelog entry once."""
    timestamp = format_datetime(datetime.combine(release_date, time(), timezone.utc))
    entries = "\n".join(f"  * {note}" for note in notes)
    entry = (
        f"{package} ({version}-{revision}) unstable; urgency=medium\n\n{entries}\n\n"
        f" -- {maintainer} <{email}>  {timestamp}\n"
    )
    # Package rebuilds must not discard or duplicate prior native-package notes.
    contents = path.read_text(encoding="utf-8") if path.exists() else ""
    if not contents.startswith(f"{package} ({version}-{revision}) "):
        path.write_text(entry + contents, encoding="utf-8")


def rpm_spec(path: Path, version: str, revision: str, release_date: date, notes: list[str],
             maintainer: str, email: str) -> None:
    """Update a staged RPM spec without modifying its tracked template."""
    # The RPM build works from a copy so versioning a package never dirties the
    # source-controlled spec file.
    contents = path.read_text(encoding="utf-8")
    contents = re.sub(r"(?m)^Version:\s+.*$", f"Version:        {version}", contents)
    contents = re.sub(r"(?m)^Release:\s+.*$", f"Release:        {revision}%{{?dist}}", contents)
    entries = "\n".join(f"- {note}" for note in notes)
    stamp = release_date.strftime("%a %b %d %Y")
    changelog = f"%changelog\n* {stamp} {maintainer} <{email}> - {version}-{revision}\n{entries}\n"
    path.write_text(re.sub(r"(?s)%changelog\n.*\Z", changelog, contents), encoding="utf-8")


def main() -> int:
    """Synchronize requested native-package metadata with the project release."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--debian-changelog", type=Path)
    parser.add_argument("--rpm-spec", type=Path)
    parser.add_argument("--revision", default="1")
    arguments = parser.parse_args()
    if not re.fullmatch(r"[1-9]\d*", arguments.revision):
        parser.error("--revision must be a positive integer")
    root = Path(__file__).resolve().parents[1]
    package, version, maintainer, email = project_metadata(root / "pyproject.toml")
    release_version, release_date, notes = latest_release(root / "CHANGELOG.md")
    if version != release_version:
        raise ValueError(f"pyproject.toml is {version}, but CHANGELOG.md is {release_version}")
    if arguments.debian_changelog:
        debian_changelog(
            arguments.debian_changelog, package, version, arguments.revision, release_date,
            notes, maintainer, email,
        )
    if arguments.rpm_spec:
        rpm_spec(arguments.rpm_spec, version, arguments.revision, release_date, notes,
                 maintainer, email)
    if not arguments.debian_changelog and not arguments.rpm_spec:
        parser.error("select --debian-changelog and/or --rpm-spec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
