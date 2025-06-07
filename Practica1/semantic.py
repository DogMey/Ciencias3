import lexer, parser, tester

symbol_table = {}

def evaluate_expression(expression, symbol_table):
    if isinstance(expression, int):
        return "int"
    elif isinstance(expression, str):
        if expression in symbol_table:
            return symbol_table[expression]
        else:
            raise NameError(f"Variable '{expression}' no definida")
    elif isinstance(expression, list):
        # Asumimos que es una expresión compuesta
        return "composite"
    else:
        raise TypeError("Tipo de expresión no soportado")

def semantic_analyze(ast):
    symbol_table = {}
    for node in ast:
        node_type = node[0]
        if node_type == "ASSIGNMENT":
            variable_name = node[1]
            expression = node[2]
            value_type = evaluate_expression(expression, symbol_table)
            symbol_table[variable_name] = value_type