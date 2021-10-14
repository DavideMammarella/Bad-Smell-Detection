from owlready2 import *
import ast
import javalang



def populateOntology(onto, tree):
    #class that populate the ontology
    print(tree)
    print("Entered the class!")


def main():
    onto = get_ontology("output/tree_section1.owl").load()  # load the ontology created in step 1 (onto-creator.py)
    # loop because you need every javafile
    javafile = open(
            "input/android-chess/app/src/main/java/jwtc/chess/Pos.java")  # get a java file of android-chess as input file
    tree_of_javafile = javalang.parse.parse(javafile.read())  # get the TREE of input file
    populateOntology(onto, tree_of_javafile)
    onto.save(file="output/tree_section2.owl", format="rdfxml")  # save the ontology


# def test_ontology():
#     onto = get_ontology("tree_section2.owl").load()
#     tree = javalang.parse.parse("class A { int x, y; }")
#     populateOntology(onto, tree)
#     a = onto['ClassDeclaration'].instances()[0]
#     assert a.body[0].is_a[0].name == 'FieldDeclaration'
#     assert a.body[0].jname[0] == 'x'
#     assert a.body[1].is_a[0].name == 'FieldDeclaration'
#     assert a.body[1].jname[0] == 'y'
#     print("Ontology is fine!")


if __name__ == "__main__":
    main()
    #test_ontology()
