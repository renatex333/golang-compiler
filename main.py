import sys

from compiler.src.parser.Parser import Parser
from compiler.src.semantic_analysis.SymbolTable import SymbolTable

def main(argv):
    root = Parser.run(argv[1])
    symbol_table = SymbolTable()
    root.evaluate(symbol_table)

if __name__ == "__main__":
    main(sys.argv)

