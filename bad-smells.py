import javalang
import rdflib
import rdflib.plugins.sparql as sq
from owlready2 import *
import importlib

# Global variables used only for Latex output purpose
tab_number = 0
bad_smells = []

def writeLogBadSmells(bad_smells):
    with open("log.txt", "a+") as file_object:
        file_object.write("\n\\begin{table}[H]\n\\centering \\scriptsize\n\\begin{tabular}{c c c}\n\\hline\nBad Smell & Count\\\\\n\\hline\n")
        for row in bad_smells:
            file_object.write(row)
        file_object.write("\\hline\n\\end{tabular}\n\\caption{Bad smells (Total).}\n\\label{table:badSmellTable}\n\\end{table}\n")

def writeLog(title, query_result, tab_number):
    with open("log.txt", "a+") as file_object:
        if len(query_result):
            file_object.write("\n\\begin{table}[H]\n\\centering \\scriptsize\n\\begin{tabular}{c c c}\n\\hline\nClass Name & Method Name & Number Of Instances\\\\\n\\hline\n")
            tab_number = tab_number + 1
            count = 0
            for row in query_result:
                file_object.write(row.cn)
                file_object.write(" & ")
                file_object.write(row.mn)
                file_object.write(" & ")
                file_object.write(str(int(row.tot)))
                file_object.write(" \\\\\n")
                count = count + 1
            file_object.write("\\hline\n\\end{tabular}\n\\caption{"+title+".}\n\\label{table:tab"+str(tab_number)+"}\n\\end{table}\n\n\n")
            bad_smells.append(title+" & "+str(count)+" \\\\\n")
        else:
            bad_smells.append(title + " & 0 \\\\\n")


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
    title = "Test:"
    writeLog(title, query_result, 0)

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
            HAVING (COUNT(?statement) >= 20)""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Long Methods"
    writeLog(title, query_result, 1)

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
            HAVING (COUNT(?statement) >= 20)""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Long Constructors"
    writeLog(title, query_result, 2)

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
            HAVING (COUNT(?method) >= 20)""",
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Large Classes"
    writeLog(title, query_result, 3)

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
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Methods with Switch"
    writeLog(title, query_result, 4)

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
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Constructors with Switch"
    writeLog(title, query_result, 5)

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
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Methods with Long Parameter List"
    writeLog(title, query_result, 6)

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
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Constructors with Long Parameter List"
    writeLog(title, query_result, 7)

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
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    query_result = g.query(q)
    title = "Classes with only Setters and Getters"
    writeLog(title, query_result, 8)


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
    main()
