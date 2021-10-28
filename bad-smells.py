import rdflib
import rdflib.plugins.sparql as sq


def main():
    g = rdflib.Graph()
    g.load("tree2.owl")

    print(len(g)) #we have 1751 lines

    q1 = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?m""",
        initNs={"tree": "http://test.org/onto.owl#"})

    for row in g.query(q1):
        print(row.cn, "::", row.mn, "::", int(row.tot))

if __name__ == "__main__":
    main()