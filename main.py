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
        if self.source[self.position].isnumeric():
            token_type = "INTEGER"
            number = str(self.source[self.position])
            while self.source[self.position+1].isnumeric():
                number += str(self.source[self.position+1])
                self.position += 1
            token_value = int(self.source[self.position])
        elif self.source[self.position] == "+":
            token_type = "PLUS"
            token_value = self.source[self.position]
            self.position += 1
        elif self.source[self.position] == "-":
            token_type = "MINUS"
            token_value = self.source[self.position]
            self.position += 1
        elif self.source[self.position] == " ":
            self.position += 1
            self.select_next()
        elif self.position == len(self.source):
            token_type = "EOF"
            token_value = ""
        else:
            raise Exception("Invalid input")
        self.next = Token(token_type, token_value)

class Parser:
    tokenizer = None
    @staticmethod
    def parse_expression():
        result = None
        if Parser.tokenizer.next.type == "INTEGER":
            result = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS":
                if Parser.tokenizer.next.type == "PLUS":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "INTEGER":
                        result += Parser.tokenizer.next.value
                    else:
                        raise Exception("Invalid input")
                elif Parser.tokenizer.next.type == "MINUS":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "INTEGER":
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
            raise Exception("Invalid input")
        return result

def main(argv):
    result = Parser.run(argv[1])
    print(result)

if __name__ == "__main__":
    main(sys.argv)


