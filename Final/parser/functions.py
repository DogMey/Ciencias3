from .utils import expect, parse_id, match
from .expressions import parse_expression

def parse_function_call(tokens):
    func_name = parse_id(tokens)
    expect(tokens, 'LPAREN')
    args = []
    # Soporta cero o más argumentos separados por coma
    if not match(tokens, 'RPAREN'):
        while True:
            arg = parse_expression(tokens)
            args.append(arg)
            if match(tokens, 'COMMA'):
                tokens.pop(0)
            else:
                break
    expect(tokens, 'RPAREN')
    expect(tokens, 'SEMICOLON')
    return ('FUNC_CALL', func_name, args)