import sys

from compiler.src.parser.Parser import Parser
from compiler.src.semantic_analysis.Tables import SymbolTable, FunctionTable

def main(argv):
    root = Parser.run(filename=argv[1])
    symbol_table = SymbolTable()
    function_table = FunctionTable()
    root.evaluate(symbol_table, function_table)

if __name__ == "__main__":
    main(sys.argv)
