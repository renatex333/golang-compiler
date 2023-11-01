class CodeGen():
    def __init__(self, filename: str):
        self.filename = filename.replace(".go", ".asm")
        self.asm_header =   """
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
extern fflush
extern stdout

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
"""

        self.asm_footer =   """
    ; interruption to exit the program
    PUSH DWORD [stdout]
    CALL fflush
    ADD ESP, 4
    MOV ESP, EBP
    POP EBP
    MOV EAX, 1
    XOR EBX, EBX
    INT 0x80
"""
        self.indent = 1

    def start(self):
        with open(self.filename, "w") as file:
            file.write(self.asm_header)
    
    def write_line(self, line: str):
        with open(self.filename, "a") as file:
            file.write(self.indent*"\t" + line + "\n")

    def finish(self):
        with open(self.filename, "a") as file:
            file.write(self.asm_footer)

    def indent_up(self):
        self.indent += 1
    
    def indent_down(self):
        self.indent -= 1