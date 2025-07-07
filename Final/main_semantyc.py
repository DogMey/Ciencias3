# main_semantyc.py
# Analizador semántico básico modularizado


from semantic.scopes import ScopeStack
from semantic.declaration import check_declaration
from semantic.assignment import check_assignment
from semantic.type_inference import infer_type
from semantic.ifblock import check_ifblock
from semantic.whileblock import check_whileblock

def semantic_analyze(ast):
    scopes = ScopeStack()
    def analyze_node(node, scopes):
        node_type = node[0]
        if node_type == 'DECLARATION':
            check_declaration(node, scopes)
        elif node_type == 'ASSIGNMENT':
            check_assignment(node, scopes, infer_type)
        elif node_type == 'IF':
            check_ifblock(node, scopes, analyze_node)
        elif node_type == 'WHILE':
            check_whileblock(node, scopes, analyze_node)

    for node in ast:
        analyze_node(node, scopes)
    return True