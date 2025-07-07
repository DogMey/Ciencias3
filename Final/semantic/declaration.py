from semantic.scopes import ScopeStack

def check_declaration(node, scopes):
    tipo, nombre = node[1], node[2]
    scopes.declare(nombre, tipo)
