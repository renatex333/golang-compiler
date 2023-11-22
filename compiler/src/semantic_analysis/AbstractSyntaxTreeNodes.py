from __future__ import annotations
from abc import ABC, abstractmethod
from .Tables import SymbolTable, FunctionTable

class Node(ABC):
    def __init__(self, value: str, children: list[Node]):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        pass


class BinOp(Node):
    """
    value: operator \n
    children: [left node, right node], both returned from Parse Boolean Expression Call
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, function_table)
        child_1_value, child_1_type = self.children[1].evaluate(symbol_table, function_table)
        if child_0_type == "INT" and child_1_type == "INT":
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
            elif self.value == "&&":
                return (int(child_0_value and child_1_value), "INT")
            elif self.value == "==":
                return (int(child_0_value == child_1_value), "INT")
            elif self.value == ">":
                return (int(child_0_value > child_1_value), "INT")
            elif self.value == "<":
                return (int(child_0_value < child_1_value), "INT")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" and child_1_type == "STRING":
            if self.value == ".":
                return (str(child_0_value) + str(child_1_value), "STRING")
            elif self.value == "==":
                return (int(child_0_value == child_1_value), "INT")
            elif self.value == ">":
                return (int(child_0_value > child_1_value), "INT")
            elif self.value == "<":
                return (int(child_0_value < child_1_value), "INT")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")
        elif child_0_type == "STRING" or child_1_type == "STRING":
            if self.value == ".":
                return (str(child_0_value) + str(child_1_value), "STRING")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid operator between types {child_0_type} and {child_1_type}.")


class UnOp(Node):
    """
    value: operator \n
    children: [node], returned from Parse Boolean Expression Call
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, function_table)
        if child_0_type == "INT":
            if self.value == "+":
                return (child_0_value, "INT")
            elif self.value == "-":
                return (-child_0_value, "INT")
            elif self.value == "!":
                return (int(not child_0_value), "INT")
            else:
                raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")
        else:
            raise Exception(f"Invalid Operator Error: Operator {repr(self.value)} is not a valid unary operator fot type {child_0_type}.")


class IntVal(Node):
    """
    value: token value, must be int \n
    children: [empty]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        value = self.value
        return (int(value), "INT")


class StringVal(Node):
    """
    value: token value, must be string \n
    children: [empty]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        value = self.value
        return (str(value), "STRING")


class Identifier(Node):
    """
    value: token value, must be string \n
    children: [empty]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def __getitem__(self, key):
        return self.value

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        identifier = self.value
        return symbol_table.get(identifier)
    

class Assignment(Node):
    """
    value: assignment operator \n
    children: [identifier node, node returned from Parse Boolean Expression Call]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, function_table)
        child_1_value, child_1_type = self.children[1].evaluate(symbol_table, function_table)
        if child_0_type != child_1_type:
            raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {child_0_type}.")
        identifier = self.children[0].value
        symbol_table.set(identifier, (child_1_value, child_1_type))


class Print(Node):
    """
    value: print keyword \n
    children: [node returned from Parse Boolean Expression Call]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, function_table)
        print(child_0_value)


class Scan(Node):
    """
    value: scan keyword \n
    children: [empty]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        return (int(input()), "INT")


class If(Node):
    """
    value: if keyword \n
    children: [condition node, block, optional block] \n
    condition node: node returned from Parse Boolean Expression Call \n
    block: block node, returned from Parse Block Call \n
    optional block: block node, returned from Parse Block Call, in case there is an 'else' keyword
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        child_0_value, child_0_type = self.children[0].evaluate(symbol_table, function_table)
        if child_0_type != "INT":
            raise Exception(f"Invalid Type Error: Type {child_0_type} is not a valid type for an if statement.")
        if child_0_value:
            self.children[1].evaluate(symbol_table, function_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table, function_table)


class For(Node):
    """
    value: for keyword \n
    children: [initialization, condition, increment, block] \n
    initialization: assignment node \n
    condition: node returned from Parse Boolean Expression Call \n
    increment: assignment node \n
    block: node returned from Parse Block Call
    """

    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)
        self.initialization = self.children[0]
        self.condition = self.children[1]
        self.increment = self.children[2]
        self.body = self.children[3]

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        self.initialization.evaluate(symbol_table, function_table)
        while self.condition.evaluate(symbol_table, function_table)[0]:
            self.body.evaluate(symbol_table, function_table)
            self.increment.evaluate(symbol_table, function_table)


class Block(Node):
    """
    value: block keyword \n
    children: [N nodes, each returned from a Parse Statement Call]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        for child in self.children:
            child.evaluate(symbol_table, function_table)


class Program(Node):
    """
    value: program keyword \n
    children: [N nodes returned from Parse Declaration Call]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        for child in self.children:
            child.evaluate(symbol_table, function_table)


class VarDec(Node):
    """
    value: var type \n
    children: [identifier node, optional assignment node]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)
        self.identifier = self.children[0].value
        self.var_type = self.value
        
    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        symbol_table.create(self.identifier, self.var_type)
        if len(self.children) > 1:
            assignment = self.children[1]
            child_1_value, child_1_type = assignment.evaluate(symbol_table, function_table)
            if child_1_type != self.var_type:
                raise Exception(f"Invalid Type Error: Type {child_1_type} is not a valid type for a variable of type {self.var_type}.")
            symbol_table.set(self.identifier, (child_1_value, child_1_type))


class FuncDec(Node):
    """
    value: function keyword \n
    children: [N nodes] \n
    -> Children[0]: function name declaration, using VarDec \n
    -> Children[1:]: N optional function arguments (VarDec nodes), followed by N nodes returned from Parse Statement Call
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        func_dec = self.children[0]
        func_dec.evaluate(symbol_table, function_table)
        identifier = func_dec.children[0].value
        func_value, func_type = symbol_table.get(identifier)
        function_table.create(identifier, func_type)
        function_table.set(identifier, (self, func_type))


class FuncCall(Node):
    """
    value: function name \n
    children: [N nodes, each returned from Parse Boolean Expression Call], the arguments of the function call
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        func_name = self.value
        local_symbol_table = SymbolTable()
        func_node, func_type = function_table.get(func_name)
        args_n_statements = func_node.children[1:]
        arguments = list(zip(args_n_statements, self.children))
        num_args = len(arguments)
        for function_argument, passed_argument in arguments:
            function_argument.evaluate(local_symbol_table, function_table)
            passed_argument_value, passed_argument_type = passed_argument.evaluate(symbol_table, function_table)
            if function_argument.var_type != passed_argument_type:
                if function_argument.var_type == "STRING":
                    passed_argument_value = str(passed_argument_value)
                    passed_argument_type = "STRING"
                else:
                    raise Exception(f"Invalid Type Error: Type {passed_argument_type} is not a valid type for a variable of type {function_argument.var_type}.")
            local_symbol_table.set(function_argument.identifier, (passed_argument_value, passed_argument_type))
        for statement in args_n_statements[num_args:]:
            if statement.value == "Return":
                return_value, return_type = statement.evaluate(local_symbol_table, function_table)
                if return_type != func_type:
                    raise Exception(f"Invalid Type Error: Type {return_type} is not a valid return type for a function of type {func_type}.")
                return (return_value, return_type)
            statement.evaluate(local_symbol_table, function_table)
        

class Return(Node):
    """
    value: return keyword \n
    children: [node returned from Parse Boolean Expression Call]
    """
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        return self.children[0].evaluate(symbol_table, function_table)


class NoOp(Node):
    def __init__(self, value: str, children: list[Node]):
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable, function_table: FunctionTable):
        pass
