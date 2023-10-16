from __future__ import annotations
from abc import ABC, abstractmethod

class SymbolTable:
    def __init__(self):
        self.table = dict()
    
    def get(self, identifier: str):
        try:
            return self.table[identifier]
        except KeyError:
            raise Exception(f"Identifier Error: Identifier '{identifier}' not declared.")
    
    def set(self, identifier: str, value: tuple):
        self.table[identifier] = value

    def create(self, identifier: str):
        self.table[identifier] = None

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
        if self.value == "+":
            return self.children[0].evaluate(symbol_table) + self.children[1].evaluate(symbol_table)
        elif self.value == "-":
            return self.children[0].evaluate(symbol_table) - self.children[1].evaluate(symbol_table)
        elif self.value == "*":
            return self.children[0].evaluate(symbol_table) * self.children[1].evaluate(symbol_table)
        elif self.value == "/":
            return self.children[0].evaluate(symbol_table) // self.children[1].evaluate(symbol_table)
        elif self.value == "||":
            return self.children[0].evaluate(symbol_table) or self.children[1].evaluate(symbol_table)
        elif self.value == "&&":
            return self.children[0].evaluate(symbol_table) and self.children[1].evaluate(symbol_table)
        elif self.value == "==":
            return self.children[0].evaluate(symbol_table) == self.children[1].evaluate(symbol_table)
        elif self.value == ">":
            return self.children[0].evaluate(symbol_table) > self.children[1].evaluate(symbol_table)
        elif self.value == "<":
            return self.children[0].evaluate(symbol_table) < self.children[1].evaluate(symbol_table)
        elif self.value == ".":
            return str(self.children[0].evaluate(symbol_table)) + str(self.children[1].evaluate(symbol_table))

class UnOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        if self.value == "+":
            return self.children[0].evaluate(symbol_table)
        elif self.value == "-":
            return -self.children[0].evaluate(symbol_table)
        elif self.value == "!":
            return not self.children[0].evaluate(symbol_table)

class IntVal(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        return int(self.value)
    
class Identifier(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        return symbol_table.get(self.value)
    
class Assignment(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        symbol_table.set(self.children[0].value, self.children[1].evaluate(symbol_table))

class Print(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        print(self.children[0].evaluate(symbol_table))

class Scan(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        return int(input())

class If(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table)

class For(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table):
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
        if len(self.children) > 1:
            symbol_table.set(self.children[0].evaluate(symbol_table), self.children[1].evaluate(symbol_table))
        else:
            symbol_table.create(self.children[0].evaluate(symbol_table))

class NoOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        pass