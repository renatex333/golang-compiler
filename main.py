import sys

from Parser import Parser
from AbstractSyntaxTreeNodes import SymbolTable

def main(argv):
    root = Parser.run(argv[1])
    symbol_table = SymbolTable()
    root.evaluate(symbol_table)

if __name__ == "__main__":
    main(sys.argv)

