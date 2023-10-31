import sys

from compiler.src.parser.Parser import Parser
from compiler.src.semantic_analysis.SymbolTable import SymbolTable
from compiler.src.codegen.CodeGenerator import CodeGen

def main(argv):
    root = Parser.run(argv[1])
    symbol_table = SymbolTable()
    filename = "program.asm"
    if len(argv) > 2:
        filename = argv[2]
    code_generator = CodeGen(filename)
    code_generator.start()
    root.evaluate(symbol_table, code_generator)
    code_generator.finish()

if __name__ == "__main__":
    main(sys.argv)

