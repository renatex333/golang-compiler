# Projeto-Logica

![git status](http://3.129.230.99/svg/renatex333/Projeto-Logica/)

## Diagrama sintático

![diagrama sintatico](./diagrama-sintatico.png)

## EBNF

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
