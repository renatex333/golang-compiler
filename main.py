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
    code_gen = CodeGen(filename)
    code_gen.start()
    # root.evaluate(symbol_table, code_gen)
    code_gen.finish()

if __name__ == "__main__":
    main(sys.argv)

