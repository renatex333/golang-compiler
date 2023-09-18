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
    
    def set(self, identifier: str, value: int):
        self.table[identifier] = value

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
        if self.value == "+":
            return self.children[0].evaluate(symbol_table) + self.children[1].evaluate(symbol_table)
        elif self.value == "-":
            return self.children[0].evaluate(symbol_table) - self.children[1].evaluate(symbol_table)
        elif self.value == "*":
            return self.children[0].evaluate(symbol_table) * self.children[1].evaluate(symbol_table)
        elif self.value == "/":
            return self.children[0].evaluate(symbol_table) // self.children[1].evaluate(symbol_table)

class UnOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        if self.value == "+":
            return self.children[0].evaluate(symbol_table)
        elif self.value == "-":
            return -self.children[0].evaluate(symbol_table)

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

class Block(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.evaluate(symbol_table)

class NoOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        pass