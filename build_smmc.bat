@echo off
echo ========================================
echo Building SMMC PDF Margin Adjuster
echo ========================================

echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 2: Verifying dependencies...
pip list | find "PyPDF2" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing PyPDF2...
    pip install PyPDF2==3.0.1
)

pip list | find "PyMuPDF" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing PyMuPDF...
    pip install PyMuPDF==1.23.14
)

pip list | find "reportlab" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing reportlab...
    pip install reportlab==4.0.7
)

pip list | find "Pillow" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Pillow...
    pip install Pillow==10.1.0
)

pip list | find "pyinstaller" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing PyInstaller...
    pip install pyinstaller==6.3.0
)

echo Step 3: Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Step 4: Building executable with PyInstaller...
pyinstaller SMMC.spec

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)

echo Step 5: Verifying executable...
if not exist "dist\SMMC.exe" (
    echo ERROR: SMMC.exe was not created!
    pause
    exit /b 1
)

echo Step 6: Building installer with Inno Setup...
if not exist "installer" (
    echo ERROR: installer directory not found!
    echo Please create the installer directory with setup.iss
    pause
    exit /b 1
)

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss

if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Inno Setup build failed or not found!
    echo Trying alternative path...
    "C:\Program Files\Inno Setup 6\ISCC.exe" installer\setup.iss
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Could not find Inno Setup compiler!
        echo Please install Inno Setup from https://jrsoftware.org/isdl.php
        echo Build completed but installer creation failed.
        goto :end
    )
)

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Files created:
echo - Executable: dist\SMMC.exe
if exist "installer\output\SMMC_PDF_Adjuster_v1.0.0_Setup.exe" (
    echo - Installer: installer\output\SMMC_PDF_Adjuster_v1.0.0_Setup.exe
)
echo.

:end
pause