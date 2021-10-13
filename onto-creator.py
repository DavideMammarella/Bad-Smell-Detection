from owlready2 import *
import types
import ast

onto = get_ontology("http://test.org/onto.owl")  # create an owlready2 ontology
onto_path.append("output")  # set output directory for the ontology


class AstVisitor(ast.NodeVisitor):
    """
        This class is a subclass of ast.NodeVisitor, with the purpose of adding
        custom visitor methods.
    """

    def visit_ClassDef(self, node: ast.ClassDef):

        with onto:
            for elem in node.bases:  # for each ClassDef object:
                # print("ClassDef object:", node.name, "| Superclass:", elem.id)
                if (elem.id == "Node"):
                    types.new_class(node.name, (Thing,))  # superclass Node of tree.py becomes Thing in the ontology
                else:
                    types.new_class(node.name, (onto[elem.id],))  # otherwise get the superclass from the ontology under construction(onto)


def main():
    pyfile = open("input/tree.py")  # get tree.py as input file

    try:
        ast_of_pyfile = ast.parse(pyfile.read())  # get the AST of input file
        AstVisitor().visit(ast_of_pyfile)  # visit the AST
        onto.save()  # save the ontology

    finally:
        pyfile.close()


if __name__ == "__main__":
    main()
