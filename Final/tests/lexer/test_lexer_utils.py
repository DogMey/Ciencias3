import unittest
from lexer.lexer_utils import is_keyword, add_token
from lexer.lexer_tokens import KEYWORDS

class TestLexerUtils(unittest.TestCase):
    def test_is_keyword(self):
        self.assertTrue(is_keyword('IDENTIFIER', 'if', KEYWORDS))
        self.assertFalse(is_keyword('IDENTIFIER', 'variable', KEYWORDS))
        self.assertFalse(is_keyword('NUMBER', 'if', KEYWORDS))

    def test_add_token(self):
        tokens = []
        add_token(tokens, 'IDENTIFIER', 'if', 1, 1, KEYWORDS)
        add_token(tokens, 'IDENTIFIER', 'x', 1, 4, KEYWORDS)
        self.assertEqual(tokens[0][0], 'KEYWORD')
        self.assertEqual(tokens[1][0], 'IDENTIFIER')

if __name__ == '__main__':
    unittest.main()