import rdflib
from owlready2 import *
import javalang
import importlib

onto_creator = importlib.import_module("onto-creator")
individ_creator = importlib.import_module("individ-creator")
bad_smells = importlib.import_module("bad-smells")

def create_ontology():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()
    return onto

def delete_temp_files():
    try:
        os.remove("tree.owl")
        os.remove("tmp.owl")
        os.remove("log.txt")
    except OSError:
        pass

def test_long_methods():
    onto = create_ontology()
    tree = javalang.parse.parse("class Main { "
                                "   public void method(int x) { "
                                "   x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;"
                                "   x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;"
                                "   } "
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    query_result = bad_smells.find_long_methods(g)

    assert len(query_result) == 1
    for row in query_result:
        assert (row.cn.value == "Main")
        assert (row.mn.value == "method")
        assert (row.tot.value == 21)
    delete_temp_files()


def test_long_constructors():
    onto = create_ontology()
    tree = javalang.parse.parse("class Main { "
                                "   public Main(int x) {"
                                "   x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;"
                                "   x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;"
                                "   } "
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    query_result = bad_smells.find_long_constructors(g)

    assert len(query_result) == 1
    for row in query_result:
        assert (row.cn.value == "Main")
        assert (row.tot.value == 21)
    delete_temp_files()

def test_large_classes():
    onto = create_ontology()
    tree = javalang.parse.parse("class Main { "
                                "   public void method1(int x) {}"
                                "   public void method2(int x) {}"
                                "   public void method3(int x) {}"
                                "   public void method4(int x) {}"
                                "   public void method5(int x) {}"
                                "   public void method6(int x) {}"
                                "   public void method7(int x) {}"
                                "   public void method8(int x) {}"
                                "   public void method9(int x) {}"
                                "   public void method10(int x) {}"
                                "   public void method11(int x) {}"
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    query_result = bad_smells.find_large_classes(g)

    assert len(query_result) == 1
    for row in query_result:
        assert (row.cn.value == "Main")
        assert (row.tot.value == 11)

    delete_temp_files()

def test_methods_with_switch():
    onto = create_ontology()
    tree = javalang.parse.parse("class Main { "
                                "   public void method(int x) {}"
                                "   public void methodSwitch(int x) {"
                                "      int month = 2;"
                                "       int year = 2000;"
                                "       int numDays = 0;"
                                "       switch (month) {"
                                "           case 1: case 3: case 5:"
                                "           case 7: case 8: case 10:"
                                "           case 12:"
                                "               numDays = 31;"
                                "               break;"
                                "           case 4: case 6:"
                                "           case 9: case 11:"
                                "               numDays = 30;"
                                "               break;"
                                "           case 2:"
                                "               if (((year % 4 == 0) && "
                                "                   !(year % 100 == 0))"
                                "                   || (year % 400 == 0))"
                                "               numDays = 29;"
                                "               else"
                                "                   numDays = 28;"
                                "           break;"
                                "       }"
                                "   }"
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    query_result = bad_smells.find_methods_with_switch(g)

    assert len(query_result) == 1
    for row in query_result:
        assert (row.cn.value == "Main")
        assert (row.mn.value == "methodSwitch")
        assert (row.tot.value == 1)
    delete_temp_files()

def test_constructors_with_switch():
    onto = create_ontology()
    tree = javalang.parse.parse("class Main { "
                                "   public void method(int x) {}"
                                "   public Main(int x) {"
                                "      int month = 2;"
                                "       int year = 2000;"
                                "       int numDays = 0;"
                                "       switch (month) {"
                                "           case 1: case 3: case 5:"
                                "           case 7: case 8: case 10:"
                                "           case 12:"
                                "               numDays = 31;"
                                "               break;"
                                "           case 4: case 6:"
                                "           case 9: case 11:"
                                "               numDays = 30;"
                                "               break;"
                                "           case 2:"
                                "               if (((year % 4 == 0) && "
                                "                   !(year % 100 == 0))"
                                "                   || (year % 400 == 0))"
                                "               numDays = 29;"
                                "               else"
                                "                   numDays = 28;"
                                "           break;"
                                "       }"
                                "   }"
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    query_result = bad_smells.find_constructors_with_switch(g)

    assert len(query_result) == 1
    for row in query_result:
        assert (row.cn.value == "Main")
        assert (row.tot.value == 1)
    delete_temp_files()

def test_methods_with_long_parameter_list():
    onto = create_ontology()
    tree = javalang.parse.parse("class Main { "
                                "   public void method1(int x) {}"
                                "   public void method2(int a, int b, int c, int d, int e) {}"
                                "   public void method3(String a, Long b, Double c, int d, int e, int f) {}"
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    query_result = bad_smells.find_methods_with_long_parameter_list(g)

    assert len(query_result) == 2
    for row in query_result:
        assert (row.cn.value == "Main")
        if (row.mn.value == "method2"):
            assert (row.tot.value == 5)
        elif (row.mn.value == "method3"):
            assert (row.tot.value == 6)
    delete_temp_files()


def test_constructors_with_long_parameter_list():
    onto = create_ontology()
    tree = javalang.parse.parse("class Main { "
                                "   public void method1(int x) {}"
                                "   public void method2(int a, int b, int c, int d, int e) {}"
                                "   public Main(String a, Long b, Double c, int d, int e, int f) {}"
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    query_result = bad_smells.find_constructors_with_long_parameter_list(g)

    assert len(query_result) == 1
    for row in query_result:
        assert (row.cn.value == "Main")
        assert (row.tot.value == 6)
    delete_temp_files()


def test_data_classes():
    onto = create_ontology()
    tree = javalang.parse.parse("class Class1 { "
                                "   public void method(int x) {}"
                                "}"
                                "class Class2 { "
                                "   public int getA() {}"
                                "   public int setA() {}"
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.parse("tmp.owl")
    getset_classes_query_result, all_classes_query_result = bad_smells.find_data_classes(g)

    assert len(getset_classes_query_result) == 1
    assert len(all_classes_query_result) == 2

    for normal_class in all_classes_query_result:
        for data_class in getset_classes_query_result:
            if (normal_class.mn == data_class.mn) and (normal_class.tot == data_class.tot):
                assert (data_class.cn.value == "Class2")

    delete_temp_files()