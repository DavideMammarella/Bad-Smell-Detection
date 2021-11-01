import rdflib
import rdflib.plugins.sparql as sq


def writeLog(title, query_result):
    with open("log.txt", "a+") as file_object:
        file_object.write("\n"+title+"\n")
        for row in query_result:
            file_object.write(row.cn)
            file_object.write("::")
            file_object.write(row.mn)
            file_object.write("::")
            file_object.write(str(int(row.tot)))
            file_object.write("\n")


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
                ?m tree:body ?stmt .
                ?stmt a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?m
            HAVING (COUNT(?stmt) >= 20)""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Long Methods Query Results:"
    writeLog(title, query_result)


def main():
    g = rdflib.Graph()
    g.load("tree2.owl")
    open("log.txt", "w").close()  # erase the log on every start
    # queries
    testQuery(g)
    findLongMethods(g)


if __name__ == "__main__":
    main()
