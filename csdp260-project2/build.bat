@echo off
setlocal
cd /d "%~dp0"
if not exist "build" mkdir "build"
where nasm >nul 2>nul
if errorlevel 1 (
  echo ERROR: NASM not found. Install NASM and add it to PATH.
  exit /b 1
)
where link >nul 2>nul
if errorlevel 1 (
  echo ERROR: Microsoft link.exe not found.
  echo Run this file from an x64 Native Tools Command Prompt for Visual Studio.
  exit /b 1
)
nasm -f win64 "Standley_Saint_Leger_Rock_CSDP260_Project2_main.asm" -o "build\main.obj" || exit /b 1
nasm -f win64 "Standley_Saint_Leger_Rock_CSDP260_Project2_gui.asm" -o "build\gui.obj" || exit /b 1
nasm -f win64 "Standley_Saint_Leger_Rock_CSDP260_Project2_arithmetic.asm" -o "build\arithmetic.obj" || exit /b 1
nasm -f win64 "Standley_Saint_Leger_Rock_CSDP260_Project2_validation.asm" -o "build\validation.obj" || exit /b 1
link /NOLOGO /MACHINE:X64 /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup /OUT:"build\Calculator.exe" "build\main.obj" "build\gui.obj" "build\arithmetic.obj" "build\validation.obj" user32.lib kernel32.lib || exit /b 1
echo.
echo BUILD OK: build\Calculator.exe
echo Run with: build\Calculator.exe
endlocal