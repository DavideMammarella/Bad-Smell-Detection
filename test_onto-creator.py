from owlready2 import *
import importlib
onto_creator = importlib.import_module("onto-creator")

def test_class_hierarchy():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    class_hierarchy = ["Annotation", "ArrayInitializer", "CompilationUnit", "Declaration",
                       "Documented", "ElementArrayValue", "ElementValuePair", "EnhancedForControl",
                       "EnumBody", "Expression", "ForControl", "Import", "InferredFormalParameter",
                       "Statement", "SwitchStatementCase", "Type", "TypeArgument", "TypeParameter",
                       "VariableDeclarator"]
    for element in class_hierarchy:
        cd = onto[element]
        assert cd.name == element
        assert len(cd.is_a) == 1


def test_class_count():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    count = 1  # Thing get excluded in onto.classes()
    for _ in onto.classes():
        count = count + 1

    assert count == 78


def test_object_property_count():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    count = 0
    for _ in onto.object_properties():
        count = count + 1

    assert count == 2


def test_data_property_count():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    count = 0
    for _ in onto.data_properties():
        count = count + 1

    assert count == 65


def test_classes():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    # Class
    cd = onto["ClassDeclaration"]
    assert cd.name == "ClassDeclaration"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == "TypeDeclaration"


def test_class_members():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    class_members = ["MethodDeclaration", "FieldDeclaration"]
    for class_member in class_members:
        cd = onto[class_member]
        assert cd.name == class_member
        assert len(cd.is_a) == 2
        assert cd.is_a[0].name == "Member"
        assert cd.is_a[1].name == "Declaration"

    cd = onto["ConstructorDeclaration"]
    assert cd.name == "ConstructorDeclaration"
    assert len(cd.is_a) == 2
    assert cd.is_a[0].name == "Declaration"
    assert cd.is_a[1].name == "Documented"


def test_statements():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    cd = onto["Statement"]
    assert cd.name == "Statement"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == "Thing"

    statement_types = ["BlockStatement", "BreakStatement", "ContinueStatement", "DoStatement",
                       "ForStatement", "IfStatement", "ReturnStatement", "StatementExpression",
                       "SwitchStatement", "SynchronizedStatement", "ThrowStatement", "TryStatement",
                       "WhileStatement", "CatchClause"]
    for statement in statement_types:
        cd = onto[statement]
        assert cd.name == statement
        assert len(cd.is_a) == 1
        assert cd.is_a[0].name == "Statement"


def test_parameters():
    world = World()
    onto_creator.main()
    onto = world.get_ontology("tree.owl").load()

    cd = onto["FormalParameter"]
    assert cd.name == "FormalParameter"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == "Declaration"
