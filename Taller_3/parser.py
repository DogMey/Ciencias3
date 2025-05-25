# === ANALIZADOR SINTÁCTICO (Parser) ===

def parser(tokens):
    """
    Función principal del parser.
    Recibe una lista de tokens (tuplas de tipo y valor) y devuelve el árbol de sintaxis abstracta (AST).
    """

    # Convertir tokens del formato del lexer a formato interno manteniendo info de línea
    if tokens and isinstance(tokens[0], dict):
        # Si vienen como diccionarios del nuevo lexer, convertir manteniendo línea
        formatted_tokens = []
        for token in tokens:
            formatted_tokens.append((token['type'], token['value'], token['line']))
        tokens = formatted_tokens
    else:
        # Si vienen como tuplas simples, agregar línea por defecto
        tokens = [(t[0], t[1], 1) for t in tokens]

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
    if not tokens:
        raise SyntaxError("Se esperaba una sentencia pero no hay más tokens.")
    # Declaración si el primer token es un tipo válido (int o float)
    if tokens[0][0] == 'IDENTIFIER' and tokens[0][1] in ('int', 'float'):
        return parse_declaration(tokens)
    if tokens[0][0] == 'IDENTIFIER' and tokens[0][1] == 'if':
        return parse_if(tokens)
    # Asignación si el primer token es un identificador de variable
    if tokens[0][0] == 'IDENTIFIER':
        return parse_assignment(tokens)
    
    # Si no es ninguna de las anteriores, lanza error de sintaxis con línea
    line = tokens[0][2] if len(tokens[0]) > 2 else 1
    raise SyntaxError(f"Sentencia inválida en la línea {line}. Token inesperado: {tokens[0][1]}")


def parse_declaration(tokens):
    """
    Analiza una declaración de variable.
    Formatos válidos:
      - tipo ID '=' expresión ';'
      - tipo ID ';'
    """
    tipo = parse_type(tokens)            # Tipo: int o float
    identificador = parse_id(tokens)     # Nombre de la variable

    # Si sigue un '=', se parsea la expresión
    if tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] == '=':
        parse_equals(tokens)
        expr = parse_expression(tokens)
        parse_semi(tokens)
        return ('DECLARATION', tipo, identificador, expr)
    
    # Si no, solo espera el ';'
    parse_semi(tokens)
    return ('DECLARATION', tipo, identificador)


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
    return consume(tokens, 'IDENTIFIER')


def parse_num(tokens):
    """
    Extrae y convierte un número (int o float).
    """
    number = consume(tokens, 'NUMBER')
    return float(number) if '.' in number else int(number)


def parse_equals(tokens):
    """
    Verifica que el siguiente token sea el operador de asignación '='.
    """
    consume(tokens, 'OPERATOR', '=')


def parse_semi(tokens):
    """
    Verifica que el siguiente token sea un punto y coma ';'.
    """
    consume(tokens, 'SEMICOLON')

def parse_expression(tokens):
    """
    Nivel más alto: comparación.
    expression → arith_expr (COMPARISON_OP arith_expr)?
    """
    node = parse_arith_expr(tokens)

    # Comparadores lógicos
    if tokens and tokens[0][0] == 'LOGICOPERATOR' and tokens[0][1] in ('==', '!=', '<', '>', '<=', '>='):
        op = tokens.pop(0)[1]
        right = parse_arith_expr(tokens)
        node = (op, node, right)
    
    return node

def parse_arith_expr(tokens):
    """Suma y resta: expr → term ((+|-) term)*"""
    node = parse_term(tokens)
    while tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] in ('+', '-'):
        op = tokens.pop(0)[1]
        right = parse_term(tokens)
        node = (op, node, right)
    return node

def parse_term(tokens):
    """
    Multiplicación y división.
    term → factor ((*|/) factor)*
    """
    node = parse_factor(tokens)
    while tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] in ('*', '/'):
        op = tokens.pop(0)[1]
        right = parse_factor(tokens)
        node = (op, node, right)
    return node

def parse_factor(tokens):
    """
    Un número, un identificador o una expresión entre paréntesis.
    factor → NUMBER | IDENTIFIER | (expression)
    """
    if not tokens:
        raise SyntaxError("Expresión incompleta.")
    
    tk_type, tk_val = tokens[0][:2]
    tk_line = tokens[0][2] if len(tokens[0]) > 2 else 1

    if tk_type == 'NUMBER':
        return parse_num(tokens)
    elif tk_type == 'IDENTIFIER':
        return parse_id(tokens)
    elif tk_type == 'LPAREN':
        tokens.pop(0)  # Consume '('
        expr = parse_expression(tokens)
        if not tokens or tokens[0][0] != 'RPAREN':
            current_line = tokens[0][2] if tokens and len(tokens[0]) > 2 else tk_line
            raise SyntaxError(f"Error de sintaxis en la línea {current_line}: Se esperaba ')' al cerrar la expresión.")
        tokens.pop(0)  # Consume ')'
        return expr
    else:
        raise SyntaxError(f"Elemento inesperado en la expresión: {tk_val}")

def parse_if(tokens):
    """
    Parsea una estructura if (condición) { bloque } [else { bloque }]
    """
    tk_type, tk_val, tk_line = tokens.pop(0)[:3] if len(tokens[0]) > 2 else (*tokens.pop(0), 1)
    if tk_type != 'IDENTIFIER' or tk_val != 'if':
        raise SyntaxError(f"Error de sintaxis en la línea {tk_line}: Se esperaba 'if'.")

    if not tokens or tokens[0][0] != 'LPAREN':
        current_line = tokens[0][2] if tokens and len(tokens[0]) > 2 else tk_line
        raise SyntaxError(f"Error de sintaxis en la línea {current_line}: Se esperaba '(' después de 'if'.")
    tokens.pop(0)  # Consume '('

    condition = parse_expression(tokens)  # Parsea condición lógica

    if not tokens or tokens[0][0] != 'RPAREN':
        current_line = tokens[0][2] if tokens and len(tokens[0]) > 2 else tk_line
        raise SyntaxError(f"Error de sintaxis en la línea {current_line}: Se esperaba ')' después de la condición.")
    tokens.pop(0)  # Consume ')'

    if not tokens or tokens[0][0] != 'LBRACE':
        current_line = tokens[0][2] if tokens and len(tokens[0]) > 2 else tk_line
        raise SyntaxError(f"Error de sintaxis en la línea {current_line}: Se esperaba '{{' para abrir el bloque.")
    tokens.pop(0)  # Consume '{'

    if_body = []
    while tokens and tokens[0][0] != 'RBRACE':
        if_body.append(parse_statement(tokens))

    if not tokens or tokens[0][0] != 'RBRACE':
        raise SyntaxError(f"Error de sintaxis: Se esperaba '}}' al final del bloque 'if'.")
    tokens.pop(0)  # Consume '}'

    # Bloque opcional 'else'
    else_body = None
    if tokens and tokens[0][0] == 'IDENTIFIER' and tokens[0][1] == 'else':
        tokens.pop(0)  # Consume 'else'

        if not tokens or tokens[0][0] != 'LBRACE':
            current_line = tokens[0][2] if tokens and len(tokens[0]) > 2 else 1
            raise SyntaxError(f"Error de sintaxis en la línea {current_line}: Se esperaba '{{' para abrir el bloque 'else'.")
        tokens.pop(0)  # Consume '{'

        else_body = []
        while tokens and tokens[0][0] != 'RBRACE':
            else_body.append(parse_statement(tokens))

        if not tokens or tokens[0][0] != 'RBRACE':
            raise SyntaxError("Error de sintaxis: Se esperaba '}' al final del bloque 'else'.")
        tokens.pop(0)  # Consume '}'

    return ('IF', condition, if_body, else_body)

def consume(tokens, expected_type, expected_value=None):
    if not tokens:
        raise SyntaxError(f"Se esperaba {expected_type} pero no hay más tokens.")
    
    # Extraer información del token incluyendo línea si está disponible
    tk_type = tokens[0][0]
    tk_val = tokens[0][1]
    tk_line = tokens[0][2] if len(tokens[0]) > 2 else 1
    
    token = tokens.pop(0) # Consume el token actual----------
    
    if tk_type != expected_type or (expected_value is not None and tk_val != expected_value):
        expected_str = f"{expected_type}"
        if expected_value:
            expected_str += f" '{expected_value}'"
        raise SyntaxError(f"Error de sintaxis en la línea {tk_line}: Se esperaba {expected_str} pero se encontró {tk_type} '{tk_val}'")
    return tk_val