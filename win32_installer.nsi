; The name of the installer
Name "bwCSV"

; The file to write
OutFile "installers\bwcsv_1.1.0_installer_win32.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\bwCSV"

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\bwCSV" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages
Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "bwCSV (required)"

    SectionIn RO

    ; Set output path to the installation directory.
    SetOutPath $INSTDIR

    ; Put application files there
    File "build\*.*"

    ; Write the installation path into the registry
    WriteRegStr HKLM "SOFTWARE\bwCSV" "Install_Dir" "$INSTDIR"

    ; Write the uninstall keys for Windows
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwCSV" "DisplayName" "bwCSV"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwCSV" "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwCSV" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwCSV" "NoRepair" 1
    WriteUninstaller "Uninstall.exe"

SectionEnd


; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

    CreateDirectory "$SMPROGRAMS\bwCSV"
    CreateShortCut "$SMPROGRAMS\bwCSV\bwCSV.lnk" "$INSTDIR\bwCSV.exe" "" "$INSTDIR\bwCSV.exe" 0
    CreateShortCut "$SMPROGRAMS\bwCSV\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0

SectionEnd

;--------------------------------

; Uninstaller
Section "Uninstall"

    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\bwCSV"
    DeleteRegKey HKLM "SOFTWARE\bwCSV"

    ; Remove files
    Delete "$INSTDIR\*.*"

    ; Remove shortcuts, if any
    Delete "$SMPROGRAMS\bwCSV\*.*"

    ; Remove directories used
    RMDir "$SMPROGRAMS\bwCSV"
    RMDir "$INSTDIR"

SectionEnd
