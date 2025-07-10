"""
Conjunto de instrucciones para la máquina virtual de pila.
"""

class VMInstructionSet:
    """Conjunto de instrucciones de la máquina virtual."""
    
    # Instrucciones de pila
    PUSH = "PUSH"      # Empuja valor a la pila
    POP = "POP"        # Saca valor de la pila
    
    # Instrucciones de variables
    LOAD = "LOAD"      # Carga variable a la pila
    STORE = "STORE"    # Guarda valor de la pila en variable
    ALLOC = "ALLOC"    # Reserva espacio para variable
    
    # Instrucciones aritméticas
    ADD = "ADD"        # Suma: pop b, pop a, push a+b
    SUB = "SUB"        # Resta: pop b, pop a, push a-b
    MUL = "MUL"        # Multiplicación: pop b, pop a, push a*b
    DIV = "DIV"        # División: pop b, pop a, push a/b
    MOD = "MOD"        # Módulo: pop b, pop a, push a%b
    
    # Instrucciones de control
    HALT = "HALT"      # Detiene la ejecución
    NOP = "NOP"        # No operación
    
    # Instrucciones de debugging
    PRINT = "PRINT"    # Imprime valor del tope de la pila
    PRINT_VAR = "PRINT_VAR"  # Imprime variable
    
    @classmethod
    def is_arithmetic(cls, instruction):
        """Verifica si una instrucción es aritmética."""
        return instruction in [cls.ADD, cls.SUB, cls.MUL, cls.DIV, cls.MOD]
    
    @classmethod
    def is_stack_operation(cls, instruction):
        """Verifica si una instrucción opera con la pila."""
        return instruction in [cls.PUSH, cls.POP, cls.LOAD, cls.STORE]
    
    @classmethod
    def get_all_instructions(cls):
        """Retorna todas las instrucciones disponibles."""
        return [
            cls.PUSH, cls.POP, cls.LOAD, cls.STORE, cls.ALLOC,
            cls.ADD, cls.SUB, cls.MUL, cls.DIV, cls.MOD,
            cls.HALT, cls.NOP, cls.PRINT, cls.PRINT_VAR
        ]


class VMInstruction:
    """Representa una instrucción de la máquina virtual."""
    
    def __init__(self, opcode, operand=None, comment=None):
        self.opcode = opcode
        self.operand = operand
        self.comment = comment
    
    def __str__(self):
        if self.operand is not None:
            result = f"{self.opcode} {self.operand}"
        else:
            result = self.opcode
        
        if self.comment:
            result += f"  # {self.comment}"
        
        return result
    
    def __repr__(self):
        return f"VMInstruction({self.opcode}, {self.operand}, {self.comment})"
