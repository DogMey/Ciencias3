KEYWORDS = {
    'if', 'else', 'while', 'return', 'for', 'int', 'float', 'bool', 'true', 'false',
    'const', 'string', 'function', 'void', 'break', 'continue', 'switch', 'case', 'default', 'func'
}

TOKEN_DEFINITIONS = [
    ('STRING', r'"([^"\\]|\\.)*"'),
    ('CHAR', r"'([^'\\]|\\.)'"),
    ('EQUALS', r'=='),
    ('NOTEQUAL', r'!='),
    ('LESSEQUAL', r'<='),
    ('GREATEREQUAL', r'>='),
    ('INCREMENT', r'\+\+'),
    ('DECREMENT', r'--'),
    ('LESS', r'<'),
    ('GREATER', r'>'),
    ('NOT', r'!'),
    ('COMMENT', r'//.*'),
    ('NUMBER', r'\d+\.\d+|\d+'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('OPERATOR', r'[+\-*/=]'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('WHITESPACE', r'\s+'),
]