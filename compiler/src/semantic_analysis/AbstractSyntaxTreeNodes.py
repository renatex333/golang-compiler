from __future__ import annotations
from abc import ABC, abstractmethod
from .SymbolTable import SymbolTable
from compiler.src.codegen.CodeGenerator import CodeGen

class Node(ABC):
    index = 0

    def __init__(self, value: str, children: list[Node]):
        self.value = value
        self.children = children
        self.index = Node.new_index()

    @abstractmethod
    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        pass

    @staticmethod
    def new_index():
        Node.index += 1
        return Node.index

class BinOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        child_1_type = self.children[1].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"PUSH EAX")
        child_0_type = self.children[0].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"POP EBX")
        if child_0_type == "INT" and child_1_type == "INT":
            if self.value == "+":
                code_generator.write_line(f"ADD EAX, EBX")
                return "INT"
            elif self.value == "-":
                code_generator.write_line(f"SUB EAX, EBX")
                return "INT"
            elif self.value == ".":
                code_generator.write_line(f"; CONCATENATE STRINGS NOT IMPLEMENTED YET")
                return "STRING"
            elif self.value == "*":
                code_generator.write_line(f"MUL EBX")
                return "INT"
            elif self.value == "/":
                code_generator.write_line(f"DIV EBX")
                return "INT"
            elif self.value == "||":
                code_generator.write_line(f"OR EAX, EBX")
                return "INT"
            elif self.value == "&&":
                code_generator.write_line(f"AND EAX, EBX")
                return "INT"
            elif self.value == "==":
                code_generator.write_line(f"CMP EAX, EBX")
                code_generator.write_line(f"CALL binop_je")
                return "INT"
            elif self.value == ">":
                code_generator.write_line(f"CMP EAX, EBX")
                code_generator.write_line(f"CALL binop_jg")
                return "INT"
            elif self.value == "<":
                code_generator.write_line(f"CMP EAX, EBX")
                code_generator.write_line(f"CALL binop_jl")
                return "INT"
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" and child_1_type == "STRING":
            if self.value == ".":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return "STRING"
            elif self.value == "==":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return "INT"
            elif self.value == ">":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return "INT"
            elif self.value == "<":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return "INT"
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" or child_1_type == "STRING":
            if self.value == ".":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return "STRING"
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        

class UnOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        child_0_type = self.children[0].evaluate(symbol_table, code_generator)
        if child_0_type == "INT":
            if self.value == "+":
                pass
            elif self.value == "-":
                code_generator.write_line(f"NEG EAX")
            elif self.value == "!":
                code_generator.write_line(f"TEST EAX, EAX")
                code_generator.write_line(f"SETZ AL")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")
            return "INT"
        else:
            raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")

class IntVal(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"MOV EAX, {int(self.value)}")
        return "INT"
    
class StringVal(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
        return "STRING"
    
class Identifier(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        identifier_type, identifier_stack_location = symbol_table.get(self.value)
        code_generator.write_line(f"MOV EAX, [EBP - {identifier_stack_location}]")
        return identifier_type
    
class Assignment(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        child_1_type = self.children[1].evaluate(symbol_table, code_generator)
        identifier_type, identifier_stack_location = symbol_table.get(self.children[0].value)
        if identifier_type != child_1_type:
            raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {identifier_type}.")
        symbol_table.set(self.children[0].value, (child_1_type, identifier_stack_location))
        code_generator.write_line(f"MOV [EBP - {identifier_stack_location}], EAX")

class Print(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        self.children[0].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"PUSH EAX")
        code_generator.write_line(f"PUSH formatout")
        code_generator.write_line(f"CALL printf")
        code_generator.write_line(f"ADD ESP, 8")

class Scan(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"PUSH scanint")
        code_generator.write_line(f"PUSH formatin")
        code_generator.write_line(f"CALL scanf")
        code_generator.write_line(f"ADD ESP, 8")
        code_generator.write_line(f"MOV EAX, DWORD [scanint]")
        return "INT"

class If(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        child_0_type = self.children[0].evaluate(symbol_table, code_generator)
        if child_0_type != "INT":
            raise Exception(f"Invalid Type Error: Type {child_0_type} is not a valid type for an if statement.")
        code_generator.write_line(f"CMP EAX, False")
        code_generator.write_line(f"JE EXIT_{self.index}")
        self.children[1].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"EXIT_{self.index}:")
        if len(self.children) > 2:
            self.children[2].evaluate(symbol_table, code_generator)

class For(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        self.children[0].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"LOOP_{self.index}:")
        code_generator.indent_up()
        self.children[1].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"CMP EAX, False")
        code_generator.write_line(f"JE EXIT_{self.index}")
        self.children[3].evaluate(symbol_table, code_generator)
        self.children[2].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"JMP LOOP_{self.index}")
        code_generator.indent_down()
        code_generator.write_line(f"EXIT_{self.index}:")

class Block(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        for child in self.children:
            child.evaluate(symbol_table, code_generator)

class Program(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        for child in self.children:
            child.evaluate(symbol_table, code_generator)

class VarDec(Node):
    def __init__(self, var_type: str, children: list[Node]):
        super().__init__(value=var_type, children=children)
    
    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        symbol_table.create(self.children[0].value, self.value)
        code_generator.write_line(f"PUSH DWORD 0")
        if len(self.children) > 1:
            child_1_type = self.children[1].evaluate(symbol_table, code_generator)
            if child_1_type != self.var_type:
                raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {self.value}.")
            identifier_type, identifier_stack_location = symbol_table.get(self.children[0].value)
            symbol_table.set(identifier=self.children[0].value, value=(child_1_type, identifier_stack_location))
            code_generator.write_line(f"MOV [EBP - {identifier_stack_location}], EAX")

class NoOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"NOP")