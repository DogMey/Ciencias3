from .utils import expect, parse_id, match
from .expressions import parse_expression

def parse_assignment(tokens, expect_semicolon=True):
    ident = parse_id(tokens)
    # Soporte para i++ y i--
    if match(tokens, 'INCREMENT'):
        tokens.pop(0)
        if expect_semicolon:
            expect(tokens, 'SEMICOLON')
        return ('INCREMENT', ident)
    elif match(tokens, 'DECREMENT'):
        tokens.pop(0)
        if expect_semicolon:
            expect(tokens, 'SEMICOLON')
        return ('DECREMENT', ident)
    # Asignación tradicional
    expect(tokens, 'OPERATOR', '=')
    value = parse_expression(tokens)
    if expect_semicolon:
        expect(tokens, 'SEMICOLON')
    return ('ASSIGNMENT', ident, value)