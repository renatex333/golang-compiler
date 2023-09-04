# Projeto-Logica

![git status](http://3.129.230.99/svg/renatex333/Projeto-Logica/)

## Diagrama sintático

![diagrama sintatico](./diagrama-sintatico.png)

## EBNF

```
EXPRESSION = TERM, {("+" | "-"), TERM} ;
TERM = NUMBER, {("*" | "/"), NUMBER} ;
NUMBER = DIGIT, {DIGIT} ;
DIGIT = 0 | 1 | ... | 9 ;
```
