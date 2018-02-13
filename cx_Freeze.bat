@ECHO OFF
CLS

ECHO Compiling .exe-file...
setup.py build

ECHO.

ECHO Copying application files...
COPY /Y "test.csv" "build"
COPY /Y "GPL.txt" "build"
COPY /Y "License.txt" "build"
COPY /Y "WhatsNew.txt" "build"

ECHO.

ECHO Deleting configuration files...
DEL /Q /S "config.cfg"
