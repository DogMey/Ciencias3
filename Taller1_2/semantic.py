scope_stack = []  # Pila de ámbitos
symbol_table = {}  # Tabla general de símbolos por ámbito

def enter_scope(name):
    scope_stack.append(name)
    symbol_table[name] = {}

def exit_scope():
    scope_stack.pop()

def current_scope():
    return scope_stack[-1] if scope_stack else None

def semantic_analyze(ast, usage_table=None):
    global symbol_table
    if usage_table is None:
        usage_table = {}

    # Inicia ámbito global
    if not scope_stack:
        enter_scope("global")

    for node in ast:
        node_type = node[0]

        if node_type == "DECLARATION":
            handle_declaration(node, usage_table)
        elif node_type == "ASSIGNMENT":
            handle_assignment(node, usage_table)
        elif node_type == "CALL":
            handle_call(node, usage_table)
        elif node_type == "IF":
            handle_if_statement(node, usage_table)
        elif node_type == "WHILE":
            handle_while_statement(node, usage_table)
        elif node_type == "FOR":
            handle_for_statement(node, usage_table)
        elif node_type == "CONST_DECLARATION":
            handle_const_declaration(node, usage_table)

    if current_scope() == "global":
        for scope in symbol_table:
            for var in symbol_table[scope]:
                if usage_table.get(var, 0) == 0:
                    raise Exception(f"Advertencia: la variable '{var}' fue declarada pero nunca utilizada.")

    return True

def declare_variable(name, vtype, usage_table):
    scope = current_scope()
    table = symbol_table[scope]
    if name in table:
        print(f"Warning: ‘{name}’ shadows a name in scope ‘{scope}’")
    table[name] = vtype
    usage_table[name] = 0

def resolve_variable(name):
    for scope in reversed(scope_stack):
        table = symbol_table[scope]
        if name in table:
            return table[name]
    return None

def handle_declaration(node, usage_table):
    var_type = node[1]
    var_name = node[2]
    if resolve_variable(var_name) and var_name in symbol_table[current_scope()]:
        raise Exception(f"Error semántico: la variable '{var_name}' ya fue declarada.")
    if len(node) > 3:
        expr = node[3]
        expr_type = eval_expression_type(expr)
        if not types_compatible(var_type, expr_type):
            raise Exception(f"Error semántico: no se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")
    declare_variable(var_name, var_type, usage_table)

def handle_const_declaration(node, usage_table):
    const_name = node[1]
    expr = node[2]
    if resolve_variable(const_name) and const_name in symbol_table[current_scope()]:
        raise Exception(f"Error semántico: no se puede modificar la constante '{const_name}'.")
    expr_type = eval_expression_type(expr)
    symbol_table[current_scope()][const_name] = {'type': expr_type, 'const': True}
    usage_table[const_name] = 0

def handle_assignment(node, usage_table):
    var_name = node[1]
    entry = resolve_variable(var_name)
    if not entry:
        raise Exception(f"Error semántico: la variable '{var_name}' no ha sido declarada.")
    var_type = entry['type'] if isinstance(entry, dict) else entry
    if isinstance(entry, dict) and entry.get('const', False):
        raise Exception(f"Error semántico: no se puede modificar la constante '{var_name}'.")
    expr = node[2]
    expr_type = eval_expression_type(expr)
    if not types_compatible(var_type, expr_type):
        raise Exception(f"Error semántico: no se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")
    usage_table[var_name] = usage_table.get(var_name, 0) + 1

def handle_call(node, usage_table):
    func_name = node[1]
    arguments = node[2] if len(node) > 2 else []
    for arg in arguments:
        if isinstance(arg, str):
            if resolve_variable(arg):
                usage_table[arg] = usage_table.get(arg, 0) + 1
            else:
                raise Exception(f"Error semántico: la variable '{arg}' no ha sido declarada.")

def eval_expression_type(expr):
    if isinstance(expr, int):
        return 'int'
    if isinstance(expr, float):
        return 'float'
    if isinstance(expr, str):
        if expr.startswith('"') and expr.endswith('"'):
            return 'string'
        if expr.startswith("'") and expr.endswith("'"):
            return 'char'
        val = resolve_variable(expr)
        return val['type'] if isinstance(val, dict) else val if val else 'unknown'
    if isinstance(expr, tuple):
        op = expr[0]
        if op == 'CAST':
            cast_type = expr[1]
            inner_type = eval_expression_type(expr[2])
            if cast_type in ['int', 'float'] and inner_type == 'string':
                return cast_type
            raise Exception(f"Error semántico: conversión inválida de '{inner_type}' a '{cast_type}'.")
        if op in ('>', '<', '>=', '<=', '==', '!='):
            lt = eval_expression_type(expr[1])
            rt = eval_expression_type(expr[2])
            if not types_comparable(lt, rt):
                raise Exception(f"Error semántico: no se pueden comparar tipos '{lt}' y '{rt}'.")
            return 'bool'
        if op in ('&&', '||', 'AND', 'OR'):
            lt = eval_expression_type(expr[1])
            rt = eval_expression_type(expr[2])
            if not is_boolean_expression(expr[1], lt) or not is_boolean_expression(expr[2], rt):
                raise Exception("Error semántico: operandos no booleanos en operación lógica.")
            return 'bool'
        if op in ('!', 'NOT'):
            operand_type = eval_expression_type(expr[1])
            if not is_boolean_expression(expr[1], operand_type):
                raise Exception(f"Error semántico: el operador '!' solo puede aplicarse a valores booleanos, se encontró '{operand_type}'.")
            return 'bool'
        if op in ('+', '-', '*', '/'):
            lt = eval_expression_type(expr[1])
            rt = eval_expression_type(expr[2])
            if (lt == 'string' and rt in ('int', 'float')) or (rt == 'string' and lt in ('int', 'float')):
                raise Exception("Error semántico: no se puede operar entre 'string' y tipo numérico sin conversión explícita.")
            if lt == 'string' or rt == 'string':
                return 'string'
            if lt == 'float' or rt == 'float':
                return 'float'
            if lt == 'int' and rt == 'int':
                return 'int'
            return 'unknown'
    return 'unknown'

def types_compatible(var_type, expr_type):
    return var_type == expr_type or (var_type == 'float' and expr_type == 'int')

def types_comparable(type1, type2):
    numeric = {'int', 'float'}
    if type1 in numeric and type2 in numeric:
        return True
    if type1 == type2:
        return True
    if type1 in {'string', 'char'} and type2 in {'string', 'char'}:
        return True
    return False

def is_boolean_expression(expr, expr_type):
    if expr_type == 'bool':
        return True
    if isinstance(expr, tuple) and expr[0] in ('>', '<', '>=', '<=', '==', '!=', '&&', '||', 'AND', 'OR', '!', 'NOT'):
        return True
    return expr_type in ('int', 'float')

def handle_if_statement(node, usage_table):
    condition = node[1]
    then_block = node[2]
    else_block = node[3] if len(node) > 3 else None

    condition_type = eval_expression_type(condition)
    if not is_boolean_expression(condition, condition_type):
        raise Exception(f"Error semántico: la condición del IF debe ser una expresión booleana, se encontró '{condition_type}'.")

    enter_scope("if")
    semantic_analyze(then_block, usage_table)
    exit_scope()

    if else_block:
        enter_scope("else")
        semantic_analyze(else_block, usage_table)
        exit_scope()

def handle_while_statement(node, usage_table):
    condition = node[1]
    body_block = node[2]

    condition_type = eval_expression_type(condition)
    if not is_boolean_expression(condition, condition_type):
        raise Exception(f"Error semántico: la condición del WHILE debe ser una expresión booleana, se encontró '{condition_type}'.")

    enter_scope("while")
    semantic_analyze(body_block, usage_table)
    exit_scope()

def handle_for_statement(node, usage_table):
    init = node[1]
    condition = node[2]
    increment = node[3]
    body_block = node[4]

    enter_scope("for")
    if init:
        if init[0] == "DECLARATION":
            handle_declaration(init, usage_table)
        elif init[0] == "ASSIGNMENT":
            handle_assignment(init, usage_table)

    if condition:
        cond_type = eval_expression_type(condition)
        if not is_boolean_expression(condition, cond_type):
            raise Exception(f"Error semántico: la condición del FOR debe ser una expresión booleana, se encontró '{cond_type}'.")

    if increment and increment[0] == "ASSIGNMENT":
        handle_assignment(increment, usage_table)

    semantic_analyze(body_block, usage_table)
    exit_scope()
