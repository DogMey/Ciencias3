from .utils import expect, match, match_keyword, parse_condition
from .declaration import parse_declaration
from .assignment import parse_assignment
from .expressions import parse_expression

def parse_for(tokens):
    expect(tokens, 'KEYWORD', 'for')
    expect(tokens, 'LPAREN')
    # Inicialización
    if match_keyword(tokens, 'int') or match_keyword(tokens, 'float'):
        init = parse_declaration(tokens)
    elif match(tokens, 'IDENTIFIER'):
        init = parse_assignment(tokens)
    elif match(tokens, 'SEMICOLON'):
        init = None
        tokens.pop(0)
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba inicialización en bucle 'for', pero se encontró '{val}'")
    # Condición
    if not match(tokens, 'SEMICOLON'):
        condition = parse_condition(tokens)
    else:
        condition = None
    expect(tokens, 'SEMICOLON')
    # Incremento
    if not match(tokens, 'RPAREN'):
        if match(tokens, 'IDENTIFIER'):
            increment = parse_assignment(tokens, expect_semicolon=False)
        else:
            increment = parse_expression(tokens)
    else:
        increment = None
    expect(tokens, 'RPAREN')
    expect(tokens, 'LBRACE')
    block = []
    from .statements import parse_statement  # Importación local para evitar ciclos
    while tokens and not match(tokens, 'RBRACE'):
        block.append(parse_statement(tokens))
    if not match(tokens, 'RBRACE'):
        tipo, val, line, col = tokens[-1]
        raise SyntaxError(f"Error en línea {line}, columna {col}: falta '}}' de cierre en el bloque 'for'")
    tokens.pop(0)  # Consumir '}'
    return ('FOR', init, condition, increment, block)