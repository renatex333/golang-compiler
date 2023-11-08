# GoLang Compiler by Renato Laffranchi Falcão

Welcome to my GoLang compiler repository! This project was developed under the guidance of Professor Raul Ikeda during the "Lógica da Computação" course at Insper. It encapsulates intricate principles of the theory of computation and compiler design, presenting a comprehensive journey into the world of GoLang compiler creation.

## Sprint Tracker

![sprint tracker](http://3.129.230.99/svg/renatex333/Projeto-Logica/)

## Syntactic Diagram

![syntactic diagram](./img/syntactic-diagram.png)

## EBNF

### Grammar Definitions

```
# Grammatical Elements:
#
# * Strings with double quotes (") denote keywords.
# * Upper case names (NAME) denote tokens in the Grammar/Tokens file.
# * First character upper case names (Name) denote rule names.
#
# Grammar Syntax:
#
# Rule Name = expression
#   The rule is defined by the expression. 
# expression 1, expression 2
#   Match expression 1, then match expression 2.
# expression 1 | expression 2
#   Match expression 1 or expression 2.
# ( expression )
#   Match expression.
# [ expression ]
#   Optionally match expression.
# { expression }
#   Match zero or more occurrences of expression.
#
```

### Rule Definitions

```
PROGRAM = { DECLARATION } ;
DECLARATION = "func", IDENTIFIER, "(", { IDENTIFIER, ( "int" | "string" ), [ "," ] }, ")", ( "int" | "string" ), BLOCK, "\n" ;
BLOCK = "{", "\n", { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGN | PRINT | IF | FOR | VAR | RETURN ), "\n" ;
ASSIGN = IDENTIFIER, ( ( "=", BOOLEAN EXPRESSION ) | ( "(", { BOOLEAN EXPRESSION, [ "," ] }, ")" ) ) ;
PRINT = "Println", "(", BOOLEAN EXPRESSION, ")" ;
IF = "if", BOOLEAN EXPRESSION, BLOCK, { "else", BLOCK } ;
FOR = "for", ASSIGN, ";", BOOLEAN EXPRESSION, ";", ASSIGN, BLOCK ;
VAR = "var", IDENTIFIER, ( "int" | "string" ), ( λ | "=", BOOLEAN EXPRESSION ) ;
RETURN = "return", BOOLEAN EXPRESSION ;
BOOLEAN EXPRESSION = BOOLEAN TERM, { "||" BOOLEAN TERM } ;
BOOLEAN TERM = RELATIONAL EXPRESSION, { "&&", RELATIONAL EXPRESSION } ;
RELATIONAL EXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-" | "." ), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | STRING | IDENTIFIER ["(", { BOOLEAN EXPRESSION, [ "," ] }, ")" ] | (("+" | "-" | "!"), FACTOR) | "(", BOOLEAN EXPRESSION, ")" | SCAN ;
SCAN = "Scanln", "(", ")" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
STRING = ( `"` | `'` ), { λ | LETTER | DIGIT }, ( `"` | `'` ) ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```