# Generador de Código Objeto y Máquina Virtual

## Descripción

El generador de código objeto traduce código intermedio de tres direcciones a instrucciones ejecutables por una máquina virtual de pila. Define un conjunto de instrucciones simples y una arquitectura de ejecución basada en pila.

## Definición del Código Objeto

### Formato de Instrucciones
```
<OPCODE> [<OPERANDO>]  [# <COMENTARIO>]
```

### Conjunto de Instrucciones

#### Gestión de Pila
- `PUSH <valor>`: Empuja un valor constante a la pila
- `POP`: Extrae el valor del tope de la pila
- `LOAD <dirección>`: Carga variable desde memoria a la pila
- `STORE <dirección>`: Guarda valor de la pila en memoria

#### Gestión de Memoria
- `ALLOC <dirección>`: Reserva espacio de memoria para variable

#### Operaciones Aritméticas
- `ADD`: `pop b, pop a, push(a + b)`
- `SUB`: `pop b, pop a, push(a - b)`
- `MUL`: `pop b, pop a, push(a * b)`
- `DIV`: `pop b, pop a, push(a / b)`
- `MOD`: `pop b, pop a, push(a % b)`

#### Control de Ejecución
- `HALT`: Termina la ejecución del programa
- `NOP`: No operación

### Traducción de Código Intermedio

#### Declaraciones
**Intermedio:**
```
DECLARE int x
```
**Objeto:**
```
ALLOC 0    # Reservar memoria para x
```

#### Asignaciones Directas
**Intermedio:**
```
ASSIGN x = 5
```
**Objeto:**
```
PUSH 5     # Cargar constante
STORE 0    # Guardar en variable x
```

#### Expresiones de Tres Direcciones
**Intermedio:**
```
t0 = a + b
```
**Objeto:**
```
LOAD 0     # Cargar variable a
LOAD 1     # Cargar variable b
ADD        # Sumar
STORE 2    # Guardar resultado en t0
```

#### Ejemplo Completo
**Código intermedio:**
```
DECLARE int x
ASSIGN x = 10
DECLARE int y
ASSIGN y = 20
t0 = x + y
ASSIGN x = t0
```

**Código objeto:**
```
ALLOC 0    # Declarar x
PUSH 10    # Valor 10
STORE 0    # x = 10
ALLOC 1    # Declarar y
PUSH 20    # Valor 20
STORE 1    # y = 20
LOAD 0     # Cargar x
LOAD 1     # Cargar y
ADD        # Sumar
STORE 2    # t0 = x + y
LOAD 2     # Cargar t0
STORE 0    # x = t0
HALT       # Fin
```

## Especificación de la Máquina Virtual

### Arquitectura
- **Modelo**: Máquina de pila (stack-based)
- **Memoria**: Lineal, direccionamiento por enteros secuenciales
- **Pila**: LIFO para operandos y resultados temporales
- **Contador de programa**: PC para control de ejecución secuencial

### Estado de la Máquina
```python
{
    'stack': [],           # Pila de operandos
    'memory': {},          # Memoria de variables {dirección: valor}
    'pc': 0,              # Program Counter
    'running': False       # Estado de ejecución
}
```

### Gestión de Variables
- **Direcciones**: Asignación secuencial automática (0, 1, 2, ...)
- **Variables de usuario**: Direcciones bajas
- **Variables temporales**: Direcciones siguientes
- **Mapeo**: `{nombre_variable: dirección_memoria}`

### Semántica de Ejecución
1. **Fetch**: Obtener instrucción en PC
2. **Decode**: Interpretar opcode y operando
3. **Execute**: Ejecutar operación
4. **Update**: Incrementar PC (salvo instrucciones de control)

### Manejo de Errores
- **Stack Underflow**: Pop en pila vacía
- **División por Cero**: Verificación automática
- **Memoria No Inicializada**: Acceso a dirección no asignada
- **Opcode Inválido**: Instrucción no reconocida

## Uso Programático

### Traducción
```python
from objectcode.code_translator import CodeTranslator

translator = CodeTranslator()
object_code = translator.translate_program(intermediate_code)
```

### Ejecución
```python
from objectcode.stack_machine import StackMachine

vm = StackMachine()
vm.load_program(object_code)
vm.run(debug=True)
```

### Introspección
```python
# Estado de la máquina
state = vm.get_state()

# Información de variables
var_info = translator.get_variable_info()
```

---
*Generador de Código Objeto - Especificación Técnica*
