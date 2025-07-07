import unittest
from lexer.lexer_tokens import KEYWORDS, TOKEN_DEFINITIONS

class TestLexerTokens(unittest.TestCase):
    def test_keywords(self):
        self.assertIn('if', KEYWORDS)
        self.assertIn('func', KEYWORDS)
        self.assertNotIn('variable', KEYWORDS)

    def test_token_definitions(self):
        token_types = [t[0] for t in TOKEN_DEFINITIONS]
        self.assertIn('STRING', token_types)
        self.assertIn('IDENTIFIER', token_types)
        self.assertIn('NUMBER', token_types)

if __name__ == '__main__':
    unittest.main()