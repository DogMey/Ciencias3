import re

# === DEFINICIÓN DE TOKENS ===
# Cada tupla contiene un nombre de token y su patrón de expresión regular.
# El orden es importante: los patrones más específicos deben ir primero.
token_definitions = [
    ('LOGICOPERATOR', r'==|!=|>=|<=|>|<'),      # Operadores lógicos (orden importante)
    ('COMMENT', r'//.*'),                      # Comentarios
    ('NUMBER', r'\d+\.\d+|\d+'),               # Números decimales o enteros
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),           # Identificadores
    ('OPERATOR', r'[+\-*/=]'),                 # Operadores aritméticos y asignación
    ('LPAREN', r'\('),                         # Paréntesis izquierdo
    ('RPAREN', r'\)'),                         # Paréntesis derecho
    ('LBRACE', r'\{'),                         # Llave izquierda
    ('RBRACE', r'\}'),                         # Llave derecha
    ('SEMICOLON', r';'),                       # Punto y coma
    ('WHITESPACE', r'\s+'),                    # Espacios en blanco (se ignoran)
]

def lexer(source_code):
    """
    Analizador léxico que devuelve tokens con tipo, valor, línea y columna.
    """
    position = 0        # Posición actual dentro del texto fuente
    line = 1
    column = 1
    found_tokens = []   # Lista donde se almacenarán los tokens válidos

    # Mientras no se haya llegado al final del texto fuente
    while position < len(source_code):
        match = None    # Variable para almacenar la coincidencia actual

        for token_type, pattern in token_definitions:
            regex = re.compile(pattern)                 # Compila el patrón regex    
            match = regex.match(source_code, position)  # Busca coincidencia desde la posición actual

            if match:                           # Si encontró una coincidencia
                token_value = match.group(0)    # Extrae el texto coincidente

                # Ignorar los tokens de espacio en blanco y comentarios
                if token_type not in ('WHITESPACE', 'COMMENT'):
                    # Añade el token (tipo, valor, línea, columna) a la lista de tokens encontrados
                    found_tokens.append({
                        'type': token_type,
                        'value': token_value,
                        'line': line,
                        'column': column
                    })

                # Actualizar línea y columna
                lines = token_value.split('\n')
                if len(lines) > 1:
                    line += len(lines) - 1      # Aumenta la línea por cada nueva línea encontrada
                    column = len(lines[-1]) + 1 # Columna de la última línea
                else:
                    column += len(token_value)  # Aumenta la columna por la longitud del token

                position = match.end()  # Avanza la posición hasta el final del texto que coincidió
                break

        # Si no se encontró ningún token válido en la posición actual, hay un error
        if not match:
            raise SyntaxError(f"Token no reconocido en la línea {line}, columna {column}")

    # Retorna la lista completa de tokens válidos encontrados en el código fuente
    return found_tokens