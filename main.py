import sys

from semantic_analysis import Parser
from syntactic_analysis import SymbolTable

def main(argv):
    root = Parser.run(argv[1])
    symbol_table = SymbolTable()
    root.evaluate(symbol_table)

if __name__ == "__main__":
    main(sys.argv)
