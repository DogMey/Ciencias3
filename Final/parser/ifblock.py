from .utils import expect, match, parse_condition, match_keyword

def parse_if(tokens):
    expect(tokens, 'KEYWORD', 'if')
    expect(tokens, 'LPAREN')
    condition = parse_condition(tokens)
    expect(tokens, 'RPAREN')
    expect(tokens, 'LBRACE')
    if_block = []
    from .statements import parse_statement  # Importación local para evitar ciclos
    while tokens and not match(tokens, 'RBRACE'):
        if_block.append(parse_statement(tokens))
    if not match(tokens, 'RBRACE'):
        if tokens:
            tipo, val, line, col = tokens[-1]
            raise SyntaxError(f"Error en línea {line}, columna {col}: falta '}}' de cierre en el bloque 'if'")
        else:
            raise SyntaxError("Error: falta '}' de cierre en el bloque 'if', llegó al final del archivo")
    tokens.pop(0)  # Consumir '}'
    
    # Verificar si hay una cláusula else
    else_block = None
    if tokens and match_keyword(tokens, 'else'):
        tokens.pop(0)  # Consumir 'else'
        
        # Verificar si es else if
        if tokens and match_keyword(tokens, 'if'):
            # Es else if, parsear como un nuevo if
            else_block = [parse_if(tokens)]
        else:
            # Es else simple
            expect(tokens, 'LBRACE')
            else_block = []
            while tokens and not match(tokens, 'RBRACE'):
                else_block.append(parse_statement(tokens))
            if not match(tokens, 'RBRACE'):
                if tokens:
                    tipo, val, line, col = tokens[-1]
                    raise SyntaxError(f"Error en línea {line}, columna {col}: falta '}}' de cierre en el bloque 'else'")
                else:
                    raise SyntaxError("Error: falta '}' de cierre en el bloque 'else', llegó al final del archivo")
            tokens.pop(0)  # Consumir '}'
    
    # Retornar el AST con o sin else
    if else_block is not None:
        return ('IF_ELSE', condition, if_block, else_block)
    else:
        return ('IF', condition, if_block)