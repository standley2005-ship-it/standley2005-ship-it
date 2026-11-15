; Signed int32 input parser and NASM result formatting.
; parse_int32: RCX -> NUL-terminated ASCII string. RAX = value, EDX = status
; (0 valid, 1 missing, 2 invalid characters, 3 out of signed-int32 range).
; format_int64: RCX = signed integer -> RAX = pointer to string.
; format_fixed4: RCX = signed value scaled by 10,000 -> RAX = pointer.
; Both format functions use the same buffer (single-threaded GUI).
default rel
bits 64

global parse_int32, format_int64, format_fixed4

section .data
    ten dq 10
    scale dq 10000

section .bss
    output_buffer resb 80

section .text
parse_int32:
    mov r10, rcx                 ; input cursor
    xor eax, eax                 ; unsigned magnitude
    xor r8d, r8d                 ; negative flag
    xor r9d, r9d                 ; digits consumed
.skip_leading:
    movzx r11d, byte [r10]
    cmp r11b, ' '
    je .advance_leading
    cmp r11b, 9                  ; horizontal tab
    jne .check_sign
.advance_leading:
    inc r10
    jmp .skip_leading
.check_sign:
    test r11b, r11b
    jz .missing
    cmp r11b, '-'
    jne .plus_sign
    mov r8d, 1
    inc r10
    jmp .digit_loop
.plus_sign:
    cmp r11b, '+'
    jne .digit_loop
    inc r10
.digit_loop:
    movzx r11d, byte [r10]
    cmp r11b, '0'
    jb .end_digits
    cmp r11b, '9'
    ja .end_digits
    imul rax, rax, 10
    sub r11d, '0'
    add rax, r11
    mov r11, 2147483648         ; largest allowed magnitude (negative only)
    cmp rax, r11
    ja .out_of_range
    inc r9d
    inc r10
    jmp .digit_loop
.end_digits:
    test r9d, r9d
    jz .invalid
.skip_trailing:
    movzx r11d, byte [r10]
    test r11b, r11b
    jz .range_and_sign
    cmp r11b, ' '
    je .advance_trailing
    cmp r11b, 9
    jne .invalid
.advance_trailing:
    inc r10
    jmp .skip_trailing
.range_and_sign:
    test r8d, r8d
    jnz .make_negative
    cmp rax, 2147483647
    ja .out_of_range
    xor edx, edx
    ret
.make_negative:
    neg rax
    xor edx, edx
    ret
.missing:
    xor eax, eax
    mov edx, 1
    ret
.invalid:
    xor eax, eax
    mov edx, 2
    ret
.out_of_range:
    xor eax, eax
    mov edx, 3
    ret

format_int64:
    mov rax, rcx
    xor r11d, r11d
    test rax, rax
    jns .start
    neg rax
    mov r11d, 1
.start:
    lea r10, [output_buffer + 79]
    mov byte [r10], 0
.digit:
    xor edx, edx
    div qword [ten]
    add dl, '0'
    dec r10
    mov [r10], dl
    test rax, rax
    jnz .digit
    test r11d, r11d
    jz .done
    dec r10
    mov byte [r10], '-'
.done:
    mov rax, r10
    ret

format_fixed4:
    ; Format a signed scaled integer, removing trailing decimal zeros.
    ; E.g. 75000 -> "7.5", -5000 -> "-0.5", 10000 -> "1".
    mov rax, rcx
    xor r11d, r11d
    test rax, rax
    jns .abs_value
    neg rax
    mov r11d, 1
.abs_value:
    xor edx, edx
    div qword [scale]
    mov r8, rax                  ; whole-part magnitude
    mov r9, rdx                  ; fractional digits as 0..9999
    lea r10, [output_buffer + 79]
    mov byte [r10], 0
    test r9, r9
    jz .write_whole
    mov ecx, 4                   ; original fractional precision
.trim_zero:
    mov rax, r9
    xor edx, edx
    div qword [ten]
    test rdx, rdx
    jnz .write_fraction
    mov r9, rax
    dec ecx
    jmp .trim_zero
.write_fraction:
    mov rax, r9
.frac_digit:
    xor edx, edx
    div qword [ten]
    add dl, '0'
    dec r10
    mov [r10], dl
    dec ecx
    jnz .frac_digit
    dec r10
    mov byte [r10], '.'
.write_whole:
    mov rax, r8
.whole_digit:
    xor edx, edx
    div qword [ten]
    add dl, '0'
    dec r10
    mov [r10], dl
    test rax, rax
    jnz .whole_digit
    test r11d, r11d
    jz .done
    dec r10
    mov byte [r10], '-'
.done:
    mov rax, r10
    ret