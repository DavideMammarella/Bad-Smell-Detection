from owlready2 import *
import types
import ast

onto = get_ontology("http://test.org/onto.owl")  # create an owlready2 ontology


class AstVisitor(ast.NodeVisitor):
    """
    Subclass of ast.NodeVisitor, with the purpose of adding ClassDef visitor method.
    """

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Create a new class in the ontology for each ClassDef object:
        - superclass Node of tree.py becomes Thing in the ontology
        - otherwise get the superclass from the ontology under construction(onto)

        During the visit of each ClassDef create a new property in the ontology for each Assign in the body:
        - all properties are assumed to be data properties,
        - except for "body" and "parameters", which are ObjectProperties.
        Property "name" renamed to "jname" to avoid conflicts with the predefined "name" attribute.
        """
        with onto:
            for object in node.bases:
                if object.id == "Node":
                    types.new_class(node.name, (Thing,))
                else:
                    types.new_class(node.name, (onto[object.id],))
            for x in node.body:
                if isinstance(x, ast.Assign):
                    for element in x.value.elts:
                        if element.s == "parameters":
                            types.new_class(element.s, (ObjectProperty,))
                        elif element.s == "body":
                            types.new_class(element.s, (ObjectProperty,))
                        elif element.s == "name":
                            types.new_class("jname", (DataProperty,))
                        else:
                            types.new_class(element.s, (DataProperty,))


def main():
    """
    Create an ontology for Java entities:
    - Get tree.py as input file
    - Obtain AST from the input file
    - Visit the AST and save the ontology
    """
    with open("tree.py") as py_file:
        ast_of_py_file = ast.parse(py_file.read())
        AstVisitor().visit(ast_of_py_file)
        onto.save(file="tree.owl", format="rdfxml")


if __name__ == "__main__":
    main()
