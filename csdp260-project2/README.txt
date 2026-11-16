CSDP 260 Project 2 - NASM x64 Windows Calculator
Student: Standley Saint Leger Rock

START WITH START_HERE_LIVE_DEMO.txt.
The downloadable Actions artifact contains the generated build/Calculator.exe.
Extract the ZIP completely before running; Windows x64 is required.

Project layout
src/main.asm       entry point
src/gui.asm        Windows API GUI and event handling
src/arithmetic.asm signed integer arithmetic, scaled division
src/validation.asm input parsing and result formatting
src/win32_bridge.c preserved unused original; NOT linked into calculator
build.bat          NASM + Microsoft linker build
.vscode/tasks.json Windows build task
windows_test.ps1   actual Windows GUI tests with WM_CHAR typed input
 test_routines.c   independent C harness calling NASM (not app arithmetic)
documentation/     technical report, manual, testing and missing-items status
screenshots/       genuine captures generated during Windows verification
video/             actual narrated MP4 required; currently absent

Build prerequisites: NASM in PATH and Visual Studio C++ Build Tools with
Windows SDK. Open x64 Native Tools Command Prompt for VS, cd to this folder,
then run build.bat. Launch build\Calculator.exe.
For VS Code, run `code .` from that same developer prompt, then Ctrl+Shift+B.
No C/C++ compiler is needed to build the calculator; CI uses cl for the
independent test harness only. No external runtime or network is required.

Inputs: signed 32-bit integers (-2147483648..2147483647), optional sign and
surrounding spaces/tabs. Decimal input is not supported. Results use signed
64-bit arithmetic; division rounds to four decimal places (half away from
zero) and removes trailing zeros. Clear resets fields; Exit closes the app.

Submission status: NOT COMPLETE FOR CANVAS until the student's genuine
narrated video and any instructor-required original report are supplied.
See documentation/MISSING_ITEMS.txt and TESTING_REPORT.txt. The Actions ZIP
is a verified software/demo package, not proof all grading requirements exist.
