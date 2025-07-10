from semantic.scopes import ScopeStack

def check_declaration(node, scopes):
    # node = ("DECLARATION", tipo, nombre, valor)
    tipo, nombre = node[1], node[2]
    
    # Si hay una expresión inicial, validarla antes de declarar la variable
    if len(node) > 3:
        valor = node[3]
        # Verificar que todas las variables usadas en la expresión estén declaradas
        _check_expression_variables(valor, scopes)
    
    # Declarar la variable
    scopes.declare(nombre, tipo)

def _check_expression_variables(expr, scopes):
    """Verifica que todas las variables en una expresión estén declaradas."""
    if isinstance(expr, str):
        # Es un identificador - verificar si no es un literal numérico, booleano o string
        if not expr.isdigit() and not expr.replace('.', '').isdigit() and expr not in ['true', 'false'] and not expr.startswith('"') and not expr.startswith("'"):
            if not scopes.is_declared(expr):
                raise NameError(f"Variable '{expr}' no declarada en el ámbito '{scopes.current_scope_name()}'")
    elif isinstance(expr, tuple):
        # Es una expresión compuesta
        if len(expr) >= 3:
            # Formato: (operador, left, right)
            _check_expression_variables(expr[1], scopes)
            _check_expression_variables(expr[2], scopes)
        elif len(expr) == 2:
            # Formato: (operador, operando)
            _check_expression_variables(expr[1], scopes)
    # Para números e otros literales, no hacer nada
