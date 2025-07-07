def check_assignment(node, scopes, infer_type):
    nombre = node[1]
    if not scopes.is_declared(nombre):
        raise Exception(f"Variable '{nombre}' no declarada en el ámbito '{scopes.current_scope_name()}'")
    tipo_var = scopes.get_type(nombre)
    valor = node[2]
    tipo_valor = infer_type(valor, scopes)
    if tipo_var != tipo_valor:
        raise Exception(f"Tipos incompatibles en asignación a '{nombre}': {tipo_var} <- {tipo_valor}")
