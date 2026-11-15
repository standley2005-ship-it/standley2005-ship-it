; CSDP 260 Project 2 — x86-64 NASM Windows GUI calculator
; Program entry point. Build as /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup.
default rel
bits 64

global mainCRTStartup
extern gui_start
extern ExitProcess

section .text
mainCRTStartup:
    ; At entry RSP is 8 mod 16. Reserve 32-byte shadow space + 8 alignment.
    sub rsp, 40
    call gui_start                ; EAX = program exit code
    mov ecx, eax
    call ExitProcess             ; no return