#!/usr/bin/env bash
set -euo pipefail

# Keep the generated Python form next to the package code used at runtime.
# Do not hand-edit that output: this command deliberately replaces it.
pyside6-uic "src/bwcsv/mainwindow.ui" -o "src/bwcsv/mainwindow.py"
