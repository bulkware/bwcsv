#!/usr/bin/env python3
"""Remove build output and Python caches without touching project data."""

from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "build", ROOT / "dist", ROOT / ".coverage")


def main() -> int:
    """Remove known generated directories and files."""
    # Restrict cleanup to disposable paths rooted in this checkout.
    for target in TARGETS:
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    # Build backends leave metadata and bytecode in different locations.
    for metadata in (ROOT / "src").glob("*.egg-info"):
        if metadata.is_dir():
            shutil.rmtree(metadata)
    for cache in ROOT.rglob("__pycache__"):
        if cache.is_dir() and not cache.is_symlink():
            shutil.rmtree(cache)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
