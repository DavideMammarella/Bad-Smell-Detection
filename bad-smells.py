import rdflib
import rdflib.plugins.sparql as sq

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

    with open("log.txt", "a+") as file_object:
        file_object.write("\nQuery Test Result:\n")
        for row in g.query(q):
            file_object.write(row.cn)
            file_object.write("::")
            file_object.write(row.mn)
            file_object.write("::")
            file_object.write(str(int(row.tot)))
            file_object.write("\n")

def findLongMethods(g):
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?stmt .
                ?stmt a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?m
            HAVING (COUNT(?stmt) >= 20)""",
        initNs={"tree": "http://test.org/onto.owl#"})

    with open("log.txt", "a+") as file_object:
        file_object.write( "\nLong Methods Query Results:\n")
        for row in g.query(q):
            file_object.write(row.cn)
            file_object.write("::")
            file_object.write(row.mn)
            file_object.write("::")
            file_object.write(str(int(row.tot)))
            file_object.write("\n")

def main():
    g = rdflib.Graph()
    g.load("tree2.owl")
    open("log.txt", "w").close() #erase the log on every start
    # queries
    testQuery(g)
    findLongMethods(g)


if __name__ == "__main__":
    main()