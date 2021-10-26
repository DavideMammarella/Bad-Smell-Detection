from owlready2 import *
import ast
import javalang  # https://github.com/c2nes/javalang


def populateOntology(onto, tree):
    for node in tree.types:
        if type(node) is javalang.tree.ClassDeclaration:  # for each ClassDeclaration in the javalang parse tree
            cd = onto["ClassDeclaration"]()  # create an instance of the ontology class ClassDeclaration
            cd.jname = [node.name]

            for body_cd in node.body:
                if type(body_cd) is javalang.tree.MethodDeclaration:
                    md = onto["MethodDeclaration"]()
                    md.jname = [node.name]
                    cd.body.append(md)
                elif type(body_cd) is javalang.tree.FieldDeclaration:
                    fd = onto["FieldDeclaration"]()
                    fd.jname = [node.name]
                    cd.body.append(fd)
                elif type(body_cd) is javalang.tree.ConstructorDeclaration:
                    cdec = onto["ConstructorDeclaration"]()
                    cdec.jname = [node.name]
                    cd.body.append(cdec)
            """
                For each class member (MethodDeclaration/FieldDeclaration/ConstructorDeclaration) in the
                "body" of a ClassDeclaration create a MethodDeclaration/FieldDeclaration/ConstructorDeclaration
                instance and add (append) the member instance to the property "body" of the ClassDeclaration instance
            """


def main():
    onto = get_ontology("tree.owl").load()  # load the ontology created in step 1 (onto-creator.py)
    # TODO: Ask if it is possible to upload multiple file in plain Python (not Panda)
    javafile = open(
        "input/android-chess/app/src/main/java/jwtc/chess/Pos.java").read()  # get a java file of android-chess as input file
    tree_of_javafile = javalang.parse.parse(javafile)  # get the TREE of input file
    populateOntology(onto, tree_of_javafile) # populate the ontology
    onto.save(file="tree.owl", format="rdfxml")  # save the ontology


# def test_ontology():
#     onto = get_ontology("tree.owl").load()
#     tree = javalang.parse.parse("class A { int x, y; }")
#     populateOntology(onto, tree)
#     a = onto['ClassDeclaration'].instances()[0]
#     assert a.body[0].is_a[0].name == 'FieldDeclaration'
#     assert a.body[0].jname[0] == 'x'
#     assert a.body[1].is_a[0].name == 'FieldDeclaration'
#     assert a.body[1].jname[0] == 'y'
#     print("Ontology is fine!")
# TODO: Ask why the method seems working on a java class but not on the unit test


if __name__ == "__main__":
    main()
    # test_ontology()
