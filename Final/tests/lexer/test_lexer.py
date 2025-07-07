import unittest
from main_lexer import lexer

class TestLexer(unittest.TestCase):
    def test_simple_tokens(self):
        code = 'int x = 5;'
        tokens = lexer(code)
        self.assertEqual(tokens[0][0], 'KEYWORD')  # int
        self.assertEqual(tokens[1][0], 'IDENTIFIER')  # x
        self.assertEqual(tokens[2][0], 'OPERATOR')  # =
        self.assertEqual(tokens[3][0], 'NUMBER')  # 5
        self.assertEqual(tokens[4][0], 'SEMICOLON')  # ;

    def test_keywords_and_identifiers(self):
        code = 'if else variable'
        tokens = lexer(code)
        self.assertEqual(tokens[0][0], 'KEYWORD')  # if
        self.assertEqual(tokens[1][0], 'KEYWORD')  # else
        self.assertEqual(tokens[2][0], 'IDENTIFIER')  # variable

    def test_string_and_char(self):
        code = '"hola" \'a\''
        tokens = lexer(code)
        self.assertEqual(tokens[0][0], 'STRING')
        self.assertEqual(tokens[1][0], 'CHAR')

    def test_unrecognized_token(self):
        with self.assertRaises(SyntaxError):
            lexer('@')

if __name__ == '__main__':
    unittest.main()