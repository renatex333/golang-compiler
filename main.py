import sys

from pre_processing import PrePro
from lexical_analysis import Tokenizer
from syntactic_analysis import BinOp, UnOp, IntVal, NoOp

class Parser:
    tokenizer = None

    @staticmethod
    def run(filename):
        with open(f"{filename}", 'r') as file:
            lines = file.readlines()
            code = PrePro.filter(lines)
        Parser.tokenizer = Tokenizer(code, 0, None)
        Parser.tokenizer.select_next()
        root = Parser.parse_expression()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception(
                f"Invalid Input Error: Last Token type is not EOF, is {Parser.tokenizer.next.type} = {Parser.tokenizer.next.value}. Located at position {Parser.tokenizer.position}.")
        return root

    @staticmethod
    def parse_expression():
        root = None
        root = Parser.parse_term()
        while (Parser.tokenizer.next.type == "PLUS") or (Parser.tokenizer.next.type == "MINUS"):
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.select_next()
                root = BinOp("+", [root, Parser.parse_term()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.select_next()
                root = BinOp("-", [root, Parser.parse_term()])
        return root

    @staticmethod
    def parse_term():
        root = None
        root = Parser.parse_factor()
        while (Parser.tokenizer.next.type == "MULT") or (Parser.tokenizer.next.type == "DIV"):
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.select_next()
                root = BinOp("*", [root, Parser.parse_factor()])
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.select_next()
                root = BinOp("/", [root, Parser.parse_factor()])
        return root

    @staticmethod
    def parse_factor():
        root = None
        if Parser.tokenizer.next.type == "INT":
            root = IntVal(Parser.tokenizer.next.value, None)
            Parser.tokenizer.select_next()
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.select_next()
            root = UnOp("+", [Parser.parse_factor()])
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.select_next()
            root = UnOp("-", [Parser.parse_factor()])
        elif Parser.tokenizer.next.type == "LEFTPARENTESIS":
            Parser.tokenizer.select_next()
            root = Parser.parse_expression()
            if Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                raise Exception(
                    f"Invalid Input Error: Expected ')' after expression. Got '{Parser.tokenizer.next.value}' instead. Located at position {Parser.tokenizer.position}.")
            Parser.tokenizer.select_next()
        else:
            raise Exception(
                f"Invalid Input Error: Expected an integer, '+', '-', or '('. Got '{Parser.tokenizer.next.value}' instead. Located at position {Parser.tokenizer.position}.")
        return root


def main(argv):
    root = Parser.run(argv[1])
    print(root.evaluate())

if __name__ == "__main__":
    main(sys.argv)
