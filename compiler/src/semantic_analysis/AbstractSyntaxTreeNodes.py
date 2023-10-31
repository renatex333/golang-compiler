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
        child_1_value, child_1_type = self.children[1].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"PUSH EAX")
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"POP EBX")
        if child_0_type == "INT" and child_1_type == "INT":
            if self.value == "+":
                code_generator.write_line(f"ADD EAX, EBX")
                return (child_0_value + child_1_value, "INT")
            elif self.value == "-":
                code_generator.write_line(f"SUB EAX, EBX")
                return (child_0_value - child_1_value, "INT")
            elif self.value == ".":
                code_generator.write_line(f"; CONCATENATE STRINGS NOT IMPLEMENTED YET")
                return (str(child_0_value) + str(child_1_value), "STRING")
            elif self.value == "*":
                code_generator.write_line(f"MUL EBX")
                return (child_0_value * child_1_value, "INT")
            elif self.value == "/":
                code_generator.write_line(f"DIV EBX")
                return (child_0_value // child_1_value, "INT")
            elif self.value == "||":
                code_generator.write_line(f"OR EAX, EBX")
                return (int(child_0_value or child_1_value), "INT")
            elif self.value == "&&":
                code_generator.write_line(f"AND EAX, EBX")
                return (int(child_0_value and child_1_value), "INT")
            elif self.value == "==":
                code_generator.write_line(f"CMP EAX, EBX")
                code_generator.write_line(f"JMP binop_je")
                return (int(child_0_value == child_1_value), "INT")
            elif self.value == ">":
                code_generator.write_line(f"CMP EAX, EBX")
                code_generator.write_line(f"JMP binop_jg")
                return (int(child_0_value > child_1_value), "INT")
            elif self.value == "<":
                code_generator.write_line(f"CMP EAX, EBX")
                code_generator.write_line(f"JMP binop_jl")
                return (int(child_0_value < child_1_value), "INT")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" and child_1_type == "STRING":
            if self.value == ".":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return (str(child_0_value) + str(child_1_value), "STRING")
            elif self.value == "==":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return (int(child_0_value == child_1_value), "INT")
            elif self.value == ">":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return (int(child_0_value > child_1_value), "INT")
            elif self.value == "<":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return (int(child_0_value < child_1_value), "INT")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" or child_1_type == "STRING":
            if self.value == ".":
                code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
                return (str(child_0_value) + str(child_1_value), "STRING")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        

class UnOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, code_generator)
        if child_0_type == "INT":
            if self.value == "+":
                return (child_0_value, "INT")
            elif self.value == "-":
                code_generator.write_line(f"NEG EAX")
                return (-child_0_value, "INT")
            elif self.value == "!":
                code_generator.write_line(f"NOT EAX")
                return (int(not child_0_value), "INT")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")
        else:
            raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")

class IntVal(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"MOV EAX, {int(self.value)}")
        return (int(self.value), "INT")
    
class StringVal(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"; STRING OPERATIONS NOT IMPLEMENTED YET")
        return (str(self.value), "STRING")
    
class Identifier(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        identifier_value, identifier_type, identifier_stack_location = symbol_table.get(self.value)
        code_generator.write_line(f"MOV EAX, [EBP - {identifier_stack_location}]")
        return identifier_value, identifier_type
    
class Assignment(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        child_1_value, child_1_type = self.children[1].evaluate(symbol_table, code_generator)
        identifier_value, identifier_type, identifier_stack_location = symbol_table.get(self.children[0].value)
        if identifier_type != child_1_type:
            raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {identifier_type}.")
        symbol_table.set(self.children[0].value, (child_1_value, child_1_type, identifier_stack_location))
        code_generator.write_line(f"MOV [EBP - {identifier_stack_location}], EAX")

class Print(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"PUSH EAX")
        code_generator.write_line(f"PUSH formatout")
        code_generator.write_line(f"CALL printf")
        code_generator.write_line(f"ADD ESP, 8")
        print(self.children[0].evaluate(symbol_table, code_generator)[0])

class Scan(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"PUSH scanint")
        code_generator.write_line(f"PUSH formatin")
        code_generator.write_line(f"CALL scanf")
        code_generator.write_line(f"ADD ESP, 8")
        code_generator.write_line(f"MOV EAX, DWORD [scanint]")
        return (int(input()), "INT")

class If(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, code_generator)
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
        child_1_value, child_1_type = self.children[1].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"CMP EAX, False")
        code_generator.write_line(f"JE EXIT_{self.index}")
        self.children[3].evaluate(symbol_table, code_generator)
        self.children[2].evaluate(symbol_table, code_generator)
        code_generator.write_line(f"JMP LOOP_{self.index}")
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
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)
    
    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        symbol_table.create(self.children[0].value, self.value)
        code_generator.write_line(f"PUSH DWORD 0")
        if len(self.children) > 1:
            child_1_value, child_1_type = self.children[1].evaluate(symbol_table, code_generator)
            if child_1_type != self.value:
                raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {self.value}.")
            identifier_value, identifier_type, identifier_stack_location = symbol_table.get(self.children[0].value)
            symbol_table.set(self.children[0].value, (child_1_value, child_1_type, identifier_stack_location))

class NoOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, code_generator: CodeGen):
        code_generator.write_line(f"NOP")
        pass