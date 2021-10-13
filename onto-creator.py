from owlready2 import *
import types
import ast


class AstVisitor(ast.NodeVisitor, owl_ontology):
    """
        This class is a subclass of ast.NodeVisitor, with the purpose of adding
        custom visitor methods.
    """

    def visit(self, node):
        super().visit(node)

        # TODO: implement the visit of the AST
        # create a new class in the ontology for each ClassDef object:
        ## superclass Node of tree.py becomes Thing in the ontology: new_class("name", (Thing,));
        ## otherwise get the superclass from the ontology under construction(onto): new_class("name", (onto["superclassName"],)


def main():
    pyfile = open("input/tree.py")  # get tree.py as input file
    onto = get_ontology("http://test.org/onto.owl")  # create an owlready2 ontology
    onto_path.append("output")  # set output directory for the ontology

    try:
        ast_of_pyfile = ast.parse(pyfile.read())  # get the AST of input file
        AstVisitor().visit(ast_of_pyfile)  # visit the AST
        onto.save()  # save the ontology

    finally:
        pyfile.close()


main()
