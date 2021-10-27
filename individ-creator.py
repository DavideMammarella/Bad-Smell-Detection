from owlready2 import *
import ast
import os
from os.path import isfile
import javalang  # https://github.com/c2nes/javalang


def populateOntology(onto, tree):
    for node in tree.types:
        if type(node) is javalang.tree.ClassDeclaration:  # for each ClassDeclaration in the javalang parse tree
            cd = onto["ClassDeclaration"]()  # create an instance of the ontology class ClassDeclaration
            cd.jname = [node.name]

            for body_cd in node.body:
                if type(body_cd) is javalang.tree.MethodDeclaration:
                    md = onto["MethodDeclaration"]()
                    md.jname = [body_cd.name]
                    cd.body.append(md)
                    # create statement instances (first element is the path!)
                    for _, statement in body_cd:
                        if type(statement) is javalang.tree.Statement:
                            statement_name = type(statement).__name__
                            statement_instance = onto[statement_name]()
                            md.body.append(statement_instance)
                elif type(body_cd) is javalang.tree.ConstructorDeclaration:
                    cdec = onto["ConstructorDeclaration"]()
                    cdec.jname = [body_cd.name]
                    cd.body.append(cdec)
                    # create statement instances (first element is the path!)
                    for _, statement in body_cd:
                        if type(statement) is javalang.tree.Statement:
                            statement_name = type(statement).__name__
                            statement_instance = onto[statement_name]()
                            cdec.body.append(statement_instance)
                elif type(body_cd) is javalang.tree.FieldDeclaration:
                    for f in body_cd.declarators:
                        fd = onto["FieldDeclaration"]()
                        fd.jname = [f.name]
                        cd.body.append(fd)
            """
                For each class member (MethodDeclaration/FieldDeclaration/ConstructorDeclaration) in the
                "body" of a ClassDeclaration create a MethodDeclaration/FieldDeclaration/ConstructorDeclaration
                instance and add (append) the member instance to the property "body" of the ClassDeclaration instance
                
                For each Statement (IfStatement, WhileStatement, etc.) reachable from the body of a
                MethodDeclaration or ConstructorDeclaration, create a Statement instance  and add (append) 
                the Statement instances to the property "body" of the MethodDeclaration or ConstructorDeclaration
            """


def main():
    onto = get_ontology("tree.owl").load()  # load the ontology created in step 1 (onto-creator.py)

    # multiple javafile processing (stackoverflow.com/questions/58108964/how-to-open-multiple-files-in-loop-in-python)
    folderpath = r"input/android-chess/app/src/main/java/jwtc/chess"  # make sure to put the 'r' in front
    filepaths = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    for path in filepaths:
        if isfile(path):
            with open(path, 'r') as f:
                javafile = f.read()  # get a java file of android-chess as input file
                tree_of_javafile = javalang.parse.parse(javafile)  # get the TREE of input file
                populateOntology(onto, tree_of_javafile)  # populate the ontology
                onto.save(file="tree2.owl", format="rdfxml")  # save the ontology


def test_ontology():
    world = World()
    onto = world.get_ontology("tree.owl").load()
    tree = javalang.parse.parse("class A { int x, y; }")
    populateOntology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]
    assert a.body[0].is_a[0].name == 'FieldDeclaration'
    assert a.body[0].jname[0] == 'x'
    assert a.body[1].is_a[0].name == 'FieldDeclaration'
    assert a.body[1].jname[0] == 'y'


if __name__ == "__main__":
    main()
    #test_ontology()
