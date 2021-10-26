from owlready2 import *
import types
import ast

onto = get_ontology("http://test.org/onto.owl")  # create an owlready2 ontology


class AstVisitor(ast.NodeVisitor):
    """
        This class is a subclass of ast.NodeVisitor, with the purpose of adding
        custom visitor methods.
    """

    def visit_ClassDef(self, node: ast.ClassDef):
        for object in node.bases:  # for each ClassDef object:
            with onto:
                if (object.id == "Node"):
                    types.new_class(node.name, (Thing,))  # superclass Node of tree.py becomes Thing in the ontology
                else:
                    types.new_class(node.name, (
                        onto[object.id],))  # otherwise get the superclass from the ontology under construction(onto)

        for x in node.body:  # given an expression x in body
            with onto:
                if type(x) == ast.Assign:  # check if type(x) is ast.Assign
                    for element in x.value.elts:  # iterate over x.value.elts
                        if element.s == "parameters":
                            types.new_class(element.s, (ObjectProperty,))
                        elif element.s == "body":
                            types.new_class(element.s, (ObjectProperty,))
                        elif element.s == "name":
                            types.new_class("jname", (DataProperty,))
                        else:
                            types.new_class(element.s, (DataProperty,))
                        """
                                Use attribute s of each element to get a string representation of the elements
                                in the right hand side tuple of the assignment.
                                
                                Create a property for each of them:
                                    new_class("property", (ObjectProperty,)) for object properties
                                    new_class("property", (DataProperty,)) for datatype properties
                                    
                                Rename property "name" to "jname" to avoid conflicts with the predefined "name" attribute
                                
                                All properties are assumed to be data properties, except for "body" and "parameters",
                                which are ObjectProperties.
                        """


def main():
    pyfile = open("input/tree.py")  # get tree.py as input file

    try:
        ast_of_pyfile = ast.parse(pyfile.read())  # get the AST of input file
        AstVisitor().visit(ast_of_pyfile)  # visit the AST
        onto.save(file="tree.owl", format="rdfxml")  # save the ontology

    finally:
        pyfile.close()


def test_ontology():
    onto = get_ontology("tree.owl").load()
    cd = onto["ClassDeclaration"]
    assert cd.name == "ClassDeclaration"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == "TypeDeclaration"


if __name__ == "__main__":
    main()
    test_ontology()
