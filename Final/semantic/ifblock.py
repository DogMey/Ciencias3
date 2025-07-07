def check_ifblock(node, scopes, analyze_node):
    # node = ("IF", condicion, cuerpo)
    condicion = node[1]
    cuerpo = node[2]
    # Se puede agregar verificación de tipo de la condición si se desea
    scopes.enter_scope_if()
    for stmt in cuerpo:
        analyze_node(stmt, scopes)
    scopes.exit_scope()
