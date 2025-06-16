# -------------------------------------------------------------
# Analizador Sintáctico para Lenguajes de Programación
# Versión 4.0 - Febrero 1, 2025
# Desarrollado por: Ing. Jonathan Torres, Ph.D.
# -------------------------------------------------------------


# Variable global para la última línea procesada
last_token_line = None

# Función principal que maneja el análisis sintáctico
def parser(tokens):
    global last_token_line  # Acceder a la variable global que guarda la última línea procesada

    tokens = tokens.copy()  # Copiar los tokens para no modificar la lista original
    ast = []  # Lista donde se almacenará el árbol de sintaxis abstracta (AST)

    # Obtenemos la última línea de los tokens para informar sobre el contexto
    last_token = tokens[-1]
    last_token_line = last_token[2]  # Se asume que el tercer elemento de cada token es la línea

    # Procesar todos los tokens, agregando la estructura a 'ast'
    while tokens:
        try:
            stmt = parse_statement(tokens)
            if isinstance(stmt, list):
                ast.extend(stmt)  # Añade cada declaración individualmente
            else:
                ast.append(stmt)
        except SyntaxError as e:  # Si ocurre un error de sintaxis, lo propagamos
            raise SyntaxError(str(e))
    
    return ast  # Retorna el árbol de sintaxis abstracta (AST)

# Función para procesar una sentencia del código
def parse_statement(tokens):
    # Si el primer token es 'int' o 'float', procesamos como declaración
    if match_keyword(tokens, 'int') or match_keyword(tokens, 'float') or match_keyword(tokens, 'string') or match_keyword(tokens, 'char') or match_keyword(tokens, 'bool'):
        return parse_declaration(tokens)

    # Si el primer token es 'if', procesamos una estructura condicional
    elif match_keyword(tokens, 'if'):
        return parse_if(tokens)
    
    # Si el primer token es 'for', procesamos un bucle for
    elif match_keyword(tokens, 'for'):
        return parse_for(tokens)

    # Si el primer token es 'while', procesamos un bucle while
    elif match_keyword(tokens, 'while'):
        return parse_while(tokens)
    
    elif match_keyword(tokens, 'function'):
        return parse_func(tokens)

    # Si el primer token es 'const', procesamos declaración de constante
    elif match_keyword(tokens, 'const'):
        tokens.pop(0)  # Consumir 'const'
        # Espera un identificador para el nombre de la constante
        if not match(tokens, 'IDENTIFIER'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba el nombre de la constante después de 'const', pero se encontró '{val}'")
        const_name = parse_id(tokens)
        # Espera '='
        parse_equals(tokens)
        # Procesa el valor de la constante
        expr = parse_expression(tokens)
        # Espera ';'
        parse_semi(tokens)
        return ('CONST_DECLARATION', const_name, expr)

    # Si el primer token es un identificador, procesamos una asignación
    elif match(tokens, 'IDENTIFIER'):
        # Mejorar el mensaje de error para palabras reservadas mal escritas
        ident = tokens[0][1]
        if ident in ('iff', 'els', 'whle', 'retrun', 'fro', 'foor', 'whille'):  # Se puede ampliar esta lista por errores comunes
            _, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba 'if', pero se encontró '{val}'")
        # Si el siguiente token es LPAREN, es una llamada a función
        if len(tokens) > 1 and tokens[1][0] == 'LPAREN':
            return parse_function_call(tokens)
        # Si no, es una asignación
        return parse_assignment(tokens)
    # Si no es ninguno de los anteriores, es un error de sintaxis
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: sentencia inválida, token inesperado '{val}'")

# Función para procesar una declaración (ejemplo: int a = 5;)
def parse_declaration(tokens):
    tipo = parse_type(tokens)  # Procesa el tipo de la declaración (ej. 'int', 'float')
    declarations = []

    while True:
        ident = parse_id(tokens)  # Procesa el identificador (ej. 'a')

        # Si el siguiente token es un punto y coma, la declaración está completa
        if match(tokens, 'SEMICOLON'):
            declarations.append(('DECLARATION', tipo, ident))
            tokens.pop(0)  # Consumir el token ';'
            break

        # Si es una asignación
        if match(tokens, 'OPERATOR', '='):
            parse_equals(tokens)
            expr = parse_expression(tokens)
            declarations.append(('DECLARATION', tipo, ident, expr))
        else:
            declarations.append(('DECLARATION', tipo, ident))

        # Si hay una coma, seguimos con la siguiente variable
        if match(tokens, 'COMMA'):
            tokens.pop(0)  # Consumir la coma y continuar
            continue

        # Si hay un punto y coma, terminamos la declaración
        if match(tokens, 'SEMICOLON'):
            tokens.pop(0)
            break

        # Si no hay ni coma ni punto y coma, es un error
        if tokens:
            val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ',' o ';' pero se encontró '{val}'")
        else:
            raise SyntaxError("Error: se esperaba ',' o ';' pero no se encontraron más tokens.")

    # Si solo hay una declaración, retorna el elemento, si hay varias, retorna la lista
    return declarations if len(declarations) > 1 else declarations[0]

# Función para procesar una asignación, por ejemplo: 'a = 5'
def parse_assignment(tokens):
    # Procesar el identificador (ej. 'a')
    ident = parse_id(tokens)
    
    # Procesar el operador de asignación ('=')
    parse_equals(tokens)
    
    # Procesar la expresión del lado derecho de la asignación (ej. '5')
    expr = parse_expression(tokens)
    
    # Procesar el punto y coma al final
    parse_semi(tokens)
    
    # Retornar la estructura de la asignación
    return ('ASSIGNMENT', ident, expr)

# Función para procesar una estructura de función 'function'
def parse_func(tokens):

    # Verificamos si el primer token es la palabra clave 'function'
    expect_keyword(tokens, 'function')

    # Guardamos la información de la línea y columna del 'function' para mostrarla en caso de error
    func_line, func_col = tokens[0][2], tokens[0][3]
    #Recuperamos el nombre de la función
    if not match(tokens, 'IDENTIFIER'):
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba nombre de función después de 'function', pero se encontró '{val}'")
    func_name = parse_id(tokens)
    # Espera el paréntesis de apertura '('
    expect(tokens, 'LPAREN')
    params = []  # Lista para almacenar los parámetros de la función
    # Procesa los parámetros de la función
    while not match(tokens, 'RPAREN'):
        # Procesa el tipo del parámetro (ej. 'int', 'float')
        param_type = parse_type(tokens)
        # Procesa el identificador del parámetro
        if not match(tokens, 'IDENTIFIER'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba nombre de parámetro después de '{param_type}', pero se encontró '{val}'")
        param_name = parse_id(tokens)
        params.append((param_type, param_name))
        # Si hay una coma, seguimos con el siguiente parámetro
        if match(tokens, 'COMMA'):
            tokens.pop(0)
            continue
        # Si no hay una coma, esperamos el paréntesis de cierre ')'
        elif match(tokens, 'RPAREN'):
            tokens.pop(0)
            break
        else:
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ',' o ')' pero se encontró '{val}'")
    # Espera la llave de apertura '{'
    expect(tokens, 'LBRACE')
    body = []  # Lista para almacenar el cuerpo de la función
    # Procesa las sentencias dentro del cuerpo de la función
    while tokens and not match(tokens, 'RBRACE'):
        stmt = parse_statement(tokens)
        if isinstance(stmt, list):
            body.extend(stmt)
        else:
            body.append(stmt)
    # Si no hemos encontrado la llave de cierre 'RBRACE' y ya no quedan tokens, lanzar error
    if not match(tokens, 'RBRACE'):
        raise SyntaxError(f"Error en línea {func_line}, columna {func_col}: falta '}}' de cierre en el bloque de la función '{func_name}'")
    # Consumir la llave de cierre 'RBRACE'
    tokens.pop(0)
    # Retorna la estructura de la función con su nombre, parámetros y cuerpo
    return ('FUNCTION', func_name, params, body)

# Función para procesar una estructura condicional 'if'
def parse_if(tokens):
    # Verificamos si el primer token es la palabra clave 'if'
    expect_keyword(tokens, 'if')

    # Guardamos la información de la línea y columna del 'if' para mostrarla en caso de error
    if_line, if_col = tokens[0][2], tokens[0][3]

    # Espera el paréntesis de apertura '('
    expect(tokens, 'LPAREN')

    # Procesa la expresión dentro de los paréntesis
    cond = parse_expression(tokens)

    # Espera el paréntesis de cierre ')'
    expect(tokens, 'RPAREN')
    
    # Espera la llave de apertura '{'
    expect(tokens, 'LBRACE')

    block = []
    # Procesar sentencias dentro del bloque
    while tokens and not match(tokens, 'RBRACE'):
        block.append(parse_statement(tokens))

    # Si no hemos encontrado la llave de cierre 'RBRACE' y ya no quedan tokens, lanzar error
    if not match(tokens, 'RBRACE'):
        raise SyntaxError(f"Error en línea {if_line}, columna {if_col}: falta '}}' de cierre en el bloque 'if'")

    # Consumir la llave de cierre 'RBRACE'
    tokens.pop(0)

    # Retorna la estructura del bloque 'if' con su condición y bloque de sentencias
    return ('IF', cond, block)

# Función para procesar expresiones, que son comparaciones o operaciones
def parse_expression(tokens):
    return parse_comparison(tokens)

# Función para procesar expresiones de comparación (ejemplo: 'x > 5', 'y == 3')
def parse_comparison(tokens):
    # Primero procesamos las operaciones de adición y sustracción
    left = parse_add_sub(tokens)

    # Mientras encontremos un operador de comparación ('>', '<', '==')
    while match(tokens, 'GREATER') or match(tokens, 'LESS') or match(tokens, 'EQUALS'):
        _, op, _, _ = tokens.pop(0)  # Consumimos el operador de comparación
        # Procesamos la expresión de la derecha de la comparación
        right = parse_add_sub(tokens)
        # Retornamos la comparación estructurada
        left = (op, left, right)

    return left

# Función para procesar operaciones de adición y sustracción
def parse_add_sub(tokens):
    # Primero procesamos las multiplicaciones y divisiones
    left = parse_mul_div(tokens)
    # Mientras encontremos un operador de adición o sustracción
    while match(tokens, 'OPERATOR', '+') or match(tokens, 'OPERATOR', '-'):
        _, op, _, _ = tokens.pop(0)  # Consumimos el operador
        # Procesamos la expresión de la derecha
        right = parse_mul_div(tokens)
        # Retornamos la expresión con el operador aplicado
        left = (op, left, right)
    return left

# Función para procesar operaciones de multiplicación y división
def parse_mul_div(tokens):
    # Procesamos el primer operando
    left = parse_primary(tokens)
    # Mientras encontremos un operador de multiplicación o división
    while match(tokens, 'OPERATOR', '*') or match(tokens, 'OPERATOR', '/'):
        _, op, _, _ = tokens.pop(0)  # Consumimos el operador
        # Procesamos el operando de la derecha
        right = parse_primary(tokens)
        # Retornamos la expresión con el operador aplicado
        left = (op, left, right)

    return left

# Función para procesar los operandos primarios (números, identificadores o paréntesis)
def parse_primary(tokens):
    # Soporte para negación lógica: !expr
    if match(tokens, 'NOT'):
        _, val, line, col = tokens.pop(0)
        operand = parse_primary(tokens)
        return ('NOT', operand)
    
    # Soporte para valores booleanos: true y false
    if match_keyword(tokens, 'true'):
        tokens.pop(0)
        return True
    if match_keyword(tokens, 'false'):
        tokens.pop(0)
        return False
    
    # Soporte para cast: int("5") o float(x)
    if match_keyword(tokens, 'int') or match_keyword(tokens, 'float'):
        cast_type = tokens.pop(0)[1]  # 'int' o 'float'
        if not match(tokens, 'LPAREN'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba '(' después de '{cast_type}' para conversión de tipo.")
        tokens.pop(0)  # Consume LPAREN
        expr = parse_expression(tokens)
        if not match(tokens, 'RPAREN'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ')' después de la expresión en conversión de tipo.")
        tokens.pop(0)  # Consume RPAREN
        return ('CAST', cast_type, expr)
    
    # Si encontramos un paréntesis de apertura, procesamos la expresión entre paréntesis
    if match(tokens, 'LPAREN'):
        tokens.pop(0)
        expr = parse_expression(tokens)
        # Verificamos que haya un paréntesis de cierre correspondiente
        if not match(tokens, 'RPAREN'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba RPAREN ')' pero se encontró '{val}'")
        tokens.pop(0)  # Consumimos 'RPAREN'
        return expr

    # Si encontramos un número, lo procesamos
    elif match(tokens, 'NUMBER'):
        return parse_num(tokens)
    
        # Si encontramos una cadena, la procesamos
    elif match(tokens, 'STRING'):
        return parse_string(tokens)

    # Si encontramos un carácter, lo procesamos
    elif match(tokens, 'CHAR'):
        return parse_char(tokens)

    # Si encontramos un identificador, lo procesamos
    elif match(tokens, 'IDENTIFIER'):
        return parse_id(tokens)

    # Si encontramos un operador de comparación '==', lanzamos un error
    elif match(tokens, 'OPERATOR') and tokens[0][1] == '==':
        _, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: expresión no puede comenzar con '=='")

    # Si no encontramos un token esperado, lanzamos un error
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: token inesperado '{val}' en expresión")


# === FUNCIONES AUXILIARES ===

# Variable global para almacenar la última línea procesada en el analizador.
last_token_line = None

# Función para procesar un tipo de dato (int, float)
def parse_type(tokens):
    global last_token_line  # Accede a la variable global para la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba tipo, pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens.pop(0)  # Extrae el primer token de la lista.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica si el tipo de token es 'int' o 'float', que son tipos válidos en este contexto.
    if tipo == 'KEYWORD' and val in ('int', 'float', 'string', 'char', 'bool'):
        return val
    
    # Si no es un tipo válido, lanza un error especificando la línea y columna.
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un tipo válido, pero se encontró '{val}'")

# Función para procesar un identificador (como variables o nombres de funciones)
def parse_id(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay tokens disponibles, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba identificador, pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens.pop(0)  # Extrae el primer token de la lista.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica si el token es un identificador válido.
    if tipo == 'IDENTIFIER':
        return val
    
    # Si el token no es un identificador válido, lanza un error con la línea y columna.
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba identificador, pero se encontró '{val}'")

# Función para procesar números (entero o decimal)
def parse_num(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba número, pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens.pop(0)  # Extrae el primer token de la lista.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Si el token es un número, lo procesa como entero o decimal según corresponda.
    if tipo == 'NUMBER':
        return float(val) if '.' in val else int(val)
    
    # Si el token no es un número válido, lanza un error con la línea y columna.
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un número válido, pero se encontró '{val}'")

# Función para procesar el operador de asignación '='
def parse_equals(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba '=', pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica que el token sea un operador '='.
    if tipo != 'OPERATOR' or val != '=':
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba '=', pero se encontró '{val}'.")
    
    tokens.pop(0)  # Consume el operador '='.

# Función para procesar el punto y coma ';' al final de las instrucciones
def parse_semi(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba ';', pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica que el token sea un punto y coma ';'.
    if tipo != 'SEMICOLON':
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ';', pero se encontró '{val}'.")
    
    tokens.pop(0)  # Consume el punto y coma ';'.


# Función para procesar cadenas de texto
def parse_string(tokens):
    tipo, val, line, col = tokens.pop(0)
    # Asegurarse que la cadena esté entre comillas dobles
    if tipo == 'STRING':
        return val  # Retorna el valor de la cadena
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba una cadena pero se encontró '{val}'")

# Función para procesar caracteres
def parse_char(tokens):
    tipo, val, line, col = tokens.pop(0)
    # Asegurarse que el carácter esté entre comillas simples
    if tipo == 'CHAR':
        return val  # Retorna el valor del carácter
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un carácter pero se encontró '{val}'")

# Función para hacer coincidir un tipo de token y valor específico
def match(tokens, type_, value=None):
    if not tokens:
        return False
    tk_type, tk_val, *_ = tokens[0]  # Obtiene el tipo y valor del primer token
    return tk_type == type_ and (value is None or tk_val == value)

# Función para verificar si el token actual es una palabra clave
def match_keyword(tokens, keyword):
    if not tokens:
        return False
    tk_type, tk_val, *_ = tokens[0]  # Obtiene el tipo y valor del primer token
    return tk_type == 'KEYWORD' and tk_val == keyword

# Función para esperar un token específico
def expect(tokens, type_, value=None):
    if not match(tokens, type_, value):
        if tokens:
            tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba {type_} '{value}' pero se encontró '{val}'")
        else:
            raise SyntaxError(f"Error: se esperaba {type_} '{value}' pero se encontró EOF")
    tokens.pop(0)  # Consume el token esperado

# Función para esperar una palabra clave específica
def expect_keyword(tokens, keyword):
    if not match_keyword(tokens, keyword):
        if tokens:
            tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba palabra clave '{keyword}' pero se encontró '{val}'")
        else:
            raise SyntaxError(f"Error: se esperaba palabra clave '{keyword}' pero se encontró EOF")
    tokens.pop(0)  # Consume la palabra clave esperada

def parse_function_call(tokens):
    func_name = tokens.pop(0)[1]  # IDENTIFIER
    tokens.pop(0)  # LPAREN
    args = []
    # Procesa los argumentos hasta RPAREN
    while not match(tokens, 'RPAREN'):
        args.append(parse_expression(tokens))
        if match(tokens, 'COMMA'):
            tokens.pop(0)
    tokens.pop(0)  # RPAREN
    if match(tokens, 'SEMICOLON'):
        tokens.pop(0)
    return ('CALL', func_name, args)

def parse_for(tokens):
    expect_keyword(tokens, 'for')   # Verificamos si el primer token es la palabra clave 'for'
    for_line, for_col = tokens[0][2], tokens[0][3] # Guardamos la información de la línea y columna del 'for' para mostrarla en caso de error
    
    expect(tokens, 'LPAREN')    # Espera el paréntesis de apertura '('
    
    init = None # Procesa la inicialización del for (debe ser declaración completa o asignación completa)
    if match_keyword(tokens, 'int') or match_keyword(tokens, 'float'):
        init = parse_declaration(tokens)    # Declaración: for(int i = 0; ...)
    elif match(tokens, 'IDENTIFIER'):
        init = parse_assignment(tokens) # Asignación: for(i = 0; ...)
    elif match(tokens, 'SEMICOLON'):
        # Inicialización vacía: for(; ...)
        tokens.pop(0)  # Consumir el ';'
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba inicialización en bucle 'for', pero se encontró '{val}'")

    # Procesa la condición del for
    condition = None
    if not match(tokens, 'SEMICOLON'):
        condition = parse_expression(tokens)
    expect(tokens, 'SEMICOLON') # Espera el punto y coma después de la condición

    # Procesa el incremento del for
    increment = None
    if not match(tokens, 'RPAREN'):
        if match(tokens, 'IDENTIFIER'):
            increment = parse_assignment(tokens)
        else:
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba incremento en bucle 'for', pero se encontró '{val}'")
    expect(tokens, 'RPAREN')    # Espera el paréntesis de cierre ')'
    
    # Espera la llave de apertura '{'
    expect(tokens, 'LBRACE')

    # Procesar el cuerpo del bucle
    body = []
    while tokens and not match(tokens, 'RBRACE'):
        body.append(parse_statement(tokens))

    # Si no hemos encontrado la llave de cierre 'RBRACE' y ya no quedan tokens, lanzar error
    if not match(tokens, 'RBRACE'):
        raise SyntaxError(f"Error en línea {for_line}, columna {for_col}: falta '}}' de cierre en el bloque 'for'")

    # Consumir la llave de cierre 'RBRACE'
    tokens.pop(0)

    # Retorna la estructura del bucle 'for'
    return ('FOR', init, condition, increment, body)

# Función para procesar un bucle 'while'
def parse_while(tokens):
    expect_keyword(tokens, 'while') # Verificamos si el primer token es la palabra clave 'while'

    # Guardamos la información de la línea y columna del 'while' para mostrarla en caso de error
    while_line, while_col = tokens[0][2], tokens[0][3]

    # Espera el paréntesis de apertura '('
    expect(tokens, 'LPAREN')

    # Procesa la condición del while
    condition = parse_expression(tokens)

    # Espera el paréntesis de cierre ')'
    expect(tokens, 'RPAREN')
    
    # Espera la llave de apertura '{'
    expect(tokens, 'LBRACE')

    # Procesar el cuerpo del bucle
    body = []
    while tokens and not match(tokens, 'RBRACE'):
        body.append(parse_statement(tokens))

    # Si no hemos encontrado la llave de cierre 'RBRACE' y ya no quedan tokens, lanzar error
    if not match(tokens, 'RBRACE'):
        raise SyntaxError(f"Error en línea {while_line}, columna {while_col}: falta '}}' de cierre en el bloque 'while'")

    # Consumir la llave de cierre 'RBRACE'
    tokens.pop(0)

    # Retorna la estructura del bucle 'while'
    return ('WHILE', condition, body)