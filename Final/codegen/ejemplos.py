"""
Ejemplos de prueba para el generador de código intermedio.
"""

# Ejemplo 1: Declaraciones simples
EJEMPLO_DECLARACIONES_SIMPLES = [
    ('DECLARATION', 'int', 'x', 5),
    ('DECLARATION', 'int', 'y', 10),
    ('DECLARATION', 'float', 'z', 3.14)
]

# Ejemplo 2: Declaraciones con expresiones
EJEMPLO_DECLARACIONES_EXPRESIONES = [
    ('DECLARATION', 'int', 'a', 10),
    ('DECLARATION', 'int', 'b', 20),
    ('DECLARATION', 'int', 'suma', ('+', 'a', 'b')),
    ('DECLARATION', 'int', 'producto', ('*', 'a', 'b'))
]

# Ejemplo 3: Asignaciones simples
EJEMPLO_ASIGNACIONES_SIMPLES = [
    ('DECLARATION', 'int', 'x', 5),
    ('ASSIGNMENT', 'x', 10),
    ('ASSIGNMENT', 'x', 'x'),  # Auto-asignación
]

# Ejemplo 4: Asignaciones con expresiones
EJEMPLO_ASIGNACIONES_EXPRESIONES = [
    ('DECLARATION', 'int', 'x', 0),
    ('DECLARATION', 'int', 'y', 5),
    ('ASSIGNMENT', 'x', ('+', 'x', 1)),      # x = x + 1
    ('ASSIGNMENT', 'y', ('*', 'x', 2)),      # y = x * 2
    ('ASSIGNMENT', 'x', ('+', 'x', 'y'))     # x = x + y
]

# Ejemplo 5: Expresiones complejas anidadas
EJEMPLO_EXPRESIONES_COMPLEJAS = [
    ('DECLARATION', 'int', 'a', 5),
    ('DECLARATION', 'int', 'b', 10),
    ('DECLARATION', 'int', 'c', 15),
    ('DECLARATION', 'int', 'resultado', ('+', ('*', 'a', 'b'), ('/', 'c', 3)))
]

# Ejemplo 6: Secuencia de operaciones
EJEMPLO_SECUENCIA_OPERACIONES = [
    ('DECLARATION', 'int', 'x', 1),
    ('ASSIGNMENT', 'x', ('+', 'x', 1)),      # x = x + 1
    ('ASSIGNMENT', 'x', ('*', 'x', 2)),      # x = x * 2
    ('ASSIGNMENT', 'x', ('-', 'x', 1)),      # x = x - 1
    ('ASSIGNMENT', 'x', ('/', 'x', 2))       # x = x / 2
]

# Diccionario con todos los ejemplos
EJEMPLOS_CODEGEN = {
    'declaraciones_simples': EJEMPLO_DECLARACIONES_SIMPLES,
    'declaraciones_expresiones': EJEMPLO_DECLARACIONES_EXPRESIONES,
    'asignaciones_simples': EJEMPLO_ASIGNACIONES_SIMPLES,
    'asignaciones_expresiones': EJEMPLO_ASIGNACIONES_EXPRESIONES,
    'expresiones_complejas': EJEMPLO_EXPRESIONES_COMPLEJAS,
    'secuencia_operaciones': EJEMPLO_SECUENCIA_OPERACIONES
}
