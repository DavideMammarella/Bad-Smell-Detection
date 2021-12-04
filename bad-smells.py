import rdflib
import rdflib.plugins.sparql as sq


def write_log_data_classes_and_bad_smells(getset_classes_query_result, all_classes_query_result):
    """
    Check if the number of filtered/unfiltered methods obtained from "find_data_classes" are the same
    and write the data classes in latex table format.
    Write all bad smells in latex table format.
    """
    global bad_smells
    data_class_count = 0

    with open("log.txt", "a+") as f:
        f.write("\\begin{table}[H]\n\\centering \\scriptsize\n\\begin{tabular}{c c c}\n\\hline\n"
                "Class Name & Filtered Method & Unfiltered Method\\\\\n\\hline\n")
        for normal_class in all_classes_query_result:
            for data_class in getset_classes_query_result:
                if (normal_class.mn == data_class.mn) and (normal_class.tot == data_class.tot):
                    f.write(data_class.cn)
                    f.write(" & ")
                    f.write(str(int(data_class.tot)))
                    f.write(" & ")
                    f.write(str(int(normal_class.tot)))
                    f.write(" \\\\\n")
                    data_class_count = data_class_count + 1
        bad_smells.append("Data Classes & " + str(int(data_class_count)) + " \\\\\n")
        f.write("\\hline\n\\end{tabular}\n\\"
                "caption{Data classes.}\n\\label{table:tab[EDIT TAB NUMBER]}\n\\end{table}\n\n\n\n"
                "\\begin{table}[H]\n\\centering \\scriptsize\n\\begin{tabular}{c c c}\n\\hline\n"
                "Bad Smell & Count\\\\\n\\hline\n")
        for row in bad_smells:
            f.write(row)
        f.write("\\hline\n\\end{tabular}\n\\"
                "caption{Bad smells (Total).}\n\\label{table:tab[EDIT TAB NUMBER]}\n\\end{table}")


def write_log_query(title, query_result):
    """
    Write the result of a query in latex table format.
    """
    global bad_smells
    count = 0

    with open("log.txt", "a+") as f:
        if len(query_result):
            f.write("\\begin{table}[H]\n\\centering \\scriptsize\n\\begin{tabular}{c c c}\n\\hline\n"
                    "Class Name & Method Name & Number of Occurrences\\\\\n\\hline\n")
            for row in query_result:
                f.write(row.cn)
                f.write(" & ")
                f.write(row.mn)
                f.write(" & ")
                f.write(str(int(row.tot)))
                f.write(" \\\\\n")
                count = count + 1
            f.write("\\hline\n\\end{tabular}\n\\"
                    "caption{" + title + ".}\n\\label{table:tab[EDIT TAB NUMBER]}\n\\end{table}\n\n\n\n")
            bad_smells.append(title + " & " + str(count) + " \\\\\n")
        else:
            bad_smells.append(title + " & 0 \\\\\n")


def find_long_methods(g):
    """
    Query returning long methods.
    (i.e. Methods with >= 20 statements)
    """
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
                ?method tree:body ?statement .
                ?statement a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?method
            HAVING (COUNT(?statement) >= 20)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)

    try:
        write_log_query("Long methods", query_result)
    except:
        return query_result


def find_long_constructors(g):
    """
    Query returning long constructors.
    (i.e. Constructor with >= 20 statements)
    """
    q = sq.prepareQuery(
        """SELECT ?cname ?cn (COUNT(*) AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?cdec .
                ?cdec a tree:ConstructorDeclaration .
                ?cdec tree:jname ?cname .
                ?cdec tree:body ?statement .
                ?statement a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?cdec
            HAVING (COUNT(?statement) >= 20)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)

    try:
        write_log_query("Long constructors", query_result)
    except:
        return query_result


def find_large_classes(g):
    """
    Query returning large classes.
    (i.e. Class with >= 10 methods)
    """
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
            } GROUP BY ?class
            HAVING (COUNT(?method) >= 10)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    try:
        write_log_query("Large classes", query_result)
    except:
        return query_result


def find_methods_with_switch(g):
    """
    Query returning methods with switch.
    (i.e. Method with >= 1 switch statement in method/constructor body)
    """
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
                ?method tree:body ?statement .
                ?statement a tree:SwitchStatement .
            } GROUP BY ?method
            HAVING (COUNT(?statement) >= 1)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)

    try:
        write_log_query("Methods with switch statements", query_result)
    except:
        return query_result


def find_constructors_with_switch(g):
    """
    Query returning constructor with switch.
    (i.e. Constructor with >= 1 switch statement in method/constructor body)
    """
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?cdec .
                ?cdec a tree:ConstructorDeclaration .
                ?cdec tree:jname ?cname .
                ?cdec tree:body ?statement .
                ?statement a tree:SwitchStatement .
            } GROUP BY ?cdec
            HAVING (COUNT(?statement) >= 1)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)

    try:
        write_log_query("Constructors with switch statements", query_result)
    except:
        return query_result


def find_methods_with_long_parameter_list(g):
    """
    Query returning methods with long parameter list.
    (i.e. Method with >= 5 parameters)
    """
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
                ?method tree:parameters ?parameter .
            } GROUP BY ?method
            HAVING (COUNT(?parameter) >= 5)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)

    try:
        write_log_query("Methods with long parameter list", query_result)
    except:
        return query_result


def find_constructors_with_long_parameter_list(g):
    """
    Query returning constructors with long parameter list.
    (i.e. Constructor with >= 5 parameters)
    """
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?cdec .
                ?cdec a tree:ConstructorDeclaration .
                ?cdec tree:jname ?cname .
                ?cdec tree:parameters ?parameter 
            } GROUP BY ?cdec
            HAVING (COUNT(?parameter) >= 5)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    try:
        write_log_query("Constructors with long parameter list", query_result)
    except:
        return query_result


def find_data_classes(g):
    """
    Query returning data classes.
    (i.e. Class with only setters and getters)

    Two queries are needed to check if the filtered/unfiltered number of methods is the same:
    - q1: retrieve only class with get or set methods.
    - q2: retrieve every class with every methods in the class.
    """
    q1 = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(?method)AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
                FILTER(
                    regex(?mn, "get.*") || regex(?mn, "set.*")
                )
            } GROUP BY ?class""",
        initNs={"tree": "http://test.org/onto.owl#"})
    q2 = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(?method)AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
            } GROUP BY ?class""",
        initNs={"tree": "http://test.org/onto.owl#"})

    getset_classes_query_result = g.query(q1)
    all_classes_query_result = g.query(q2)

    try:
        write_log_data_classes_and_bad_smells(getset_classes_query_result, all_classes_query_result)
    except:
        return getset_classes_query_result, all_classes_query_result

def main():
    """
    Encode bad smells as SPARQL queries:
    - Get ontology from individ-creator.py as input
    - Construct an rdflib Graph from the ontology
    - Query the Graph
    """
    open("log.txt", "w").close()
    global bad_smells
    bad_smells = []

    g = rdflib.Graph()
    g.load("tree2.owl")
    find_long_methods(g)
    find_long_constructors(g)
    find_large_classes(g)
    find_methods_with_switch(g)
    find_constructors_with_switch(g)
    find_methods_with_long_parameter_list(g)
    find_constructors_with_long_parameter_list(g)
    find_data_classes(g)


if __name__ == "__main__":
    main()
