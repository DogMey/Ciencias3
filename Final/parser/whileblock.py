from .utils import expect, match, parse_condition

def parse_while(tokens):
    expect(tokens, 'KEYWORD', 'while')
    expect(tokens, 'LPAREN')
    condition = parse_condition(tokens)
    expect(tokens, 'RPAREN')
    expect(tokens, 'LBRACE')
    block = []
    from .statements import parse_statement  # Importación local para evitar ciclos
    while tokens and not match(tokens, 'RBRACE'):
        block.append(parse_statement(tokens))
    if not match(tokens, 'RBRACE'):
        if tokens:
            tipo, val, line, col = tokens[-1]
            raise SyntaxError(f"Error en línea {line}, columna {col}: falta '}}' de cierre en el bloque 'while'")
        else:
            raise SyntaxError("Error: falta '}' de cierre en el bloque 'while', llegó al final del archivo")
    tokens.pop(0)  # Consumir '}'
    return ('WHILE', condition, block)
