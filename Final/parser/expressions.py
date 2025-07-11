from .utils import match, expect

def parse_expression(tokens):
    # Expresión de suma/resta
    node = parse_term(tokens)
    while tokens and match(tokens, 'OPERATOR') and tokens[0][1] in ('+', '-'):
        op = tokens.pop(0)[1]
        right = parse_term(tokens)
        node = (op, node, right)
    return node

def parse_term(tokens):
    # Expresión de multiplicación/división
    node = parse_factor(tokens)
    while tokens and match(tokens, 'OPERATOR') and tokens[0][1] in ('*', '/'):
        op = tokens.pop(0)[1]
        right = parse_factor(tokens)
        node = (op, node, right)
    return node

def parse_factor(tokens):
    # Números, identificadores, paréntesis, llamadas a función, literales booleanos
    if match(tokens, 'NUMBER'):
        value = tokens.pop(0)[1]
        return float(value) if '.' in value else int(value)
    elif match(tokens, 'KEYWORD') and tokens[0][1] in ('true', 'false'):
        # Literal booleano
        return tokens.pop(0)[1]
    elif match(tokens, 'IDENTIFIER'):
        # Verificar si es una llamada a función
        if len(tokens) > 1 and tokens[1][0] == 'LPAREN':
            # Es una llamada a función
            func_name = tokens.pop(0)[1]  # Consumir el nombre
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
            return ('FUNC_CALL', func_name, args)
        else:
            # Es un identificador simple
            return tokens.pop(0)[1]
    elif match(tokens, 'LPAREN'):
        expect(tokens, 'LPAREN')
        expr = parse_expression(tokens)
        expect(tokens, 'RPAREN')
        return expr
    elif match(tokens, 'STRING') or match(tokens, 'CHAR'):
        return tokens.pop(0)[1]
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: token inesperado '{val}' en expresión")