from owlready2 import *
import types
import ast


def main():
    pyfile = open("input/tree.py")  # get tree.py as input file

    try:
        ast_of_pyfile = ast.parse(pyfile.read())  # get the AST of input file
        print(ast_of_pyfile)
        # visit the AST
    finally:
        pyfile.close()


main()
