from .utils import match, expect, parse_id, parse_type, parse_num
from .expressions import parse_expression

def parse_declaration(tokens):
    tipo = parse_type(tokens)
    ident = parse_id(tokens)
    expr = None
    if match(tokens, 'OPERATOR', '='):
        expect(tokens, 'OPERATOR', '=')
        expr = parse_expression(tokens)
    expect(tokens, 'SEMICOLON')
    if expr is not None:
        return ('DECLARATION', tipo, ident, expr)
    else:
        return ('DECLARATION', tipo, ident)