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
nasm -f win64 "src\main.asm" -o "build\main.obj" || exit /b 1
nasm -f win64 "src\gui.asm" -o "build\gui.obj" || exit /b 1
nasm -f win64 "src\arithmetic.asm" -o "build\arithmetic.obj" || exit /b 1
nasm -f win64 "src\validation.asm" -o "build\validation.obj" || exit /b 1
cl /nologo /O2 /W4 /c /Fo:"build\win32_bridge.obj" "src\win32_bridge.c" || exit /b 1
link /NOLOGO /MACHINE:X64 /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup /OUT:"build\Calculator.exe" "build\main.obj" "build\gui.obj" "build\arithmetic.obj" "build\validation.obj" "build\win32_bridge.obj" user32.lib kernel32.lib || exit /b 1
echo.
echo BUILD OK: build\Calculator.exe
echo Run with: build\Calculator.exe
endlocal