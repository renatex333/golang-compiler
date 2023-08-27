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
        elif self.source[self.position] == " ":
            self.position += 1
            self.select_next()
        else:
            raise Exception("Invalid input")

class Parser:
    tokenizer = None
    @staticmethod
    def parse_expression():
        result = None
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == "INT":
            result = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            while (Parser.tokenizer.next.type == "PLUS") or (Parser.tokenizer.next.type == "MINUS"):
                if Parser.tokenizer.next.type == "PLUS":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "INT":
                        result += Parser.tokenizer.next.value
                    else:
                        raise Exception("Invalid input")
                elif Parser.tokenizer.next.type == "MINUS":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "INT":
                        result -= Parser.tokenizer.next.value
                    else:
                        raise Exception("Invalid input")
                else:
                    raise Exception("Invalid input")
                Parser.tokenizer.select_next()
            return result
        else:
            raise Exception("Invalid input")

    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code, 0, None)
        result = Parser.parse_expression()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception(f"Invalid input error: Last Token type is not EOF, is {Parser.tokenizer.next.type}")
        return result

def main(argv):
    result = Parser.run(argv[1])
    print(result)

if __name__ == "__main__":
    main(sys.argv)


