def semantic_analyze(ast):
    symbol_table = {}  # Ámbito global

    for node in ast:
        node_type = node[0]

        if node_type == "DECLARATION":
            handle_declaration(node, symbol_table)
        elif node_type == "ASSIGNMENT":
            handle_assignment(node, symbol_table)
        elif node_type == "CALL":
            handle_call(node, symbol_table)

    return True  # Si no hay errores

def handle_declaration(node, symbol_table):
    var_type = node[1]
    var_name = node[2]
    if var_name in symbol_table:
        raise Exception(f"Error semántico: la variable '{var_name}' ya fue declarada.")
    # Si hay inicialización, verifica el tipo
    if len(node) > 3:
        expr = node[3]
        expr_type = eval_expression_type(expr, symbol_table)
        if not types_compatible(var_type, expr_type):
            raise Exception(f"Error semántico: no se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")
    symbol_table[var_name] = var_type

def handle_assignment(node, symbol_table):
    var_name = node[1]
    if var_name not in symbol_table:
        raise Exception(f"Error semántico: la variable '{var_name}' no ha sido declarada.")
    var_type = symbol_table[var_name]
    expr = node[2]
    expr_type = eval_expression_type(expr, symbol_table)
    if not types_compatible(var_type, expr_type):
        raise Exception(f"Error semántico: no se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")

def handle_call(node, symbol_table):
    func_name = node[1]
    arguments = node[2] if len(node) > 2 else []
    for arg in arguments:
        if isinstance(arg, str) and arg in symbol_table:
            continue
        elif isinstance(arg, str) and arg not in symbol_table:
            raise Exception(f"Error semántico: la variable '{arg}' no ha sido declarada.")

def eval_expression_type(expr, symbol_table):
    # Si es un número entero
    if isinstance(expr, int):
        return 'int'
    # Si es un número flotante
    if isinstance(expr, float):
        return 'float'
    # Si es un string (cadena)
    if isinstance(expr, str):
        # Si es una variable, busca su tipo
        if expr in symbol_table:
            return symbol_table[expr]
        # Si es un literal string
        if expr.startswith('"') and expr.endswith('"'):
            return 'string'
        if expr.startswith("'") and expr.endswith("'"):
            return 'char'
        # Si no, asume identificador no declarado
        return 'unknown'
    # Si es una operación (tupla: ('+', izq, der), etc.)
    if isinstance(expr, tuple):
        if expr[0] == 'CAST':
            cast_type = expr[1]
            inner_type = eval_expression_type(expr[2], symbol_table)
            # Solo permitimos cast de string a int o float, puedes expandir según tu lenguaje
            if cast_type == 'int' and inner_type == 'string':
                return 'int'
            if cast_type == 'float' and inner_type == 'string':
                return 'float'
            raise Exception(f"Error semántico: conversión inválida de '{inner_type}' a '{cast_type}'.")
        op = expr[0]
        if op in ('+', '-', '*', '/'):
            left_type = eval_expression_type(expr[1], symbol_table)
            right_type = eval_expression_type(expr[2], symbol_table)
            # Si hay una suma entre string y número, es inválido
            if (left_type == 'string' and right_type in ('int', 'float')) or (right_type == 'string' and left_type in ('int', 'float')):
                raise Exception("Error semántico: no se puede operar entre 'string' y tipo numérico sin conversión explícita.")
            if left_type == 'string' or right_type == 'string':
                return 'string'
            if left_type == 'float' or right_type == 'float':
                return 'float'
            if left_type == 'int' and right_type == 'int':
                return 'int'
            return 'unknown'
    return 'unknown'

def types_compatible(var_type, expr_type):
    if var_type == expr_type:
        return True
    if var_type == 'float' and expr_type == 'int':
        return True  # Permite asignar int a float
    return False