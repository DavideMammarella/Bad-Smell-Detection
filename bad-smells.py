import rdflib
import rdflib.plugins.sparql as sq


def main():
    g = rdflib.Graph()
    g.load("tree2.owl")

    print(len(g)) #we have 1751 lines

    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?m""",
        initNs={"tree": "http://my.onto.org/tree.owl#"})

    qres = g.query(q)
    for row in qres:
        print(row)


if __name__ == "__main__":
    main()