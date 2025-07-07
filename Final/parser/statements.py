# statements.py
# Módulo principal para el análisis de sentencias del parser.
# Cada tipo de sentencia se delega a su función específica mediante importaciones locales para evitar ciclos.

def parse_statement(tokens):
    """
    Analiza una sentencia del lenguaje y retorna su representación en el AST.
    Soporta declaraciones, condicionales, bucles, funciones, asignaciones, llamadas a función y return.
    """
    from .utils import match_keyword, match
    # Declaración de variable
    if match_keyword(tokens, 'int') or match_keyword(tokens, 'float'):
        from .declaration import parse_declaration
        return parse_declaration(tokens)
    # Sentencia if
    elif match_keyword(tokens, 'if'):
        from .ifblock import parse_if
        return parse_if(tokens)
    # Bucle for
    elif match_keyword(tokens, 'for'):
        from .forblock import parse_for
        return parse_for(tokens)
    # Bucle while
    elif match_keyword(tokens, 'while'):
        from .whileblock import parse_while
        return parse_while(tokens)
    # Declaración de función
    elif match_keyword(tokens, 'func'):
        from .functions import parse_function_declaration
        return parse_function_declaration(tokens)
    # Sentencia return
    elif match_keyword(tokens, 'return'):
        from .functions import parse_return
        return parse_return(tokens)
    # Asignación o llamada a función
    elif match(tokens, 'IDENTIFIER'):
        # Si el identificador es seguido de '(', es una llamada a función
        if len(tokens) > 1 and tokens[1][0] == 'LPAREN':
            from .functions import parse_function_call
            return parse_function_call(tokens)
        # Si no, es una asignación
        from .assignment import parse_assignment
        return parse_assignment(tokens)
    # Si no coincide con ningún caso, es un error de sintaxis
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: sentencia inválida, token inesperado '{val}'")