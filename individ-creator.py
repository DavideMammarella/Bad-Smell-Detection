from owlready2 import *
import ast
import os
from os.path import isfile
import javalang


def createDeclaration(body_cd, class_declaration, body_declaration):
    """
    Append the member instance to the property "body" of the ClassDeclaration instance.
    """
    body_declaration.jname = [body_cd.name]
    class_declaration.body.append(body_declaration)


def createStatementsAndParameters(onto, body_cd, declaration):
    """
    For each Statement (IfStatement, WhileStatement, etc.) reachable from the body of a
    MethodDeclaration or ConstructorDeclaration, create a Statement instance  and add (append)
    the Statement instances to the property "body" of the MethodDeclaration or ConstructorDeclaration.

    For each parameter in the parameter list of a MethodDeclaration or ConstructorDeclaration,
    create an instance of class FormalParameter and add (append) the FormalParameter instances
    to the property "parameters" of the MethodDeclaration or ConstructorDeclaration.
    """
    for _, statement in body_cd:
        if isinstance(statement, javalang.tree.Statement):
            statement_name = type(statement).__name__
            statement_instance = onto[statement_name]()
            declaration.body.append(statement_instance)
    for parameter in body_cd.parameters:
        parameter_name = type(parameter).__name__
        parameter_instance = onto[parameter_name]()
        declaration.parameters.append(parameter_instance)


def populateOntology(onto, tree):
    """
    For each ClassDeclaration create an instance of the ontology class (ClassDeclaration).
    For each class member (MethodDeclaration/FieldDeclaration/ConstructorDeclaration) in the "body"
    of a ClassDeclaration create an instance of the ontology class member.
    """
    for _, node in tree.filter(javalang.tree.ClassDeclaration):
        cd = onto["ClassDeclaration"]()
        cd.jname = [node.name]
        for body_cd in node.body:
            if isinstance(body_cd, javalang.tree.MethodDeclaration):
                md = onto["MethodDeclaration"]()
                createDeclaration(body_cd, cd, md)
                createStatementsAndParameters(onto, body_cd, md)
            elif isinstance(body_cd, javalang.tree.ConstructorDeclaration):
                cdec = onto["ConstructorDeclaration"]()
                createDeclaration(body_cd, cd, cdec)
                createStatementsAndParameters(onto, body_cd, cdec)
            elif isinstance(body_cd, javalang.tree.FieldDeclaration):
                for field in body_cd.declarators:
                    fd = onto["FieldDeclaration"]()
                    createDeclaration(field, cd, fd)


def main():
    """
    Populate an ontology with instances:
    - Get ontology from onto-creator.py as input
    - Process every Java file in AndroidChess folder to create instances and populate the ontology
    """
    onto = get_ontology("tree.owl").load()
    folderpath = r"android-chess/app/src/main/java/jwtc/chess"
    filepaths = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    for path in filepaths:
        if isfile(path):
            with open(path, 'r') as java_file:
                tree_of_java_file = javalang.parse.parse(java_file.read())
                populateOntology(onto, tree_of_java_file)
                onto.save(file="tree2.owl", format="rdfxml")


if __name__ == "__main__":
    main()
