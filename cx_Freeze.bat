@ECHO OFF
CLS

ECHO Removing cache...
RMDIR /Q /S "__pycache__"
RMDIR /Q /S "__pycache__"

ECHO Removing build...
RMDIR /Q /S "build"
RMDIR /Q /S "build"

ECHO Compiling executable...
setup.py build

ECHO.

ECHO Copying application files...
COPY /Y "test.csv" "build"
COPY /Y "GPL.txt" "build"
COPY /Y "License.txt" "build"
COPY /Y "WhatsNew.txt" "build"

ECHO.
