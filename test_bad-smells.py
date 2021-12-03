import rdflib
from owlready2 import *
import javalang
import importlib

individ_creator = importlib.import_module("individ-creator")
bad_smells = importlib.import_module("bad-smells")

def test_long_methods():
    world = World()
    onto = world.get_ontology("tree.owl").load()
    tree = javalang.parse.parse("class classTest { "
                                "   public void method(int x) { "
                                "   x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;"
                                "   } "
                                "}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")
    query_result = bad_smells.find_long_methods(g)

    assert len(query_result) == 1
    for row in query_result:
        assert(row.cn.value == "classTest")
        assert (row.mn.value == "method")
        assert (row.tot.value == 21)