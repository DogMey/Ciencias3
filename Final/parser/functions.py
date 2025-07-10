from .utils import expect, parse_id, match, parse_type
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

def parse_function_declaration(tokens):
    # Soporta: func int nombre(tipo1 arg1, tipo2 arg2, ...) { ... }
    expect(tokens, 'KEYWORD', 'func')
    return_type = parse_type(tokens)  # int, float, etc.
    func_name = parse_id(tokens)
    expect(tokens, 'LPAREN')
    params = []
    if not match(tokens, 'RPAREN'):
        while True:
            param_type = parse_type(tokens) # int, float, etc.
            param_name = parse_id(tokens)
            params.append((param_type, param_name))
            if match(tokens, 'COMMA'):
                tokens.pop(0)
            else:
                break
    expect(tokens, 'RPAREN')
    expect(tokens, 'LBRACE')
    body = []
    from .statements import parse_statement  # Importación local para evitar ciclos
    while tokens and not match(tokens, 'RBRACE'):
        body.append(parse_statement(tokens))
    if not match(tokens, 'RBRACE'):
        if tokens:
            tipo, val, line, col = tokens[-1]
            raise SyntaxError(f"Error en línea {line}, columna {col}: falta '}}' de cierre en el cuerpo de la función")
        else:
            raise SyntaxError("Error: falta '}' de cierre en el cuerpo de la función, llegó al final del archivo")
    tokens.pop(0)  # Consumir '}'
    return ('FUNC_DECL', func_name, params, return_type, body)

def parse_return(tokens):
    from .utils import match
    from .expressions import parse_expression
    expect(tokens, 'KEYWORD', 'return')
    # Permite return con o sin expresión (ej. return;)
    if match(tokens, 'SEMICOLON'):
        tokens.pop(0)
        return ('RETURN', None)
    expr = parse_expression(tokens)
    expect(tokens, 'SEMICOLON')
    return ('RETURN', expr)