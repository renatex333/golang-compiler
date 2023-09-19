from pre_processing import PrePro
from lexical_analysis import Tokenizer
from syntactic_analysis import BinOp, UnOp, IntVal, Identifier, Assignment, Print, Block, NoOp

class Parser:
    tokenizer = None

    @staticmethod
    def run(filename):
        with open(f"{filename}", 'r') as file:
            lines = file.readlines()
            code = PrePro.filter(lines)
        Parser.tokenizer = Tokenizer(code, 0, None)
        Parser.tokenizer.select_next()
        root = Parser.parse_block()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception(f"Invalid Input Error: Last Token type is not EOF, is {Parser.tokenizer.next.type} = {Parser.tokenizer.next.value}.")
        return root
    
    @staticmethod
    def parse_block():
        children = []
        while Parser.tokenizer.next.type != "EOF":
            children.append(Parser.parse_statement())
        root = Block("Block", children)
        return root
    
    @staticmethod
    def parse_statement():
        root = None
        if Parser.tokenizer.next.type == "NEWLINE":
            Parser.tokenizer.select_next()
            root = NoOp("NoOp", [])
            return root
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "ASSIGNMENT":
                raise Exception(f"Invalid Input Error: Expected '=' after identifier. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            root = Assignment("=", [identifier, Parser.parse_expression()])
        elif Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "LEFTPARENTESIS":
                raise Exception(f"Invalid Input Error: Expected '(' after 'Println'. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            root = Print("Println", [Parser.parse_expression()])
            if Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                raise Exception(f"Invalid Input Error: Expected ')' after expression. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "NEWLINE":
            raise Exception(f"Invalid Statement: Expected newline ('\\n') after statement. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        return root

    @staticmethod
    def parse_expression():
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
            root = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            root = Identifier(Parser.tokenizer.next.value, [])
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
                raise Exception(f"Invalid Input Error: Expected ')' after expression. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
        else:
            raise Exception(f"Invalid Input Error: Expected an integer, identifier, '+', '-', or '('. Got '{Parser.tokenizer.next.value}' instead.")
        return root