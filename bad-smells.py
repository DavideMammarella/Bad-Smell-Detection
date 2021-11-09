import javalang
import rdflib
import rdflib.plugins.sparql as sq
from owlready2 import *
import importlib


def writeLogBadSmells(bad_smells):
    with open("log.txt", "a+") as file_object:
        file_object.write(
            "\\begin{table}[H]\n\\centering \\scriptsize\n\\begin{tabular}{c c c}\n\\hline\nBad Smell & Count\\\\\n\\hline\n")
        for row in bad_smells:
            file_object.write(row)
        file_object.write(
            "\\hline\n\\end{tabular}\n\\caption{Bad smells (Total).}\n\\label{table:tab[EDIT TAB NUMBER]}\n\\end{table}")


def writeLog(title, query_result):
    with open("log.txt", "a+") as file_object:
        if len(query_result):
            file_object.write(
                "\\begin{table}[H]\n\\centering \\scriptsize\n\\begin{tabular}{c c c}\n\\hline\nClass Name & Method Name & Number Of Instances\\\\\n\\hline\n")
            count = 0
            for row in query_result:
                file_object.write(row.cn)
                file_object.write(" & ")
                file_object.write(row.mn)
                file_object.write(" & ")
                file_object.write(str(int(row.tot)))
                file_object.write(" \\\\\n")
                count = count + 1
            file_object.write(
                "\\hline\n\\end{tabular}\n\\caption{" + title + ".}\n\\label{table:tab[EDIT TAB NUMBER]}\n\\end{table}\n\n\n\n")
            bad_smells.append(title + " & " + str(count) + " \\\\\n")
        else:
            bad_smells.append(title + " & 0 \\\\\n")


# Long Methods: >= 20 statements
def findLongMethods(g):
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
    title = "Long methods"
    writeLog(title, query_result)


# Long Constructor: >= 20 statements
def findLongConstructors(g):
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
    title = "Long constructors"
    writeLog(title, query_result)


# LargeClass: >= 10 methods
def findLargeClasses(g):
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
            } GROUP BY ?class
            HAVING (COUNT(?method) >= 20)
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Large classes"
    writeLog(title, query_result)


# MethodWithSwitch: >= 1 switch statement in method/constructor body
def findMethodsWithSwitch(g):
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
    title = "Methods with switch statements"
    writeLog(title, query_result)


# ConstructorWithSwitch: >= 1 switch statement in method/constructor body
def findConstructorsWithSwitch(g):
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
    title = "Constructors with switch statements"
    writeLog(title, query_result)


# MethodWithLongParameterList: >= 5 parameters
def findMethodsWithLongParameterList(g):
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
    title = "Methods with long parameter list"
    writeLog(title, query_result)


# ConstructorWithLongParameterList: >= 5 parameters
def findConstructorsWithLongParameterList(g):
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
    title = "Constructors with long parameter list"
    writeLog(title, query_result)


# DataClass: class with only setters and getters
def findDataClasses(g):
    q = sq.prepareQuery(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?class a tree:ClassDeclaration .
                ?class tree:jname ?cn .
                ?class tree:body ?method .
                ?method a tree:MethodDeclaration .
                ?method tree:jname ?mn .
                FILTER(
                    regex(?mn, "get.*") ||
                    regex(?mn, "set.*")
                )
            } GROUP BY ?class
            ORDER BY DESC(COUNT(*))""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Data Classes"
    writeLog(title, query_result)


def main():
    g = rdflib.Graph()
    g.load("tree2.owl")
    open("log.txt", "w").close()  # erase the log on every start
    # queries
    findLongMethods(g)
    findLongConstructors(g)
    findLargeClasses(g)
    findMethodsWithSwitch(g)
    findConstructorsWithSwitch(g)
    findMethodsWithLongParameterList(g)
    findConstructorsWithLongParameterList(g)
    findDataClasses(g)
    # write smells detection table
    writeLogBadSmells(bad_smells)


if __name__ == "__main__":
    # Global variables used only for Latex output purpose
    global bad_smells
    bad_smells = []
    main()
