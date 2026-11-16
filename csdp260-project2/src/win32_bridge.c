/* Thin Win32 text-control bridge. Calculation and validation remain in NASM. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
int win32_read_edit(void *edit_handle, char *buffer, int capacity) {
    if (!buffer || capacity < 2) return 0;
    buffer[0] = '\0';
    if (!edit_handle) return 0;
    return GetWindowTextA((HWND)edit_handle, buffer, capacity);
}
