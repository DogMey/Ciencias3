import re

# === DEFINICIÓN DE TOKENS ===
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
    position = 0
    line = 1
    column = 1
    found_tokens = []

    while position < len(source_code):
        match = None

        for token_type, pattern in token_definitions:
            regex = re.compile(pattern)
            match = regex.match(source_code, position)

            if match:
                token_value = match.group(0)

                if token_type not in ('WHITESPACE', 'COMMENT'):
                    found_tokens.append({
                        'type': token_type,
                        'value': token_value,
                        'line': line,
                        'column': column
                    })

                # Actualizar línea y columna
                lines = token_value.split('\n')
                if len(lines) > 1:
                    line += len(lines) - 1
                    column = len(lines[-1]) + 1
                else:
                    column += len(token_value)

                position = match.end()
                break

        if not match:
            raise SyntaxError(f"Token no reconocido en la línea {line}, columna {column}")

    return found_tokens