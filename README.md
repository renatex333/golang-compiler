# GoLang Compiler by Renato Laffranchi Falcão

Welcome to the GoLang compiler repository by Renato Laffranchi Falcão! This innovative project, crafted under the expert guidance of Professor Raul Ikeda during the "Lógica da Computação" course at Insper, delves deep into the complexities of computation theory and compiler construction. It offers an immersive exploration into the creation of a GoLang compiler, blending theoretical knowledge with practical application.

## Project Overview

This GoLang compiler serves as a testament to the progression in understanding compiler mechanisms and programming language design. It translates GoLang code into executable machine language, highlighting the intricacies involved in such a process.

## Versioning and Releases

- **Version 2.4 (Function Implementation)**: Introduced the capability to define and invoke functions within the GoLang code, significantly enhancing the compiler's versatility and aligning with modern programming paradigms.
- **Version 3.0 (Assembly Code Generation)**: Marked a milestone by generating assembly code, a critical step towards lower-level programming and optimization. This version leverages the NASM assembler to convert high-level constructs into machine-level instructions, showcasing a leap in compiler functionality.

## Sprint Tracker

Monitor our development progress in real-time with our sprint tracker:

![sprint tracker](http://3.129.230.99/svg/renatex333/Projeto-Logica/)

## Syntactic Diagram

Explore the syntactic structure of the language through our detailed diagram:

![syntactic diagram](./img/syntactic-diagram.png)

## Extended Backus-Naur Form (EBNF)

The EBNF defines the grammar of our GoLang compiler, outlining the syntax rules:

```
PROGRAM = { STATEMENT } ;
BLOCK = "{", "\n", { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGN | PRINT | IF | FOR | VAR), "\n" ;
ASSIGN = IDENTIFIER, "=", BOOLEAN EXPRESSION ;
PRINT = "Println", "(", BOOLEAN EXPRESSION, ")" ;
IF = "if", BOOLEAN EXPRESSION, BLOCK, { "else", BLOCK } ;
FOR = "for", ASSIGN, ";", BOOLEAN EXPRESSION, ";", ASSIGN, BLOCK ;
VAR = "var", IDENTIFIER, ( "int" | "string" ), ( λ | "=", BOOLEAN EXPRESSION ) ;
BOOLEAN EXPRESSION = BOOLEAN TERM, { "||" BOOLEAN TERM } ;
BOOLEAN TERM = RELATIONAL EXPRESSION, { "&&", RELATIONAL EXPRESSION } ;
RELATIONAL EXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-" | "." ), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | STRING | IDENTIFIER | (("+" | "-" | "!"), FACTOR) | "(", BOOLEAN EXPRESSION, ")" | SCAN ;
SCAN = "Scanln", "(", ")" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
STRING = ( `"` | `'` ), { λ | LETTER | DIGIT }, ( `"` | `'` ) ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```

## Debugging with GDB

### Compiling in Debug Mode

To compile in debug mode, follow these steps:

```
python3 main.py file.go
nasm -f elf -F dwarf -o program.o program.asm
gcc -m32 -no-pie -g -o program program.o
```

### GDB Commands

Utilize these GDB commands for efficient debugging:

```
gdb ./program
(gdb) b line_number -> sets a breakpoint @ line number
(gdb) run -> run complete program, unless there is a breakpoint
(gdb) step or stepi -> run line by line of code 
```

## References

IME-USP. (1999). [The Netwide Assembler: NASM](https://www.ime.usp.br/~reverbel/mac211-99/asm/nasm_doc/nasmdoca.html).
