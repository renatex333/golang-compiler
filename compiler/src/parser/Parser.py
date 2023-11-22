from compiler.src.preprocess.PreProcessing import PrePro
from compiler.src.lexer.Tokenizer import Tokenizer
from compiler.src.semantic_analysis.AbstractSyntaxTreeNodes import BinOp, UnOp, IntVal, StringVal, Identifier, Assignment, Print, Scan, If, For, Block, Program, VarDec, FuncDec, FuncCall, Return, NoOp


class Parser:
    tokenizer = None

    @staticmethod
    def run(filename):
        with open(f"{filename}", 'r') as file:
            lines = file.readlines()
            code = PrePro.filter(lines)
        Parser.tokenizer = Tokenizer(code, 0, None)
        Parser.tokenizer.select_next()
        root = Parser.parse_program()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception(
                f"Syntax Error: Last Token is not EOF, is {Parser.tokenizer.next.type}, with value of {Parser.tokenizer.next.value} instead.")
        return root


    @staticmethod
    def parse_program():
        children = []
        while Parser.tokenizer.next.type != "EOF":
            children.append(Parser.parse_declaration())
        children.append(FuncCall("main", []))
        root = Program("Program", children)
        return root


    @staticmethod
    def parse_declaration():
        root = None
        if Parser.tokenizer.next.type == "NEWLINE":
            Parser.tokenizer.select_next()
            root = NoOp("NoOp", [])
            return root
        if Parser.tokenizer.next.type != "FUNCTION":
            raise Exception(
                f"Syntax Error: Expected keyword 'func' before function declaration. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "IDENTIFIER":
            raise Exception(
                f"Syntax Error: Expected function identifier after keyword 'func'. Got '{Parser.tokenizer.next.value}' instead.")
        func_name = Parser.tokenizer.next.value
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "LEFTPARENTESIS":
            raise Exception(
                f"Syntax Error: Expected '(' after function identifier. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        children = []
        while Parser.tokenizer.next.type != "RIGHTPARENTESIS":
            if Parser.tokenizer.next.type != "IDENTIFIER":
                raise Exception(
                    f"Syntax Error: Expected identifier (function's argument) after '('. Got '{Parser.tokenizer.next.value}' instead.")
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "INT" and Parser.tokenizer.next.type != "STRING":
                raise Exception(
                    f"Syntax Error: Expected keyword 'int' or 'string' to determine identifier type. Got '{Parser.tokenizer.next.value}' instead.")
            var_type = Parser.tokenizer.next.type
            children.append(VarDec(var_type, [identifier]))
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "COMMA" and Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                raise Exception(
                    f"Syntax Error: Expected ')' or ',' after function's argument. Got '{Parser.tokenizer.next.value}' instead.")
            if Parser.tokenizer.next.type == "COMMA":
                Parser.tokenizer.select_next()
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "INT" and Parser.tokenizer.next.type != "STRING":
            raise Exception(
                f"Syntax Error: Expected keyword 'int' or 'string' to determine function return type. Got '{Parser.tokenizer.next.value}' instead.")
        func_type = Parser.tokenizer.next.type
        func_dec = VarDec(func_type, [Identifier(func_name, [])])
        children.insert(0, func_dec)
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "LEFTBRACE":
            raise Exception(
                f"Syntax Error: Expected '{{' after function signature. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "NEWLINE":
            raise Exception(
                f"Syntax Error: Expected newline ('\\n') after '{{'. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        while Parser.tokenizer.next.type != "RIGHTBRACE":
            children.append(Parser.parse_statement())
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "NEWLINE":
            raise Exception(
                f"Syntax Error: Expected newline ('\\n') after function declaration. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        root = FuncDec("FuncDec", children)
        return root


    @staticmethod
    def parse_block():
        if Parser.tokenizer.next.type != "LEFTBRACE":
            raise Exception(
                f"Syntax Error: Expected '{{' to determine block's beginning. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != "NEWLINE":
            raise Exception(
                f"Syntax Error: Expected newline ('\\n') after '{{'. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        children = []
        while Parser.tokenizer.next.type != "RIGHTBRACE":
            children.append(Parser.parse_statement())
        Parser.tokenizer.select_next()
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
            identifier_name = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "ASSIGNMENT" and Parser.tokenizer.next.type != "LEFTPARENTESIS":
                raise Exception(
                    f"Syntax Error: Expected '=' or '(' after identifier. Got '{Parser.tokenizer.next.value}' instead.")
            if Parser.tokenizer.next.type == "ASSIGNMENT":
                Parser.tokenizer.select_next()
                identifier = Identifier(identifier_name, [])
                root = Assignment(
                    "=", [identifier, Parser.parse_boolean_expression()])
            elif Parser.tokenizer.next.type == "LEFTPARENTESIS":
                Parser.tokenizer.select_next()
                children = []
                while Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                    children.append(Parser.parse_boolean_expression())
                    if Parser.tokenizer.next.type != "COMMA" and Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                        raise Exception(
                            f"Syntax Error: Expected ')' or ',' after function's argument. Got '{Parser.tokenizer.next.value}' instead.")
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                Parser.tokenizer.select_next()
                root = FuncCall(identifier_name, children)         
        elif Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "LEFTPARENTESIS":
                raise Exception(
                    f"Syntax Error: Expected '(' after 'Println' call. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            root = Print("Println", [Parser.parse_boolean_expression()])
            if Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                raise Exception(
                    f"Syntax Error: Expected ')' after expression. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.select_next()
            children = []
            condition = Parser.parse_boolean_expression()
            children.append(condition)
            block = Parser.parse_block()
            children.append(block)
            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.select_next()
                else_block = Parser.parse_block()
                children.append(else_block)
            root = If("If", children)
        elif Parser.tokenizer.next.type == "FOR":
            Parser.tokenizer.select_next()
            children = []
            if Parser.tokenizer.next.type != "IDENTIFIER":
                raise Exception(
                    f"Syntax Error: Expected identifier after keyword 'for'. Got '{Parser.tokenizer.next.value}' instead.")
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "ASSIGNMENT":
                raise Exception(
                    f"Syntax Error: Expected '=' in loop initialization. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            init = Assignment(
                "=", [identifier, Parser.parse_boolean_expression()])
            children.append(init)
            if Parser.tokenizer.next.type != "SEMICOLON":
                raise Exception(
                    f"Syntax Error: Expected ';' after initialization assignment. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            condition = Parser.parse_boolean_expression()
            children.append(condition)
            if Parser.tokenizer.next.type != "SEMICOLON":
                raise Exception(
                    f"Syntax Error: Expected ';' after loop condition. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "IDENTIFIER":
                raise Exception(
                    f"Syntax Error: Expected identifier after loop condition. Got '{Parser.tokenizer.next.value}' instead.")
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "ASSIGNMENT":
                raise Exception(
                    f"Syntax Error: Expected '=' after identifier in loop increment assignment. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            increment = Assignment(
                "=", [identifier, Parser.parse_boolean_expression()])
            children.append(increment)
            block = Parser.parse_block()
            children.append(block)
            root = For("For", children)
        elif Parser.tokenizer.next.type == "VAR":
            Parser.tokenizer.select_next()
            children = []
            if Parser.tokenizer.next.type != "IDENTIFIER":
                raise Exception(
                    f"Syntax Error: Expected identifier after keyword 'var'. Got '{Parser.tokenizer.next.value}' instead.")
            identifier = Identifier(Parser.tokenizer.next.value, [])
            children.append(identifier)
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "INT" and Parser.tokenizer.next.type != "STRING":
                raise Exception(
                    f"Syntax Error: Expected keyword 'int' or 'string' after identifier in variable declaration. Got '{Parser.tokenizer.next.value}' instead.")
            var_type = Parser.tokenizer.next.type
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "ASSIGNMENT":
                Parser.tokenizer.select_next()
                children.append(Parser.parse_boolean_expression())
            root = VarDec(var_type, children)
        elif Parser.tokenizer.next.type == "RETURN":
            Parser.tokenizer.select_next()
            root = Return("Return", [Parser.parse_boolean_expression()])
        if Parser.tokenizer.next.type != "NEWLINE":
            raise Exception(
                f"Invalid Statement: Expected newline ('\\n') after statement. Got '{Parser.tokenizer.next.value}' instead.")
        Parser.tokenizer.select_next()
        return root

    @staticmethod
    def parse_boolean_expression():
        root = Parser.parse_boolean_term()
        while Parser.tokenizer.next.type == "OR":
            Parser.tokenizer.select_next()
            root = BinOp("||", [root, Parser.parse_boolean_term()])
        return root

    @staticmethod
    def parse_boolean_term():
        root = Parser.parse_relational_expression()
        while Parser.tokenizer.next.type == "AND":
            Parser.tokenizer.select_next()
            root = BinOp("&&", [root, Parser.parse_relational_expression()])
        return root

    @staticmethod
    def parse_relational_expression():
        root = Parser.parse_expression()
        if Parser.tokenizer.next.type == "EQUALS":
            Parser.tokenizer.select_next()
            root = BinOp("==", [root, Parser.parse_expression()])
        elif Parser.tokenizer.next.type == "GREATER":
            Parser.tokenizer.select_next()
            root = BinOp(">", [root, Parser.parse_expression()])
        elif Parser.tokenizer.next.type == "LESS":
            Parser.tokenizer.select_next()
            root = BinOp("<", [root, Parser.parse_expression()])
        return root

    @staticmethod
    def parse_expression():
        root = Parser.parse_term()
        while (Parser.tokenizer.next.type == "PLUS") or (Parser.tokenizer.next.type == "MINUS") or (Parser.tokenizer.next.type == "CONCATENATION"):
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.select_next()
                root = BinOp("+", [root, Parser.parse_term()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.select_next()
                root = BinOp("-", [root, Parser.parse_term()])
            elif Parser.tokenizer.next.type == "CONCATENATION":
                Parser.tokenizer.select_next()
                root = BinOp(".", [root, Parser.parse_term()])
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
        elif Parser.tokenizer.next.type == "STRING":
            root = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            identifier_name = Parser.tokenizer.next.value
            root = Identifier(identifier_name, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "LEFTPARENTESIS":
                Parser.tokenizer.select_next()
                children = []
                while Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                    children.append(Parser.parse_boolean_expression())
                    if Parser.tokenizer.next.type != "COMMA" and Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                        raise Exception(
                            f"Syntax Error: Expected ')' or ',' after function's argument. Got '{Parser.tokenizer.next.value}' instead.")
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                Parser.tokenizer.select_next()
                root = FuncCall(identifier_name, children)
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.select_next()
            root = UnOp("+", [Parser.parse_factor()])
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.select_next()
            root = UnOp("-", [Parser.parse_factor()])
        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.select_next()
            root = UnOp("!", [Parser.parse_factor()])
        elif Parser.tokenizer.next.type == "LEFTPARENTESIS":
            Parser.tokenizer.select_next()
            root = Parser.parse_boolean_expression()
            if Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                raise Exception(
                    f"Syntax Error: Expected ')' after expression. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
        elif Parser.tokenizer.next.type == "SCAN":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "LEFTPARENTESIS":
                raise Exception(
                    f"Syntax Error: Expected '(' after keyword 'Scanln'. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != "RIGHTPARENTESIS":
                raise Exception(
                    f"Syntax Error: Expected ')' after expression. Got '{Parser.tokenizer.next.value}' instead.")
            Parser.tokenizer.select_next()
            root = Scan("Scan", [])
        else:
            raise Exception(
                f"Syntax Error: Expected an integer, identifier, function call, '+', '-', '!', '(' or 'Scanln'. Got '{Parser.tokenizer.next.value}' instead.")
        return root