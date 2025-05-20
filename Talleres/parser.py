# === ANALIZADOR SINTÁCTICO (Parser) ===

def parser(tokens):
    """
    Función principal del parser.
    Recibe una lista de tokens (tuplas de tipo y valor) y devuelve el árbol de sintaxis abstracta (AST).
    """
    tokens = tokens.copy()  # Copia para no modificar la lista original
    ast = []  # AST: lista de sentencias analizadas

    # Mientras haya tokens por analizar, procesa una sentencia
    while tokens:
        ast.append(parse_statement(tokens))  # Agrega el resultado del análisis al AST
    return ast


def parse_statement(tokens):
    """
    Determina si una sentencia es una declaración o una asignación.
    """
    # Declaración si el primer token es un tipo válido (int o float)
    if tokens[0][0] == 'IDENTIFIER' and tokens[0][1] in ('int', 'float'):
        return parse_declaration(tokens)
    # Asignación si el primer token es un identificador de variable
    if tokens[0][0] == 'IDENTIFIER':
        return parse_assignment(tokens)
    
    # Si no es ninguna de las anteriores, lanza error de sintaxis
    raise SyntaxError(f"Sentencia inválida. Token inesperado: {tokens[0]}")


def parse_declaration(tokens):
    """
    Analiza una declaración de variable.
    Forma esperada: tipo ID '=' expresión ';'
    """
    tipo = parse_type(tokens)            # Tipo: int o float
    identificador = parse_id(tokens)     # Nombre de la variable
    parse_equals(tokens)                 # Verifica que siga un '='
    expr = parse_expression(tokens)      # Expresión a asignar
    parse_semi(tokens)                   # Verifica que termine con ';'
    return ('DECLARATION', tipo, identificador, expr)  # Nodo del AST


def parse_assignment(tokens):
    """
    Analiza una asignación de variable.
    Forma esperada: ID '=' expresión ';'
    """
    identificador = parse_id(tokens)     # Nombre de la variable
    parse_equals(tokens)                 # Verifica que siga un '='
    expr = parse_expression(tokens)      # Expresión a asignar
    parse_semi(tokens)                   # Verifica que termine con ';'
    return ('ASSIGNMENT', identificador, expr)  # Nodo del AST


def parse_type(tokens):
    """
    Extrae y verifica el tipo de dato ('int' o 'float').
    """
    if not tokens:
        raise SyntaxError("Se esperaba un tipo, pero no hay más tokens.")
    tk_type, tk_val = tokens.pop(0)
    if tk_type == 'IDENTIFIER' and tk_val in ('int', 'float'):
        return tk_val
    raise SyntaxError(f"Tipo inválido: {tk_val}")


def parse_id(tokens):
    """
    Extrae y verifica un identificador (nombre de variable).
    """
    if not tokens:
        raise SyntaxError("Se esperaba un identificador, pero no hay más tokens.")
    tk_type, tk_val = tokens.pop(0)
    if tk_type == 'IDENTIFIER':
        return tk_val
    raise SyntaxError(f"Identificador inválido: {tk_val}")


def parse_num(tokens):
    """
    Extrae y convierte un número (int o float).
    """
    if not tokens:
        raise SyntaxError("Se esperaba un número, pero no hay más tokens.")
    tk_type, tk_val = tokens.pop(0)
    if tk_type == 'NUMBER':
        return float(tk_val) if '.' in tk_val else int(tk_val)  # Convierte a float si tiene punto decimal
    raise SyntaxError(f"Número inválido: {tk_val}")


def parse_equals(tokens):
    """
    Verifica que el siguiente token sea el operador de asignación '='.
    """
    if not tokens:
        raise SyntaxError("Se esperaba '=' pero no hay más tokens.")
    tk_type, tk_val = tokens.pop(0)
    if not (tk_type == 'OPERATOR' and tk_val == '='):
        raise SyntaxError(f"Se esperaba '=' pero se encontró {tk_val}")


def parse_semi(tokens):
    """
    Verifica que el siguiente token sea un punto y coma ';'.
    """
    if not tokens:
        raise SyntaxError("Se esperaba ';' pero no hay más tokens.")
    tk_type, tk_val = tokens.pop(0)
    if tk_type != 'SEMICOLON':
        raise SyntaxError(f"Se esperaba ';' pero se encontró {tk_val}")


def parse_expression(tokens):
    """
    Analiza una expresión aritmética simple:
    elemento (OP elemento)*
    Donde elemento puede ser un número o un identificador.
    """
    if not tokens:
        raise SyntaxError("Expresión vacía.")

    # Parsea el primer operando: número o identificador
    if tokens[0][0] == 'NUMBER':
        node = parse_num(tokens)
    elif tokens[0][0] == 'IDENTIFIER':
        node = parse_id(tokens)
    else:
        raise SyntaxError(f"Expresión inválida. Se encontró {tokens[0][1]}")

    # Parsea el resto de la expresión (operador + operando)
    while tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] in ('+', '-', '*', '/'):
        op = tokens.pop(0)[1]  # Extrae el operador

        # Verifica que haya otro operando válido
        if not tokens:
            raise SyntaxError("Falta operando después del operador.")

        # Extrae el siguiente operando: número o identificador
        if tokens[0][0] == 'NUMBER':
            rhs = parse_num(tokens)
        elif tokens[0][0] == 'IDENTIFIER':
            rhs = parse_id(tokens)
        else:
            raise SyntaxError(f"Operando inválido: {tokens[0][1]}")
        
        # Crea un nodo de expresión binaria: (operador, izquierdo, derecho)
        node = (op, node, rhs)

    return node  # Retorna el nodo final de la expresión
