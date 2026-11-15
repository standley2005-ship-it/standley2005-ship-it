; Windows x64 Win32 native GUI implemented in NASM.
; Window creation, control events, validation, arithmetic dispatch, result display.
default rel
bits 64

global gui_start
extern GetModuleHandleA, LoadCursorA, RegisterClassExA
extern CreateWindowExA, ShowWindow, UpdateWindow
extern GetMessageA, TranslateMessage, DispatchMessageA
extern DefWindowProcA, PostQuitMessage, DestroyWindow
extern GetWindowTextA, SetWindowTextA, GetDlgItem, GetDlgItemTextA, GetDlgItemInt
extern parse_int32, format_int64, format_fixed4
extern calc_add, calc_subtract, calc_multiply, calc_divide

%define WM_DESTROY  2
%define WM_CLOSE    16
%define WM_COMMAND  273
%define ID_ADD      101
%define ID_SUB      102
%define ID_MUL      103
%define ID_DIV      104
%define ID_CLEAR    105
%define ID_EXIT     106
%define WS_STATIC   0x50000000
%define WS_EDIT     0x50810080 ; WS_CHILD|VISIBLE|TABSTOP|BORDER|ES_AUTOHSCROLL
%define WS_BUTTON   0x50010000 ; WS_CHILD|VISIBLE|TABSTOP
%define WS_BORDERED 0x50800000 ; child/visible/border

section .data
    app_class db 'CSDP260NASMCalc', 0
    app_title db 'CSDP 260 - NASM Assembly Calculator', 0
    cls_static db 'STATIC', 0
    cls_edit db 'EDIT', 0
    cls_button db 'BUTTON', 0
    label_one db 'Number 1:', 0
    label_two db 'Number 2:', 0
    label_result db 'Result:', 0
    label_status db 'Status / error:', 0
    txt_add db 'Add (+)', 0
    txt_sub db 'Subtract (-)', 0
    txt_mul db 'Multiply (*)', 0
    txt_div db 'Divide (/)', 0
    txt_clear db 'Clear', 0
    txt_exit db 'Exit', 0
    txt_empty db '', 0
    txt_ready db 'Ready. Enter two whole numbers.', 0
    txt_done db 'Calculation completed.', 0
    err_missing db 'Please enter both numbers.', 0
    err_invalid db 'Invalid input. Use whole numbers only.', 0
    err_range db 'Out of range: -2147483648 to 2147483647.', 0
    err_divzero db 'Cannot divide by zero.', 0

    ; WNDCLASSEXA: 80 bytes on Windows x64.
    wnd_class:
        dd 80, 3                 ; cbSize; CS_HREDRAW|CS_VREDRAW
        dq window_proc          ; lpfnWndProc
        dd 0, 0                 ; cbClsExtra; cbWndExtra
        dq 0                     ; hInstance (set at runtime)
        dq 0                     ; hIcon
        dq 0                     ; hCursor (set at runtime)
        dq 6                     ; (HBRUSH)(COLOR_WINDOW+1)
        dq 0                     ; lpszMenuName
        dq app_class             ; lpszClassName
        dq 0                     ; hIconSm

    ; Control descriptor: class*, text*, x,y,width,height,style,id,outHwnd*.
    ; Controls are created in logical tab order; only edits/buttons get WS_TABSTOP.
    c_label1: dq cls_static, label_one
              dd 22, 25, 95, 24, WS_STATIC, 0
              dq dummy_handle
    c_edit1:  dq cls_edit, txt_empty
              dd 126, 22, 195, 29, WS_EDIT, 301
              dq h_input1
    c_label2: dq cls_static, label_two
              dd 22, 64, 95, 24, WS_STATIC, 0
              dq dummy_handle
    c_edit2:  dq cls_edit, txt_empty
              dd 126, 61, 195, 29, WS_EDIT, 302
              dq h_input2
    c_add:    dq cls_button, txt_add
              dd 22, 112, 130, 34, WS_BUTTON, ID_ADD
              dq dummy_handle
    c_sub:    dq cls_button, txt_sub
              dd 160, 112, 130, 34, WS_BUTTON, ID_SUB
              dq dummy_handle
    c_mul:    dq cls_button, txt_mul
              dd 298, 112, 130, 34, WS_BUTTON, ID_MUL
              dq dummy_handle
    c_div:    dq cls_button, txt_div
              dd 436, 112, 130, 34, WS_BUTTON, ID_DIV
              dq dummy_handle
    c_resultlabel: dq cls_static, label_result
              dd 22, 169, 95, 24, WS_STATIC, 0
              dq dummy_handle
    c_result: dq cls_static, txt_empty
              dd 126, 165, 440, 30, WS_BORDERED, 0
              dq h_result
    c_statuslabel: dq cls_static, label_status
              dd 22, 207, 130, 24, WS_STATIC, 0
              dq dummy_handle
    c_status: dq cls_static, txt_ready
              dd 160, 204, 406, 30, WS_BORDERED, 0
              dq h_status
    c_clear:  dq cls_button, txt_clear
              dd 326, 251, 114, 34, WS_BUTTON, ID_CLEAR
              dq dummy_handle
    c_exit:   dq cls_button, txt_exit
              dd 452, 251, 114, 34, WS_BUTTON, ID_EXIT
              dq dummy_handle

section .bss
    h_instance resq 1
    h_main resq 1
    h_input1 resq 1
    h_input2 resq 1
    h_result resq 1
    h_status resq 1
    dummy_handle resq 1
    parse_ok resd 1
    buffer1 resb 64
    buffer2 resb 64
    operand1 resq 1
    operand2 resq 1
    msg resb 48                 ; Windows x64 MSG structure

section .text
gui_start:
    push rbx
    sub rsp, 112                ; 32-byte home area + 8 args + local/alignment

    xor ecx, ecx
    call GetModuleHandleA
    test rax, rax
    jz .startup_failed
    mov [h_instance], rax
    mov [wnd_class + 24], rax

    xor ecx, ecx
    mov edx, 32512              ; IDC_ARROW
    call LoadCursorA
    mov [wnd_class + 40], rax

    lea rcx, [wnd_class]
    call RegisterClassExA
    test eax, eax
    jz .startup_failed

    xor ecx, ecx                ; dwExStyle
    lea rdx, [app_class]
    lea r8, [app_title]
    mov r9d, 0x00CF0000         ; WS_OVERLAPPEDWINDOW
    mov qword [rsp + 32], 100   ; X
    mov qword [rsp + 40], 100   ; Y
    mov qword [rsp + 48], 610   ; width
    mov qword [rsp + 56], 350   ; height
    mov qword [rsp + 64], 0     ; parent
    mov qword [rsp + 72], 0     ; menu
    mov rax, [h_instance]
    mov [rsp + 80], rax
    mov qword [rsp + 88], 0     ; lpParam
    call CreateWindowExA
    test rax, rax
    jz .startup_failed
    mov [h_main], rax
    call create_all_controls

    mov rcx, [h_main]
    mov edx, 1                  ; SW_SHOWNORMAL
    call ShowWindow
    mov rcx, [h_main]
    call UpdateWindow

.message_loop:
    lea rcx, [msg]
    xor edx, edx
    xor r8d, r8d
    xor r9d, r9d
    call GetMessageA
    cmp eax, 0
    je .normal_exit
    jl .startup_failed
    lea rcx, [msg]
    call TranslateMessage
    lea rcx, [msg]
    call DispatchMessageA
    jmp .message_loop
.normal_exit:
    xor eax, eax
    jmp .gui_return
.startup_failed:
    mov eax, 1
.gui_return:
    add rsp, 112
    pop rbx
    ret

; RCX = pointer to 48-byte control descriptor.
create_control:
    push rbx
    sub rsp, 96                 ; 32-byte home + eight extra arguments
    mov rbx, rcx
    xor ecx, ecx
    mov rdx, [rbx + 0]         ; class
    mov r8, [rbx + 8]          ; text
    mov r9d, [rbx + 32]        ; style
    mov eax, [rbx + 16]
    mov [rsp + 32], rax        ; x
    mov eax, [rbx + 20]
    mov [rsp + 40], rax        ; y
    mov eax, [rbx + 24]
    mov [rsp + 48], rax        ; width
    mov eax, [rbx + 28]
    mov [rsp + 56], rax        ; height
    mov rax, [h_main]
    mov [rsp + 64], rax        ; parent
    mov eax, [rbx + 36]
    mov [rsp + 72], rax        ; HMENU = control id
    mov rax, [h_instance]
    mov [rsp + 80], rax
    mov qword [rsp + 88], 0
    call CreateWindowExA
    mov rdx, [rbx + 40]
    mov [rdx], rax
    add rsp, 96
    pop rbx
    ret

create_all_controls:
    sub rsp, 40                 ; caller's RSP was 8 mod 16
    lea rcx, [c_label1]
    call create_control
    lea rcx, [c_edit1]
    call create_control
    lea rcx, [c_label2]
    call create_control
    lea rcx, [c_edit2]
    call create_control
    lea rcx, [c_add]
    call create_control
    lea rcx, [c_sub]
    call create_control
    lea rcx, [c_mul]
    call create_control
    lea rcx, [c_div]
    call create_control
    lea rcx, [c_resultlabel]
    call create_control
    lea rcx, [c_result]
    call create_control
    lea rcx, [c_statuslabel]
    call create_control
    lea rcx, [c_status]
    call create_control
    lea rcx, [c_clear]
    call create_control
    lea rcx, [c_exit]
    call create_control
    add rsp, 40
    ret

; Win64 WNDPROC(HWND rcx, UINT edx, WPARAM r8, LPARAM r9)
window_proc:
    push rbx
    sub rsp, 32
    mov rbx, rcx
    cmp edx, WM_COMMAND
    je .command
    cmp edx, WM_CLOSE
    je .close
    cmp edx, WM_DESTROY
    je .destroy
    call DefWindowProcA
    jmp .return
.command:
    movzx eax, r8w             ; LOWORD(wParam): button/control ID
    cmp eax, ID_ADD
    jb .handled
    cmp eax, ID_DIV
    jbe .calculate
    cmp eax, ID_CLEAR
    je .clear
    cmp eax, ID_EXIT
    je .close
    jmp .handled
.calculate:
    mov ecx, eax
    call perform_calculation
    jmp .handled
.clear:
    call clear_fields
    jmp .handled
.close:
    mov rcx, rbx
    call DestroyWindow
    jmp .handled
.destroy:
    xor ecx, ecx
    call PostQuitMessage
.handled:
    xor eax, eax
.return:
    add rsp, 32
    pop rbx
    ret

; RCX = clicked operation ID.
perform_calculation:
    push rbx
    sub rsp, 32
    mov ebx, ecx

    ; Read signed integers through Win32; arithmetic remains NASM.
    mov rcx, [h_main]
    mov edx, 301
    lea r8, [parse_ok]
    mov r9d, 1
    call GetDlgItemInt
    cmp dword [parse_ok], 0
    je .parse_input_error
    movsxd rax, eax
    mov [operand1], rax

    mov rcx, [h_main]
    mov edx, 302
    lea r8, [parse_ok]
    mov r9d, 1
    call GetDlgItemInt
    cmp dword [parse_ok], 0
    je .parse_input_error
    movsxd rax, eax
    mov [operand2], rax

    mov rcx, [operand1]
    mov rdx, [operand2]
    cmp ebx, ID_ADD
    je .add
    cmp ebx, ID_SUB
    je .sub
    cmp ebx, ID_MUL
    je .mul
    jmp .divide
.add:
    call calc_add
    jmp .integer_result
.sub:
    call calc_subtract
    jmp .integer_result
.mul:
    call calc_multiply
.integer_result:
    mov rcx, rax
    call format_int64
    jmp .display_result
.divide:
    call calc_divide
    test edx, edx
    jnz .divide_error
    mov rcx, rax
    call format_fixed4
.display_result:
    mov rdx, rax
    mov rcx, [h_result]
    call SetWindowTextA
    mov rcx, [h_status]
    lea rdx, [txt_done]
    call SetWindowTextA
    jmp .finished
.parse_input_error:
    lea rcx, [err_invalid]
    call show_error
    jmp .finished
.parse_error:
    mov ecx, edx
    call set_parse_error
    jmp .finished
.divide_error:
    lea rcx, [err_divzero]
    call show_error
.finished:
    add rsp, 32
    pop rbx
    ret

; RCX = error code from parse_int32
set_parse_error:
    cmp ecx, 1
    je .missing
    cmp ecx, 3
    je .range
    lea rcx, [err_invalid]
    jmp show_error
.missing:
    lea rcx, [err_missing]
    jmp show_error
.range:
    lea rcx, [err_range]
    jmp show_error

; RCX = pointer to readable error string
show_error:
    push rbx
    sub rsp, 32
    mov rbx, rcx
    mov rcx, [h_result]
    lea rdx, [txt_empty]
    call SetWindowTextA
    mov rcx, [h_status]
    mov rdx, rbx
    call SetWindowTextA
    add rsp, 32
    pop rbx
    ret

clear_fields:
    sub rsp, 40
    mov rcx, [h_input1]
    lea rdx, [txt_empty]
    call SetWindowTextA
    mov rcx, [h_input2]
    lea rdx, [txt_empty]
    call SetWindowTextA
    mov rcx, [h_result]
    lea rdx, [txt_empty]
    call SetWindowTextA
    mov rcx, [h_status]
    lea rdx, [txt_ready]
    call SetWindowTextA
    add rsp, 40
    ret