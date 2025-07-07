from .utils import match, expect, parse_id, parse_type, parse_num
from .expressions import parse_expression

def parse_declaration(tokens):
    """
    Analiza una declaración de variable, soportando asignación de expresiones o el resultado de una llamada a función.
    Ejemplos:
        int x;
        int y = 2 + 3;
        int z = foo(a, b);
    """
    tipo = parse_type(tokens)
    ident = parse_id(tokens)
    expr = None
    if match(tokens, 'OPERATOR', '='):
        expect(tokens, 'OPERATOR', '=')
        # Si lo siguiente es un identificador seguido de '(', es una llamada a función
        if match(tokens, 'IDENTIFIER') and len(tokens) > 1 and tokens[1][0] == 'LPAREN':
            from .functions import parse_function_call
            expr = parse_function_call(tokens)
        else:
            expr = parse_expression(tokens)
            expect(tokens, 'SEMICOLON')
    if expr is not None:
        return ('DECLARATION', tipo, ident, expr)
    else:
        return ('DECLARATION', tipo, ident)