# Inferencia de tipo simple para enteros, identificadores y operaciones aritméticas

def infer_type(expr, scopes):
    if isinstance(expr, int):
        return 'int'
    if isinstance(expr, str):
        # Puede ser un identificador
        if scopes.is_declared(expr):
            return scopes.get_type(expr)
        # Si no está declarado, no se puede inferir
        return None
    if isinstance(expr, tuple):
        op = expr[0]
        # Operaciones aritméticas binarias
        if op in {'+', '-', '*', '/'}:
            t1 = infer_type(expr[1], scopes)
            t2 = infer_type(expr[2], scopes)
            if t1 == t2:
                return t1
            return None
    return None
