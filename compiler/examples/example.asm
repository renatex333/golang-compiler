
; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data
formatin: db "%d", 0
formatout: db "%d", 10, 0 ; newline, null terminator
scanint: times 4 db 0 ; 32-bit integer = 4 bytes

segment .bss ; variables
res RESB 1

section .text
global main ; linux
extern scanf ; linux
extern printf ; linux

; subrotines if/while
binop_je:
    JE binop_true
    JMP binop_false
binop_jg:
    JG binop_true
    JMP binop_false
binop_jl:
    JL binop_true
    JMP binop_false
binop_false:
    MOV EAX, False
    JMP binop_exit
binop_true:
    MOV EAX, True
binop_exit:
    RET

main:
    PUSH EBP ; stores the base pointer
    MOV EBP, ESP ; stabilishes a new base pointer
    ; code generated by the compiler
	PUSH DWORD 0
	PUSH DWORD 0
	MOV EAX, 1
	PUSH EAX
	MOV EAX, 3
	POP EBX
	ADD EAX, EBX
	MOV [EBP - 4], EAX
	MOV EAX, [EBP - 4]
	MOV [EBP - 8], EAX
	MOV EAX, 1
	PUSH EAX
	MOV EAX, [EBP - 4]
	POP EBX
	CMP EAX, EBX
	CALL binop_jg
	CMP EAX, False
	JE EXIT_22
	MOV EAX, 1
	PUSH EAX
	MOV EAX, 5
	POP EBX
	SUB EAX, EBX
	MOV [EBP - 4], EAX
	EXIT_22:
	MOV EAX, 3
	PUSH EAX
	MOV EAX, [EBP - 4]
	POP EBX
	CMP EAX, EBX
	CALL binop_je
	CMP EAX, False
	JE EXIT_31
	EXIT_31:
	MOV EAX, 3
	MOV [EBP - 4], EAX
	MOV EAX, 3
	MOV [EBP - 4], EAX
	LOOP_49:
		MOV EAX, 5
		PUSH EAX
		MOV EAX, [EBP - 4]
		POP EBX
		CMP EAX, EBX
		CALL binop_jl
		CMP EAX, False
		JE EXIT_49
		MOV EAX, 1
		PUSH EAX
		MOV EAX, [EBP - 4]
		POP EBX
		SUB EAX, EBX
		MOV [EBP - 8], EAX
		MOV EAX, 1
		PUSH EAX
		MOV EAX, [EBP - 4]
		POP EBX
		ADD EAX, EBX
		MOV [EBP - 4], EAX
		JMP LOOP_49
	EXIT_49:
	MOV EAX, [EBP - 4]
	TEST EAX, EAX
	SETZ AL
	PUSH EAX
	PUSH formatout
	CALL printf
	ADD ESP, 8

    ; interruption to exit the program
    POP EBP
    MOV EAX, 1
    INT 0x80