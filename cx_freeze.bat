@ECHO OFF
CLS

ECHO Removing cache directory...
RMDIR /Q /S "__pycache__"
RMDIR /Q /S "__pycache__"

ECHO Removing build directory...
RMDIR /Q /S "build"
RMDIR /Q /S "build"

ECHO Removing installers directory...
RMDIR /Q /S "installers"
RMDIR /Q /S "installers"

ECHO Creating installers directory...
MD "installers"

ECHO Compiling executable...
setup.py build

ECHO.

ECHO Copying application files...
COPY /Y "about.png" "build"
COPY /Y "fseparator.png" "build"
COPY /Y "hheader.png" "build"
COPY /Y "icon.png" "build"
COPY /Y "open_file.png" "build"
COPY /Y "quit.png" "build"
COPY /Y "setheader.png" "build"
COPY /Y "tdelimiter.png" "build"
COPY /Y "vheader.png" "build"

COPY /Y "test.csv" "build"

COPY /Y "gpl.txt" "build"
COPY /Y "icons.txt" "build"
COPY /Y "license.txt" "build"
COPY /Y "whats_new.txt" "build"

ECHO.
