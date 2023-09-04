import sys

class Token:
    def __init__(self, type:str, value:int):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source:str, position:int, next:Token):
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
        elif self.source[self.position] == " ":
            self.position += 1
            self.select_next()
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
        else:
            raise Exception(f"Invalid Token Error: Token {self.source[self.position]} is not a valid token. Located at position {self.position}.")

class Parser:
    tokenizer = None

    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code, 0, None)
        Parser.tokenizer.select_next()
        result = Parser.parse_expression()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception(f"Invalid Input Error: Last Token type is not EOF, is {Parser.tokenizer.next.type} = {Parser.tokenizer.next.value}. Located at position {Parser.tokenizer.position}.")
        return result

    @staticmethod
    def parse_expression():
        result = None
        result = Parser.parse_term()
        while (Parser.tokenizer.next.type == "PLUS") or (Parser.tokenizer.next.type == "MINUS"):
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.select_next()
                result += Parser.parse_term()
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.select_next()
                result -= Parser.parse_term()
        return result

    @staticmethod
    def parse_term():
        result = None
        result = Parser.parse_factor()
        while (Parser.tokenizer.next.type == "MULT") or (Parser.tokenizer.next.type == "DIV"):
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.select_next()
                result *= Parser.parse_factor()
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.select_next()
                result //= Parser.parse_factor()
        return result

    @staticmethod
    def parse_factor():
        result = None
        if Parser.tokenizer.next.type == "INT":
            result = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.select_next()
            result = Parser.parse_factor()
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.select_next()
            result = -Parser.parse_factor()
        elif Parser.tokenizer.next.type == "LEFTPARENTESIS":
            Parser.tokenizer.select_next()
            result = Parser.parse_expression()
            if Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                raise Exception(f"Invalid Input Error: Expected ')' after expression. Got '{Parser.tokenizer.next.value}' instead. Located at position {Parser.tokenizer.position}.")
            Parser.tokenizer.select_next()
        else:
            raise Exception(f"Invalid Input Error: Expected an integer, '+', '-', or '('. Got '{Parser.tokenizer.next.value}' instead. Located at position {Parser.tokenizer.position}.")
        return result
def main(argv):
    result = Parser.run(argv[1])
    print(result)

if __name__ == "__main__":
    main(sys.argv)