import sys

from compiler.src.parser.Parser import Parser
from compiler.src.semantic_analysis.SymbolTable import SymbolTable
from compiler.src.codegen.CodeGenerator import CodeGen

def main(argv):
    root = Parser.run(filename=argv[1])
    symbol_table = SymbolTable()
    code_generator = CodeGen(filename=argv[1])
    code_generator.start()
    root.evaluate(symbol_table, code_generator)
    code_generator.finish()

if __name__ == "__main__":
    main(sys.argv)

