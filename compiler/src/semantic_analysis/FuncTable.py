class FuncTable:
    def __init__(self):
        self.table = dict()
    
    def get(self, identifier: str):
        try:
            return self.table[identifier]
        except KeyError:
            raise Exception(f"Identifier Error: Function '{identifier}' not declared.")
    
    def set(self, identifier: str, value: tuple):
        self.table[identifier] = value

    def create(self, identifier: str, var_type: str):
        if identifier in self.table.keys():
            raise Exception(f"Identifier Error: Function '{self.children[0].value}' already declared.")
        self.table[identifier] = (None, var_type)