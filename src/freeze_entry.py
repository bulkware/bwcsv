"""cx_Freeze entry point that preserves bwCSV's package-relative imports."""

# Keep Qt imports visible at the entry point so cx_Freeze applies its PySide6 hook.
from shiboken6 import Shiboken
from PySide6 import QtCore, QtGui, QtWidgets

# Importing the package entry point, rather than executing a source file, keeps
# relative imports working in the frozen application.
from bwcsv.main import main


if __name__ == "__main__":
    raise SystemExit(main())
