; Calculator arithmetic procedures (all arithmetic is implemented in NASM).
; Windows x64 ABI: RCX = first signed 32-bit-range integer; RDX = second.
; Return RAX = signed 64-bit result; division returns a scaled result (x 10000).
; EDX = status: 0 = OK, 1 = division by zero (division only).
; Input bounds guarantee add/sub/mul and scaled division fit signed 64-bit.
default rel
bits 64

global calc_add, calc_subtract, calc_multiply, calc_divide

section .text
calc_add:
    mov rax, rcx
    add rax, rdx
    xor edx, edx
    ret

calc_subtract:
    mov rax, rcx
    sub rax, rdx
    xor edx, edx
    ret

calc_multiply:
    mov rax, rcx
    imul rax, rdx
    xor edx, edx
    ret

calc_divide:
    test rdx, rdx
    jz .divide_by_zero

    ; Absolute values, then unsigned division; source values are within int32.
    ; Sign is negative if exactly one operand is negative.
    mov r8, rcx
    mov r9, rdx
    xor r10d, r10d
    test r8, r8
    jns .abs_divisor
    neg r8
    xor r10d, 1
.abs_divisor:
    test r9, r9
    jns .do_division
    neg r9
    xor r10d, 1
.do_division:
    ; Rounded to nearest 1/10000, half away from zero.
    ; With int32 operands: abs(a)*10000 + abs(b)/2 cannot overflow int64.
    mov rax, r8
    imul rax, rax, 10000
    mov r11, r9
    shr r11, 1
    add rax, r11
    xor edx, edx
    div r9
    test r10d, r10d
    jz .success
    neg rax
.success:
    xor edx, edx
    ret
.divide_by_zero:
    xor eax, eax
    mov edx, 1
    ret