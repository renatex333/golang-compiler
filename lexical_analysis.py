class Token:
    def __init__(self, type: str, value: int):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, source: str, position: int, next: Token):
        self.source = source
        self.position = position
        self.next = next

    def select_next(self):
        token_type = None
        token_value = None
        if self.position == len(self.source):
            token_type = "EOF"
            token_value = ""
            self.next = Token(token_type, token_value)
        elif self.source[self.position].isnumeric():
            token_type = "INT"
            number = str(self.source[self.position])
            self.position += 1
            while self.position < len(self.source) and self.source[self.position].isnumeric():
                number += str(self.source[self.position])
                self.position += 1
            token_value = int(number)
            self.next = Token(token_type, token_value)
        elif self.source[self.position].isalpha():
            token_type = "IDENTIFIER"
            token_value = str(self.source[self.position])
            self.position += 1
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isnumeric() or self.source[self.position] == "_"):
                token_value += str(self.source[self.position])
                self.position += 1
            if token_value == "Println":
                token_type = "PRINT"
            elif token_value == "Scanln":
                token_type = "SCAN"
            elif token_value == "if":
                token_type = "IF"
            elif token_value == "else":
                token_type = "ELSE"
            elif token_value == "for":
                token_type = "FOR"
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "+":
            token_type = "PLUS"
            token_value = "+"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "-":
            token_type = "MINUS"
            token_value = "-"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "*":
            token_type = "MULT"
            token_value = "*"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "/":
            token_type = "DIV"
            token_value = "/"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "(":
            token_type = "LEFTPARENTESIS"
            token_value = "("
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == ")":
            token_type = "RIGHTPARENTESIS"
            token_value = ")"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "\n":
            token_type = "NEWLINE"
            token_value = "\\n"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "=":
            token_type = "ASSIGNMENT"
            token_value = "="
            self.position += 1
            if self.source[self.position] == "=":
                token_type = "EQUALS"
                token_value = "=="
                self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "|" and self.source[self.position + 1] == "|":
            token_type = "OR"
            token_value = "||"
            self.position += 2
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "&" and self.source[self.position + 1] == "&":
            token_type = "AND"
            token_value = "&&"
            self.position += 2
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "!":
            token_type = "NOT"
            token_value = "!"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == ">":
            token_type = "GREATER"
            token_value = ">"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "<":
            token_type = "LESS"
            token_value = "<"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "{":
            token_type = "LEFTBRACE"
            token_value = "{"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == "}":
            token_type = "RIGHTBRACE"
            token_value = "}"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == ";":
            token_type = "SEMICOLON"
            token_value = ";"
            self.position += 1
            self.next = Token(token_type, token_value)
        elif self.source[self.position] == " ":
            self.position += 1
            self.select_next()
        else:
            raise Exception(f"Invalid Token Error: Token {repr(self.source[self.position])} is not a valid token. Located at position {self.position}.")