from owlready2 import *
import javalang
import importlib
onto_creator = importlib.import_module("onto-creator")
individ_creator = importlib.import_module("individ-creator")

def test_populate_ontology():
  world = World()
  onto_creator.main()
  onto = world.get_ontology("tree.owl").load()
  tree = javalang.parse.parse("class classTest {"
                              "   int x, y;"
                              "   private methodConstructor(){}"
                              "   protected void methodEmpty(string a){}"
                              "   public void methodStatements(double b, long c, string d){"
                              "       if(b>0) {}"
                              "       else {}"
                              "       while(c<0) {}"
                              "       for(int i; i<5; i++) {}"
                              "       try {methodNull();} catch(NullPointerException e){}"
                              "   }"
                              "}")
  individ_creator.populate_ontology(onto, tree)

  a = onto["ClassDeclaration"].instances()[0]

  assert a.body[0].is_a[0].name == "FieldDeclaration"
  assert a.body[1].is_a[0].name == "FieldDeclaration"
  assert a.body[0].jname[0] == "x"
  assert a.body[1].jname[0] == "y"

  assert a.body[2].is_a[0].name == "ConstructorDeclaration"
  assert a.body[2].jname[0] == "methodConstructor"

  assert a.body[3].is_a[0].name == "MethodDeclaration"
  assert a.body[3].jname[0] == "methodEmpty"
  assert a.body[3].parameters[0].is_a[0].name == "FormalParameter"
  assert a.body[3].parameters[0].name == "formalparameter1"

  assert a.body[4].is_a[0].name == "MethodDeclaration"
  assert a.body[4].jname[0] == "methodStatements"
  assert a.body[4].parameters[0].is_a[0].name == "FormalParameter"
  assert a.body[4].parameters[1].is_a[0].name == "FormalParameter"
  assert a.body[4].parameters[2].is_a[0].name == "FormalParameter"
  assert a.body[4].parameters[0].name == "formalparameter2"
  assert a.body[4].parameters[1].name == "formalparameter3"
  assert a.body[4].parameters[2].name == "formalparameter4"
  assert a.body[4].body[0].is_a[0].name == "IfStatement"
  assert a.body[4].body[2].is_a[0].name == "BlockStatement"
  assert a.body[4].body[3].is_a[0].name == "WhileStatement"
  assert a.body[4].body[4].is_a[0].name == "BlockStatement"
  assert a.body[4].body[5].is_a[0].name == "ForStatement"
  assert a.body[4].body[6].is_a[0].name == "BlockStatement"
  assert a.body[4].body[7].is_a[0].name == "TryStatement"
  assert a.body[4].body[8].is_a[0].name == "StatementExpression"
  assert a.body[4].body[9].is_a[0].name == "CatchClause"

