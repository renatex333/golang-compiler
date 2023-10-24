from __future__ import annotations
from abc import ABC, abstractmethod
from .SymbolTable import SymbolTable

class Node(ABC):
    def __init__(self, value: str, children: list[Node]):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self, symbol_table: SymbolTable):
        pass

class BinOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table)
        child_1_value, child_1_type = self.children[1].evaluate(symbol_table)
        if (child_0_type == "INT" or child_0_type == "BOOL") and (child_1_type == "INT" or child_1_type == "BOOL"):
            if self.value == "+":
                return (child_0_value + child_1_value, "INT")
            elif self.value == "-":
                return (child_0_value - child_1_value, "INT")
            elif self.value == ".":
                return (str(child_0_value) + str(child_1_value), "STRING")
            elif self.value == "*":
                return (child_0_value * child_1_value, "INT")
            elif self.value == "/":
                return (child_0_value // child_1_value, "INT")
            elif self.value == "||":
                return (int(child_0_value or child_1_value), "INT")
                # return (int(child_0_value or child_1_value), "BOOL")
            elif self.value == "&&":
                return (int(child_0_value and child_1_value), "INT")
                # return (int(child_0_value and child_1_value), "BOOL")
            elif self.value == "==":
                return (int(child_0_value == child_1_value), "INT")
                # return (int(child_0_value == child_1_value), "BOOL")
            elif self.value == ">":
                return (int(child_0_value > child_1_value), "INT")
                # return (int(child_0_value > child_1_value), "BOOL")
            elif self.value == "<":
                return (int(child_0_value < child_1_value), "INT")
                # return (int(child_0_value < child_1_value), "BOOL")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" and child_1_type == "STRING":
            if self.value == ".":
                return (str(child_0_value) + str(child_1_value), "STRING")
            elif self.value == "==":
                return (int(child_0_value == child_1_value), "INT")
                # return (int(child_0_value == child_1_value), "BOOL")
            elif self.value == ">":
                return (int(child_0_value > child_1_value), "INT")
                # return (int(child_0_value > child_1_value), "BOOL")
            elif self.value == "<":
                return (int(child_0_value < child_1_value), "INT")
                # return (int(child_0_value < child_1_value), "BOOL")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" or child_1_type == "STRING":
            if self.value == ".":
                return (str(child_0_value) + str(child_1_value), "STRING")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        

class UnOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table)
        if child_0_type == "INT" or child_0_type == "BOOL":
            if self.value == "+":
                return (child_0_value, "INT")
            elif self.value == "-":
                return (-child_0_value, "INT")
            elif self.value == "!":
                return (int(not child_0_value), "INT")
                # return (int(not child_0_value), "BOOL")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")
        else:
            raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")

class IntVal(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        return (int(self.value), "INT")
    
class StringVal(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        return (str(self.value), "STRING")
    
class Identifier(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        return symbol_table.get(self.value)
    
class Assignment(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table)
        child_1_value, child_1_type = self.children[1].evaluate(symbol_table)
        if child_0_type != child_1_type:
            raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {child_0_type}.")
        symbol_table.set(self.children[0].value, (child_1_value, child_1_type))

class Print(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        print(self.children[0].evaluate(symbol_table)[0])

class Scan(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        return (int(input()), "INT")

class If(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table)
        if child_0_type != "INT":
        # if child_0_type != "BOOL":
            raise Exception(f"Invalid Type Error: Type {child_0_type} is not a valid type for an if statement.")
        if child_0_value:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table)

class For(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table)[0]:
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)

class Block(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.evaluate(symbol_table)

class Program(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.evaluate(symbol_table)

class VarDec(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)
    
    def evaluate(self, symbol_table: SymbolTable):
        symbol_table.create(self.children[0].value, self.value)
        if len(self.children) > 1:
            child_1_value, child_1_type = self.children[1].evaluate(symbol_table)
            if child_1_type != self.value:
                raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {self.value}.")
            symbol_table.set(self.children[0].value, (child_1_value, child_1_type))            

class NoOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        pass