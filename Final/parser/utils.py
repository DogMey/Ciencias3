def match(tokens, type_, value=None):
    if not tokens:
        return False
    tk_type, tk_val, *_ = tokens[0]
    return tk_type == type_ and (value is None or tk_val == value)

def match_keyword(tokens, keyword):
    if not tokens:
        return False
    tk_type, tk_val, *_ = tokens[0]
    return tk_type == 'KEYWORD' and tk_val == keyword

def expect(tokens, type_, value=None):
    if not match(tokens, type_, value):
        if tokens:
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba {type_} '{value}' pero se encontró '{val}'")
        else:
            raise SyntaxError(f"Error: se esperaba {type_} '{value}' pero se encontró EOF")
    tokens.pop(0)

def expect_keyword(tokens, keyword):
    if not match_keyword(tokens, keyword):
        if tokens:
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba palabra clave '{keyword}' pero se encontró '{val}'")
        else:
            raise SyntaxError(f"Error: se esperaba palabra clave '{keyword}' pero se encontró EOF")
    tokens.pop(0)

def parse_id(tokens):
    if not tokens:
        raise SyntaxError("Error: se esperaba identificador, pero no se encontró más tokens.")
    tipo, val, line, col = tokens.pop(0)
    if tipo == 'IDENTIFIER':
        return val
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba identificador, pero se encontró '{val}'")

def parse_type(tokens):
    if not tokens:
        raise SyntaxError("Error: se esperaba tipo, pero no se encontró más tokens.")
    tipo, val, line, col = tokens.pop(0)
    if tipo == 'KEYWORD' and val in ('int', 'float', 'string', 'char', 'bool'):
        return val
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un tipo válido, pero se encontró '{val}'")

def parse_num(tokens):
    if not tokens:
        raise SyntaxError("Error: se esperaba número, pero no se encontró más tokens.")
    tipo, val, line, col = tokens.pop(0)
    if tipo == 'NUMBER':
        return float(val) if '.' in val else int(val)
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un número válido, pero se encontró '{val}'")

def parse_condition(tokens):
    from .expressions import parse_expression
    left = parse_expression(tokens)
    if not tokens:
        raise SyntaxError("Error: se esperaba operador de comparación en condición, pero no se encontró más tokens.")
    op = tokens.pop(0)
    if op[0] not in ('EQUALS', 'NOTEQUAL', 'GREATER', 'LESS', 'LESSEQUAL', 'GREATEREQUAL'):
        raise SyntaxError(f"Error en línea {op[2]}, columna {op[3]}: se esperaba operador de comparación, pero se encontró '{op[1]}'")
    right = parse_expression(tokens)
    return (op[1], left, right)