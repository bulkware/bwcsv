"""Locate bundled application assets in source, installed, and frozen builds."""

from importlib.resources import files
from pathlib import Path
import sys


def asset_path(name: str) -> str:
    """Return an absolute path to a bundled application asset."""
    # cx_Freeze exposes assets beside the executable; source and wheel installs
    # instead keep them inside the package directory.
    if getattr(sys, "frozen", False):
        return str(Path(sys.executable).resolve().parent / "assets" / name)
    return str(files("bwcsv").joinpath("assets", name))
