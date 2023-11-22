from abc import ABC, abstractmethod

class Table(ABC):
    def __init__(self):
        self.table = dict()

    @abstractmethod
    def get(self, identifier: str):
        pass

    @abstractmethod
    def set(self, identifier: str, value: tuple):
        pass

    @abstractmethod
    def create(self, identifier: str, var_type: str):
        pass

class SymbolTable(Table):
    def __init__(self):
        super().__init__()
    
    def get(self, identifier: str):
        """
        Returns the value of the identifier in the symbol table. \n
        Args: \n
            identifier (str): The identifier to retrieve the value of. \n
        Returns: \n
            (tuple -> (Value, Type)): The value of the identifier, The type of the identifier.
        """
        try:
            return self.table[identifier]
        except KeyError:
            raise Exception(f"Identifier Error: Identifier '{identifier}' not declared.")
    
    def set(self, identifier: str, value: tuple):
        """
        Sets the value of the identifier in the symbol table. \n
        Args: \n
            identifier (str): The identifier to set the value of. \n
            value (tuple -> (Value, Type)): The value to set the identifier, the type of the identifier. \n
        Returns: \n
            None
        """
        if identifier not in self.table.keys():
            raise Exception(f"Identifier Error: Identifier '{identifier}' not declared.")
        self.table[identifier] = value

    def create(self, identifier: str, var_type: str):
        """
        Creates a new identifier in the symbol table. \n
        Args: \n
            identifier (str): The identifier to create. \n
            var_type (str): The type of the identifier to create. \n
        Returns: \n
            None
        """
        if identifier in self.table.keys():
            raise Exception(f"Identifier Error: Identifier '{identifier}' already declared.")
        self.table[identifier] = (None, var_type)

class FunctionTable(Table):
    def __init__(self):
        super().__init__()
    
    def get(self, identifier: str):
        """
        Returns the value of the identifier in the function table. \n
        Args: \n
            identifier (str): The function's identifier to retrieve the value of. \n
        Returns: \n
            (tuple -> (Node, Type): The function declaration Node, the function's type of return.
        """
        try:
            return self.table[identifier]
        except KeyError:
            raise Exception(f"Identifier Error: Function '{identifier}' not declared.")
    
    def set(self, identifier: str, value: tuple):
        """
        Sets the value of the identifier in the function table. \n
        Args: \n
            identifier (str): The function's identifier to set the value of. \n
            value (tuple -> (Node, Type)): The function declaration Node, the function's type of return. \n
        Returns: \n
            None
        """
        if identifier not in self.table.keys():
            raise Exception(f"Identifier Error: Function '{identifier}' not declared.")
        self.table[identifier] = value

    def create(self, identifier: str, var_type: str):
        """
        Creates a new identifier in the function table. \n
        Args: \n
            identifier (str): The function's identifier to create. \n
            var_type (str): The function's type of return. \n
        Returns: \n
            None
        """
        if identifier in self.table.keys():
            raise Exception(f"Identifier Error: Function '{identifier}' already declared.")
        self.table[identifier] = (None, var_type)