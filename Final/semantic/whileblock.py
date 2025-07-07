def check_whileblock(node, scopes, analyze_node):
    # node = ("WHILE", condicion, cuerpo)
    condicion = node[1]
    cuerpo = node[2]
    # Se puede agregar verificación de tipo de la condición si se desea
    scopes.enter_scope_while()
    for stmt in cuerpo:
        analyze_node(stmt, scopes)
    scopes.exit_scope()
