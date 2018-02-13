#!/usr/bin/python
# -*- coding: utf-8 -*-

""" cx_Freeze setup script for bwCSV. """

# Python imports
import sys # System-specific parameters and functions

# cx_Freeze imports
from cx_Freeze import setup, Executable, build_exe

# Build options
buildOptions = dict(
    create_shared_zip = False)

# Platform specific
script = "main.py"
if sys.platform == 'win32':
    exe = Executable(script, appendScriptToExe = True,
                    appendScriptToLibrary = False, base = "Win32GUI",
                    targetDir = "build", targetName = "bwCSV.exe",
                    icon = "icon_256x256.ico")
else:
    exe = Executable(script, targetDir = "build", targetName = "bwCSV")

# Setup
setup(
    name = "bwCSV",
    version = "1.00",
    description = "A lightweight application to view CSV-files.",
    author = 'bulkware',
    options = dict(build_exe = buildOptions),
    executables = [exe])
