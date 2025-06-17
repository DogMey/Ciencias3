import unittest
from semantic import semantic_analyze, scope_stack

class TestSemanticAnalyzer(unittest.TestCase):

    def setUp(self):
        # Limpia la pila de ámbitos antes de cada test
        scope_stack.clear()

    def test_variable_declaration_and_use(self):
        ast = [
            ("DECLARATION", "int", "x"),
            ("ASSIGNMENT", "x", 5),
            ("CALL", "print", ["x"])
        ]
        self.assertTrue(semantic_analyze(ast))

    def test_variable_shadowing(self):
        ast = [
            ("DECLARATION", "int", "x"),
            ("ASSIGNMENT", "x", 1),
            ("CALL", "print", ["x"]),
            ("FUNC_DECL", "foo", [("int", "x")], "void", [
                ("ASSIGNMENT", "x", 2),
                ("CALL", "print", ["x"])
            ])
        ]
        self.assertTrue(semantic_analyze(ast))

    def test_variable_not_declared(self):
        ast = [
            ("ASSIGNMENT", "x", 5)
        ]
        with self.assertRaises(Exception) as context:
            semantic_analyze(ast)
        self.assertIn("no ha sido declarada", str(context.exception))

    def test_constant_modification(self):
        ast = [
            ("CONST_DECLARATION", "PI", 3.14),
            ("ASSIGNMENT", "PI", 3.1416)
        ]
        with self.assertRaises(Exception) as context:
            semantic_analyze(ast)
        self.assertIn("no se puede modificar la constante", str(context.exception))

    def test_unused_variable(self):
        ast = [
            ("DECLARATION", "int", "x")
        ]
        with self.assertRaises(Exception) as context:
            semantic_analyze(ast)
        self.assertIn("fue declarada pero nunca utilizada", str(context.exception))

    def test_function_declaration_and_call(self):
        ast = [
            ("FUNC_DECL", "sumar", [("int", "a"), ("int", "b")], "int", [
                ("RETURN", ("+", "a", "b"))
            ]),
            ("CALL", "sumar", [2, 3])
        ]
        self.assertTrue(semantic_analyze(ast))

    def test_function_wrong_arity(self):
        ast = [
            ("FUNC_DECL", "sumar", [("int", "a"), ("int", "b")], "int", [
                ("RETURN", ("+", "a", "b"))
            ]),
            ("CALL", "sumar", [2])
        ]
        with self.assertRaises(Exception) as context:
            semantic_analyze(ast)
        self.assertIn("Aridad incorrecta", str(context.exception))

    def test_return_type_check(self):
        ast = [
            ("FUNC_DECL", "foo", [("int", "a")], "int", [
                ("RETURN", "a")
            ])
        ]
        self.assertTrue(semantic_analyze(ast))

        ast_wrong = [
            ("FUNC_DECL", "foo", [("int", "a")], "int", [
                ("RETURN", "a"),
                ("RETURN", "hola")  # 'hola' no es int
            ])
        ]
        with self.assertRaises(Exception) as context:
            semantic_analyze(ast_wrong)
        self.assertIn("no es compatible con el tipo esperado", str(context.exception))

if __name__ == '__main__':
    unittest.main()