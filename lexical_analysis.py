TOKENS = {
            "+": "PLUS", 
            "-": "MINUS",
            ".": "CONCATENATION",
            "*": "MULT", 
            "/": "DIV", 
            "(": "LEFTPARENTESIS", 
            ")": "RIGHTPARENTESIS", 
            "\n": "NEWLINE",
            "=": "ASSIGNMENT",
            "!": "NOT", 
            ">": "GREATER", 
            "<": "LESS", 
            "==": "EQUALS",
            "||": "OR",
            "&&": "AND",
            "{": "LEFTBRACE", 
            "}": "RIGHTBRACE", 
            ";": "SEMICOLON",
            "Println": "PRINT",
            "Scanln": "SCAN",
            "if": "IF",
            "else": "ELSE",
            "for": "FOR"
          }

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
            token_value = ""
            token_type = "EOF"
        elif self.source[self.position].isnumeric():
            number = str(self.source[self.position])
            self.position += 1
            while self.position < len(self.source) and self.source[self.position].isnumeric():
                number += str(self.source[self.position])
                self.position += 1
            token_value = int(number)
            token_type = "INT"
        elif self.source[self.position].isalpha():
            token_value = str(self.source[self.position])
            self.position += 1
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isnumeric() or self.source[self.position] == "_"):
                token_value += str(self.source[self.position])
                self.position += 1
            try:
                token_type = TOKENS[token_value]
            except KeyError:
                token_type = "IDENTIFIER"
        elif self.source[self.position] == '"' or self.source[self.position] == "'":
            quotation_mark = self.source[self.position]
            token_value = quotation_mark
            self.position += 1
            while self.position < len(self.source) and self.source[self.position] != quotation_mark:
                token_value += str(self.source[self.position])
                self.position += 1
            token_value += quotation_mark
            self.position += 1
            token_type = "STRING"
        elif self.source[self.position] == " ":
            self.position += 1
            self.select_next()
            return
        else:
            try:
                token_type = TOKENS[self.source[self.position] + self.source[self.position + 1]]
                token_value = self.source[self.position] + self.source[self.position + 1]
                self.position += 2
            except (KeyError, IndexError):
                try:
                    token_type = TOKENS[self.source[self.position]]
                    token_value = self.source[self.position]
                    self.position += 1
                except KeyError:
                    raise Exception(f"Invalid Token Error: Token {repr(self.source[self.position])} is not a valid token. Located at position {self.position}. ")
        self.next = Token(token_type, token_value)  