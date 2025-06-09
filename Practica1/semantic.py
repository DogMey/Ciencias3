def semantic_analyze(ast, symbol_table=None):
    print(f"DEBUG: symbol_table RECIBIDO (antes de verificar): {symbol_table}")  # DEBUG TEMPORAL
    if symbol_table is None or not isinstance(symbol_table, dict):
        symbol_table = {}  # Solo crear nuevo si no se pasa uno

    print(f"DEBUG: symbol_table inicial: {symbol_table}")  # DEBUG

    for node in ast:
        node_type = node[0]
        print(f"DEBUG: Procesando nodo: {node}")  # DEBUG

        if node_type == "DECLARATION":
            handle_declaration(node, symbol_table)
            print(f"DEBUG: Después de DECLARATION, symbol_table: {symbol_table}")  # DEBUG
        elif node_type == "ASSIGNMENT":
            handle_assignment(node, symbol_table)
        elif node_type == "CALL":
            handle_call(node, symbol_table)
        elif node_type == "IF":
            print(f"DEBUG: Antes de IF, symbol_table: {symbol_table}")  # DEBUG
            handle_if_statement(node, symbol_table)
        elif node_type == "WHILE":
            handle_while_statement(node, symbol_table)
        elif node_type == "FOR":
            handle_for_statement(node, symbol_table)
        # Puedes agregar más casos aquí

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
        # Si el argumento es una expresión, podrías evaluarla aquí

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
        
        # Operadores de comparación retornan bool
        if op in ('>', '<', '>=', '<=', '==', '!='):
            left_type = eval_expression_type(expr[1], symbol_table)
            right_type = eval_expression_type(expr[2], symbol_table)
            
            # Verificar que los tipos sean comparables
            if not types_comparable(left_type, right_type):
                raise Exception(f"Error semántico: no se pueden comparar tipos '{left_type}' y '{right_type}'.")
            
            return 'bool'
        
        # Operadores lógicos
        if op in ('&&', '||', 'AND', 'OR'):
            left_type = eval_expression_type(expr[1], symbol_table)
            right_type = eval_expression_type(expr[2], symbol_table)
            
            if not is_boolean_expression(expr[1], left_type):
                raise Exception(f"Error semántico: operando izquierdo debe ser booleano en operación '{op}'.")
            if not is_boolean_expression(expr[2], right_type):
                raise Exception(f"Error semántico: operando derecho debe ser booleano en operación '{op}'.")
            
            return 'bool'
        
        # Operador de negación
        if op in ('!', 'NOT'):
            operand_type = eval_expression_type(expr[1], symbol_table)
            if not is_boolean_expression(expr[1], operand_type):
                raise Exception(f"Error semántico: operando debe ser booleano en operación '{op}'.")
            return 'bool'
        
        # Operadores aritméticos (código original)
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
    # Puedes ajustar las reglas según tu lenguaje
    if var_type == expr_type:
        return True
    if var_type == 'float' and expr_type == 'int':
        return True  # Permite asignar int a float
    
    return False

######################## AGREGANDO PARTE DE CONDICIONES Y FLUJO DE CONTROL #################################

def handle_if_statement(node, symbol_table):
    """
    Maneja la validación semántica de una declaración IF
    Estructura esperada: ("IF", condition, then_block, [else_block])
    """
    if len(node) < 3:
        raise Exception("Error semántico: declaración IF malformada.")
    
    condition = node[1]
    then_block = node[2]
    else_block = node[3] if len(node) > 3 else None
    
    # Validar que la condición sea una expresión booleana válida
    condition_type = eval_expression_type(condition, symbol_table)
    if not is_boolean_expression(condition, condition_type):
        raise Exception(f"Error semántico: la condición del IF debe ser una expresión booleana, se encontró '{condition_type}'.")
    
    # Validar el bloque then reutilizando semantic_analyze
    if isinstance(then_block, list):
        print(f"DEBUG: Pasando symbol_table a semantic_analyze: {symbol_table}")  # DEBUG
        semantic_analyze(then_block)
    
    # Validar el bloque else si existe
    if else_block and isinstance(else_block, list):
        semantic_analyze(else_block)

def handle_while_statement(node, symbol_table):
    """
    Maneja la validación semántica de una declaración WHILE
    Estructura esperada: ("WHILE", condition, body_block)
    """
    if len(node) < 3:
        raise Exception("Error semántico: declaración WHILE malformada.")
    
    condition = node[1]
    body_block = node[2]
    
    # Validar que la condición sea una expresión booleana válida
    condition_type = eval_expression_type(condition, symbol_table)
    if not is_boolean_expression(condition, condition_type):
        raise Exception(f"Error semántico: la condición del WHILE debe ser una expresión booleana, se encontró '{condition_type}'.")
    
    # Validar el bloque del cuerpo
    if isinstance(body_block, list):
        semantic_analyze(body_block)

def handle_for_statement(node, symbol_table):
    """
    Maneja la validación semántica de una declaración FOR
    Estructura esperada: ("FOR", init, condition, increment, body_block)
    """
    if len(node) < 5:
        raise Exception("Error semántico: declaración FOR malformada.")
    
    init = node[1]
    condition = node[2]
    increment = node[3]
    body_block = node[4]
    
    # Validar inicialización (puede ser declaración o asignación)
    if init:
        if init[0] == "DECLARATION":
            handle_declaration(init, symbol_table)
        elif init[0] == "ASSIGNMENT":
            handle_assignment(init, symbol_table)
    
    # Validar que la condición sea una expresión booleana válida
    if condition:
        condition_type = eval_expression_type(condition, symbol_table)
        if not is_boolean_expression(condition, condition_type):
            raise Exception(f"Error semántico: la condición del FOR debe ser una expresión booleana, se encontró '{condition_type}'.")
    
    # Validar incremento (normalmente una asignación)
    if increment and increment[0] == "ASSIGNMENT":
        handle_assignment(increment, symbol_table)
    
    # Validar el bloque del cuerpo
    if isinstance(body_block, list):
        semantic_analyze(body_block)

def is_boolean_expression(expr, expr_type):
    """
    Determina si una expresión es válida como condición booleana
    """
    # Tipos directamente booleanos
    if expr_type == 'bool':
        return True
    
    # Si es una operación de comparación, es booleana
    if isinstance(expr, tuple):
        op = expr[0]
        # Operadores de comparación
        if op in ('>', '<', '>=', '<=', '==', '!='):
            return True
        # Operadores lógicos
        if op in ('&&', '||', 'AND', 'OR'):
            return True
        # Operador de negación
        if op in ('!', 'NOT'):
            return True
    
    # Números pueden ser usados como booleanos (0 = false, != 0 = true)
    # Esto depende del lenguaje que estés implementando
    if expr_type in ('int', 'float'):
        return True  # Cambia a False si tu lenguaje no permite esto
    
    # Strings no son válidos como condiciones booleanas por defecto
    if expr_type in ('string', 'char'):
        return False
    
    return False

def types_comparable(type1, type2):
    """
    Determina si dos tipos pueden ser comparados
    """
    # Tipos numéricos son comparables entre sí
    numeric_types = {'int', 'float'}
    if type1 in numeric_types and type2 in numeric_types:
        return True
    
    # Mismo tipo siempre es comparable
    if type1 == type2:
        return True
    
    # Char y string pueden ser comparables dependiendo del lenguaje
    string_types = {'string', 'char'}
    if type1 in string_types and type2 in string_types:
        return True
    
    return False