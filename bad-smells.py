import javalang
import rdflib
import rdflib.plugins.sparql as sq
from owlready2 import *
import importlib
individ_creator = importlib.import_module("individ-creator")


def writeLog(title, query_result):
    with open("log.txt", "a+") as file_object:
        file_object.write(title + "\n")
        count = 0
        for row in query_result:
            file_object.write(row.cn)
            file_object.write("::")
            file_object.write(row.mn)
            file_object.write("::")
            file_object.write(str(int(row.tot)))
            file_object.write("\n")
            count = count + 1
        file_object.write("-----------------------\n")
        file_object.write("Total Results: " + str(count) + "\n\n")


def testQuery(g):
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?m""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Test Query Results:"
    writeLog(title, query_result)


def findLongMethods(g):
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?statement .
                ?statement a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?m
            HAVING (COUNT(?statement) >= 20)""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Long Methods Query Results:"
    writeLog(title, query_result)

def test_ontology():
    world = World()
    onto = world.get_ontology("tree.owl").load()
    tree = javalang.parse.parse(
        "class A { int f(int x) { x++;x++;x++;x++;x++;x+ +;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++; } }")
    individ_creator.populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")
    assert len(findLongMethods(g)) == 1


def main():
    g = rdflib.Graph()
    g.load("tree2.owl")
    open("log.txt", "w").close()  # erase the log on every start
    # queries
    # testQuery(g)
    findLongMethods(g)


if __name__ == "__main__":
    main()
    #test_ontology()
