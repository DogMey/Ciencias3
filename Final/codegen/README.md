# Generador de Código Intermedio

## Descripción

El generador de código intermedio traduce el AST (Abstract Syntax Tree) a código de tres direcciones. Este formato intermedio es independiente del lenguaje fuente y la arquitectura objetivo, facilitando optimizaciones y la generación de código objeto.

## Formato de Representación Intermedia

### Sintaxis General
```
<instrucción> [<operandos>]
```

### Tipos de Instrucciones

#### 1. Declaraciones
```
DECLARE <tipo> <variable>
```

**Ejemplo:**
```
DECLARE int x
DECLARE float pi
```

#### 2. Asignaciones
```
ASSIGN <variable> = <valor>
```

**Ejemplo:**
```
ASSIGN x = 5
ASSIGN y = x
```

#### 3. Expresiones de Tres Direcciones
```
<resultado> = <operando1> <operador> <operando2>
```

**Operadores soportados:**
- Aritméticos: `+`, `-`, `*`, `/`, `%`
- Relacionales: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Lógicos: `&&`, `||`, `!`

**Ejemplo:**
```
t0 = a + b
t1 = x * 2
t2 = t0 - t1
```

### Variables Temporales

Las variables temporales siguen el formato `t<número>` y se generan automáticamente:
- `t0`, `t1`, `t2`, ..., `tn`
- Se utilizan para almacenar resultados intermedios de expresiones complejas
- Tienen alcance local al bloque de código

### Ejemplos de Traducción

#### Expresión Simple
**Código fuente:**
```c
int x = 5 + 3;
```

**Código intermedio:**
```
DECLARE int x
t0 = 5 + 3
ASSIGN x = t0
```

#### Expresión Compleja
**Código fuente:**
```c
int resultado = (a + b) * (c - d);
```

**Código intermedio:**
```
t0 = a + b
t1 = c - d
t2 = t0 * t1
ASSIGN resultado = t2
```

#### Expresión Anidada
**Código fuente:**
```c
int x = a * b + c / (d - e);
```

**Código intermedio:**
```
t0 = a * b
t1 = d - e
t2 = c / t1
t3 = t0 + t2
ASSIGN x = t3
```

## Componentes del Generador

### CodeGenerator
Clase principal que coordina la generación:
```python
class CodeGenerator:
    def __init__(self):
        self.temp_manager = TempVariableManager()
        self.instructions = []
        self.symbol_table = {}
```

### TempVariableManager
Gestiona la generación de variables temporales:
```python
def get_temp_var(self):
    temp_var = f"t{self.temp_counter}"
    self.temp_counter += 1
    return temp_var
```

## Uso Programático

```python
from codegen import CodeGenerator, generate_declaration_code

# Crear generador
code_generator = CodeGenerator()

# Procesar nodo AST
ast_node = ('DECLARATION', 'int', 'x', 5)
generate_declaration_code(ast_node, code_generator)

# Obtener código generado
instructions = code_generator.get_code()
```

## Formato de Salida

El código intermedio se representa como una lista de strings:
```python
[
    "DECLARE int x",
    "ASSIGN x = 5",
    "t0 = x + 1",
    "ASSIGN x = t0"
]
```

---
*Generador de Código Intermedio - Documentación Técnica*
