# Importamos el módulo 're' para trabajar con expresiones regulares
import re

# === DEFINICIÓN DE TOKENS ===

# Cada tupla contiene el nombre del token y su patrón de expresión regular
tokens = [
    ('EQ', r'=='),                      # Token para el operador de igualdad (==)
    ('COMMENT', r'//.*'),               # Token para comentarios de una línea (comienzan con //)
    ('NUM', r'\d+\.\d+|\d+'),           # Token para números: primero decimales, luego enteros
    ('ID', r'[a-zA-Z_]\w*'),            # Token para identificadores: letras o _ seguidos de letras, dígitos o _
    ('OP', r'[+\-*/=]'),                # Token para operadores: +, -, *, /, =
    ('PAREN', r'[()]'),                 # Token para paréntesis: ( y )
    ('BRACE', r'[\{\}]'),               # Token para llaves: { y }
    ('SEMI', r';'),                     # Token para punto y coma ;
    ('WHITESPACE', r'\s+'),             # Token para espacios, tabulaciones y saltos de línea
]

# === ANALIZADOR LÉXICO ===
def analizador_lexico(codigo):
    pos = 0             # Posición actual dentro del texto fuente
    resultado = []      # Lista donde se almacenarán los tokens encontrados

    # Mientras no se haya recorrido todo el código fuente...
    while pos < len(codigo):
        match = None    # Se inicializa la variable de coincidencia

        # Iteramos sobre cada tipo de token y su expresión regular
        for token_type, pattern in tokens:
            regex = re.compile(pattern)         # Compilamos la expresión regular
            match = regex.match(codigo, pos)    # Buscamos coincidencia desde la posición actual

            if match:
                text = match.group(0)           # Extraemos el texto que coincidió con el patrón

                # Ignoramos los espacios en blanco y los comentarios
                if token_type not in ('WHITESPACE', 'COMMENT'):
                    resultado.append((token_type, text))    # Agregamos el token a la lista

                pos = match.end()               # Avanzamos la posición hasta el final del match
                break                           # Ya se encontró un token, no se buscan más en este punto

        if not match:
            # Si no se reconoció ningún patrón, se lanza un error de sintaxis
            raise SyntaxError(f"Token no reconocido en posición {pos}")

    return resultado    # Devolvemos la lista completa de tokens encontrados

# === ANALIZADOR SINTÁCTICO  ===

def analizador_sintactico(tokens):  # tokens: lista de tuplas (tipo, valor)
    tokens = tokens.copy()
    sentencias = []
    while tokens:
        sentencias.append(parse_sentencia(tokens))
    return sentencias #Devuelve lista de sentencias parseadas (declaraciones o asignaciones).

def parse_sentencia(tokens):    # Decide si es declaración o asignación según el primer token.
    # Si viene un tipo ('int' o 'float' etiquetado como ID), es declaración
    if tokens[0][0] == 'ID' and tokens[0][1] in ('int', 'float'):
        return parse_declaracion(tokens)
    # Si viene un identificador distinto, es asignación
    if tokens[0][0] == 'ID':
        return parse_asignacion(tokens)
    raise SyntaxError(f"Sentencia inválida, token inesperado: {tokens[0]}")

def parse_declaracion(tokens):  # Declaracion ::= tipo ID '=' expresion ';'
    tipo = parse_tipo(tokens)
    identificador = parse_id(tokens)
    parse_equals(tokens)
    expr = parse_expresion(tokens)
    parse_semi(tokens)
    return ('DECLARACION', tipo, identificador, expr)

def parse_asignacion(tokens):
    """
    asignacion ::= ID '=' expresion ';'
    """
    identificador = parse_id(tokens)
    parse_equals(tokens)
    expr = parse_expresion(tokens)
    parse_semi(tokens)
    return ('ASIGNACION', identificador, expr)

def parse_tipo(tokens): # Acepta ('ID','int') o ('ID','float') como tipo válido.
    if not tokens:
        raise SyntaxError("Se esperaba un tipo pero no quedan tokens")
    tk_type, tk_val = tokens.pop(0) # Extrae el primer token
    if tk_type == 'ID' and tk_val in ('int', 'float'):
        return tk_val
    raise SyntaxError(f"Tipo no válido: {tk_val}")

def parse_id(tokens):   # Reconoce ('ID', nombre) como identificador.
    if not tokens:
        raise SyntaxError("Se esperaba un identificador pero no quedan tokens")
    tk_type, tk_val = tokens.pop(0)
    if tk_type == 'ID':
        return tk_val
    raise SyntaxError(f"Identificador no válido: {tk_val}")

def parse_num(tokens):  # Reconoce ('NUM', valor) como número.
    if not tokens:
        raise SyntaxError("Se esperaba un número pero no quedan tokens")
    tk_type, tk_val = tokens.pop(0) # Extrae el primer token
    if tk_type == 'NUM':
        return float(tk_val) if '.' in tk_val else int(tk_val)
    raise SyntaxError(f"Número no válido: {tk_val}")

def parse_equals(tokens):   # Verifica que haya un ('OP','=')
    if not tokens:
        raise SyntaxError("Se esperaba '=' pero no quedan tokens")
    tk_type, tk_val = tokens.pop(0) # Extrae el primer token
    if not (tk_type == 'OP' and tk_val == '='):
        raise SyntaxError(f"Se esperaba '=' pero se encontró {tk_val}")

def parse_semi(tokens): # Verifica que haya un ('SEMI',';')
    if not tokens:
        raise SyntaxError("Se esperaba ';' pero no quedan tokens")
    tk_type, tk_val = tokens.pop(0) # Extrae el primer token
    if tk_type != 'SEMI':
        raise SyntaxError(f"Se esperaba ';' pero se encontró {tk_val}")

def parse_expresion(tokens):    # Expresión simple: elemento seguido de cero o más operaciones binarias.
    """
    elemento ::= ID | NUM
    expresion ::= elemento (OP elemento)*
    """
    # Se va a construir un árbol de sintaxis abstracta (AST) para la expresión
    if not tokens:
        raise SyntaxError("Expresión vacía")
    # Primer elemento
    if tokens[0][0] == 'NUM':
        nodo = parse_num(tokens)
    elif tokens[0][0] == 'ID':
        nodo = parse_id(tokens)
    else:
        raise SyntaxError(f"Expresión no válida, se encontró {tokens[0][1]}")

    # Operadores binarios
    while tokens and tokens[0][0] == 'OP' and tokens[0][1] in ('+', '-', '*', '/'):
        op = tokens.pop(0)[1]
        # Siguiente elemento
        if not tokens:
            raise SyntaxError("Falta operando después del operador")
        if tokens[0][0] == 'NUM':
            rhs = parse_num(tokens)
        elif tokens[0][0] == 'ID':
            rhs = parse_id(tokens)
        else:
            raise SyntaxError(f"Operando inválido: {tokens[0][1]}")
        nodo = (op, nodo, rhs)

    return nodo


# === BLOQUE DE PRUEBA ===

if __name__ == "__main__":
    codigo = """
    // Comentario
    int a = 10;
    int b = a + 5;
    c = a + 1;
    int f = 2;
    
    """

    print("=== ANÁLISIS LÉXICO ===")
    tokens = analizador_lexico(codigo)
    for t in tokens:
        print(t)

    print("\n=== ANÁLISIS SINTÁCTICO ===")
    try:
        ast = analizador_sintactico(tokens)
        for sentencia in ast:
            print(sentencia)
    except SyntaxError as e:
        print("Error de sintaxis:", e)
