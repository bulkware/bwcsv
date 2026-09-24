"""bwCSV package metadata."""

from importlib.metadata import PackageNotFoundError, version

# Resolve the installed version when possible, while retaining a useful label
# for direct source-checkout launches.
try:
    __version__ = version("bwCSV")
except PackageNotFoundError:
    # A checkout can run before an editable installation has created dist-info.
    __version__ = "development"
