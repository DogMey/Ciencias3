import re

tokens = [
    ('NUM_ENTERO', r'\d+'),
    ('NUM_DECIMAL', r'\d*\.\d+|\d+\.\d*'),
    ('ID', r'[a-zA-Z_]\w*'),
    ('OP', r'[+\-*/=]'),
    ('EQ', r'=='),
    ('PAREN_IZQ', r'\('),
    ('PAREN_DER', r'\)'),
    ('LLAVE_IZQ', r'\{'),
    ('LLAVE_DER', r'\}'),
    ('SEMI', r';'),
    ('WHITESPACE', r'\s+'),
    ('COMENTARIO', r'//.*'),
]

def analizador_lexico(codigo):
    pos = 0
    resultado = []
    while pos < len(codigo):
        match = None
        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(codigo, pos)
            if match:
                text = match.group(0)
                if token_type not in ('WHITESPACE', 'COMENTARIO'):
                    resultado.append((token_type, text))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f"Token no reconocido en posición {pos}")
    return resultado

def reportar_numero_tokens(tokens):
    conteo_tokens = {}
    for tipo, _ in tokens:
        conteo_tokens[tipo] = conteo_tokens.get(tipo, 0) + 1
    print("\n--- Reporte de Número de Tokens ---")
    for tipo, cantidad in conteo_tokens.items():
        print(f"{tipo}: {cantidad}")

if __name__ == "__main__":
    codigo_fuente = """
    int contador = 0; // Inicialización
    if (contador == 10.5) { // Condición
        contador = contador + 1;
    }
    float pi = 3.1416;
    return contador;
    // Este es otro comentario
    """
    tokens_analizados = analizador_lexico(codigo_fuente)
    for tipo, valor in tokens_analizados:
        print(f"{tipo}: {valor}")

    reportar_numero_tokens(tokens_analizados)
