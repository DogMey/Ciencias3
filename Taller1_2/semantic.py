scope_stack = [] # Pila de ámbitos para manejar el alcance de las variables

def semantic_analyze(ast, symbol_table=None, usage_table=None):
    if symbol_table is None or not isinstance(symbol_table, dict):
        symbol_table = {}  # Solo crear nuevo si no se pasa uno
        scope_stack.clear()  # Limpiar la pila de ámbitos
        scope_stack.append('global')  # Agregar el ámbito global por defecto
        symbol_table = {'global': {}}
    if usage_table is None:
        usage_table = {}
    if "functions" not in symbol_table:
        symbol_table["functions"] = {'print': {'params': [['int', 'float', 'string', 'char', 'bool']], 'return': 'void'}}  # Función print por defecto

    for node in ast:
        node_type = node[0]
        if node_type == "DECLARATION":
            handle_declaration(node, symbol_table, usage_table)
        elif node_type == "ASSIGNMENT":
            handle_assignment(node, symbol_table, usage_table)
        elif node_type == "CALL":
            handle_call(node, symbol_table, usage_table)
        elif node_type == "IF":
            handle_if_statement(node, symbol_table, usage_table)
        elif node_type == "WHILE":
            handle_while_statement(node, symbol_table, usage_table)
        elif node_type == "FOR":
            handle_for_statement(node, symbol_table, usage_table)
        elif node_type == "CONST_DECLARATION":
            handle_const_declaration(node, symbol_table, usage_table)
        elif node_type == "FUNC_DECL":
            handle_function_declaration(node, symbol_table, usage_table)
        elif node_type == "RETURN":
            handle_return(node, symbol_table)

    # Al final, revisa variables no usadas
    for var, count in usage_table.items():
        if count == 0:
            raise Exception(f"Advertencia: la variable '{var}' fue declarada pero nunca utilizada.")

    return True  # Si no hay errores

def handle_declaration(node, symbol_table, usage_table):
    var_type = node[1]
    var_name = node[2]
    # Solo verifica en el scope actual, no en todos
    scope = current_scope()
    if var_name in symbol_table[scope]:
        raise Exception(f"Error semántico: la variable '{var_name}' ya fue declarada en este ámbito.")
    declare_variable(var_name, var_type, symbol_table)
    usage_table[var_name] = 0

def handle_const_declaration(node, symbol_table, usage_table):
    const_name = node[1]
    expr = node[2]
    scope = current_scope()
    if const_name in symbol_table[scope]:
        raise Exception(f"Error semántico: la constante '{const_name}' ya fue declarada en este ámbito.")
    expr_type = eval_expression_type(expr, symbol_table)
    symbol_table[scope][const_name] = {'type': expr_type, 'const': True}
    usage_table[const_name] = 0

def handle_assignment(node, symbol_table, usage_table):
    var_name = node[1]
    entry = lookup_variable(var_name, symbol_table)
    if entry is None:
        raise Exception(f"Error semántico: la variable '{var_name}' no ha sido declarada.")
    # Si es constante, no se puede modificar
    if isinstance(entry, dict) and entry.get('const', False):
        raise Exception(f"Error semántico: no se puede modificar la constante '{var_name}'.")
    var_type = entry['type'] if isinstance(entry, dict) else entry
    expr = node[2]
    expr_type = eval_expression_type(expr, symbol_table)
    if not types_compatible(var_type, expr_type):
        raise Exception(f"Error semántico: no se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")
    usage_table[var_name] = usage_table.get(var_name, 0) + 1


def handle_call(node, symbol_table, usage_table):
    func_name = node[1]
    arguments = node[2] if len(node) > 2 else []
    arg_types = [eval_expression_type(arg, symbol_table) for arg in arguments]
    for arg in arguments:
        if isinstance(arg, str):
            entry = lookup_variable(arg, symbol_table)
            if entry is not None:
                usage_table[arg] = usage_table.get(arg, 0) + 1
            else:
                raise Exception(f"Error semántico: la variable '{arg}' no ha sido declarada.")
    check_function_call(func_name, arg_types, symbol_table)

def declare_function(name, param_types, return_type, symbol_table):
    if name in symbol_table["functions"]:
        raise Exception(f"Función '{name}' ya declarada")
    symbol_table["functions"][name] = {
        "params": param_types,
        "return": return_type
    }

def check_function_call(name, arg_types, symbol_table):
    funcs = symbol_table["functions"]
    if name not in funcs:
        raise Exception(f"Función '{name}' no declarada")
    sig = funcs[name]
    if len(arg_types) != len(sig["params"]):
        raise Exception(f"Aridad incorrecta en '{name}'")
    for i, (a, p) in enumerate(zip(arg_types, sig["params"])):
        # Si el argumento es un dict (constante), extrae el tipo real
        if isinstance(a, dict) and 'type' in a:
            a_type = a['type']
        else:
            a_type = a
        if isinstance(p, list):
            if a_type not in p:
                raise Exception(
                    f"Tipo erróneo en arg {i+1} de '{name}': {a_type} no es uno de {p}"
                )
        else:
            if a_type != p:
                raise Exception(
                    f"Tipo erróneo en arg {i+1} de '{name}': {a_type} ≠ {p}"
                )
    return sig["return"]

def handle_function_declaration(node, symbol_table, usage_table):
    # node = ('FUNCTION_DECL', name, param_list, return_type, body)
    name = node[1]
    param_list = node[2]  # [('int', 'a'), ('float', 'b')]
    return_type = node[3]
    param_types = [ptype for ptype, _ in param_list]
    declare_function(name, param_types, return_type, symbol_table)

    enter_scope(name, symbol_table)  # Crea un nuevo scope para la función
    # Declara los parámetros en el nuevo scope
    for ptype, pname in param_list:
        declare_variable(pname, ptype, symbol_table)
    # Analiza el cuerpo de la función
    body = node[4]
    semantic_analyze(body, symbol_table, usage_table)
    exit_scope()

def handle_return(node, symbol_table):
    # node = ('RETURN', expr)
    expr = node[1]
    # Busca el scope de función más cercano en scope_stack
    func_scope = None
    for scope in reversed(scope_stack):
        if scope in symbol_table["functions"]:
            func_scope = scope
            break
    if func_scope is None:
        raise Exception("Error semántico: 'return' fuera de una función.")
    expected_type = symbol_table["functions"][func_scope]["return"]
    if expr is None:
        return_type = 'void'
    else:
        return_type = eval_expression_type(expr, symbol_table)
    if not types_compatible(expected_type, return_type):
        raise Exception(f"Error semántico: el tipo de retorno '{return_type}' no es compatible con el tipo esperado '{expected_type}' en la función '{func_scope}'.")

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
        entry = lookup_variable(expr, symbol_table)
        if entry is not None:
            if isinstance(entry, dict) and 'type' in entry:
                return entry['type']
            return entry
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
                raise Exception(f"Error semántico: el operador '!' solo puede aplicarse a valores booleanos, se encontró '{operand_type}'.")
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

def handle_if_statement(node, symbol_table, usage_table):
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
        enter_scope("if", symbol_table)
        semantic_analyze(then_block, symbol_table=symbol_table, usage_table=usage_table)
        exit_scope()

    # Validar el bloque else si existe
    if else_block and isinstance(else_block, list):
        enter_scope("else", symbol_table)
        semantic_analyze(else_block, symbol_table=symbol_table, usage_table=usage_table)
        exit_scope()

def handle_while_statement(node, symbol_table, usage_table):
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
        semantic_analyze(body_block, symbol_table=symbol_table, usage_table=usage_table)

def handle_for_statement(node, symbol_table, usage_table):
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
        semantic_analyze(body_block, symbol_table=symbol_table, usage_table=usage_table)

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
    
    # Char y string pueden ser comparables
    string_types = {'string', 'char'}
    if type1 in string_types and type2 in string_types:
        return True
    
    return False

# Manejo de alcance de variables

def enter_scope(name, symbol_table):
    scope_stack.append(name)
    symbol_table[name] = {}

def exit_scope():
    scope_stack.pop()

def current_scope():
    return scope_stack[-1]

def declare_variable(name, vtype, symbol_table):
    scope = current_scope()
    table = symbol_table[scope]
    if name in table:
        print(f"Peligro: '{name}' oculta un nombre en el ámbito '{scope}'")
    table[name] = vtype

def lookup_variable(name, symbol_table):
    # Busca desde el scope más interno hacia el global
    for scope in reversed(scope_stack):
        table = symbol_table[scope]
        if name in table:
            return table[name]
    # Si no se encuentra, busca en el global (fuera de la pila)
    if name in symbol_table:
        return symbol_table[name]
    return None