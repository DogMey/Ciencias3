"""
Máquina virtual de pila para ejecutar código objeto.
"""

from .vm_instructions import VMInstructionSet, VMInstruction

class StackMachine:
    """Máquina virtual de pila simple."""
    
    def __init__(self):
        self.stack = []
        self.memory = {}  # dirección -> valor
        self.pc = 0  # Program Counter
        self.instructions = []
        self.running = False
        self.debug = False
    
    def reset(self):
        """Reinicia la máquina virtual."""
        self.stack = []
        self.memory = {}
        self.pc = 0
        self.instructions = []
        self.running = False
    
    def load_program(self, instructions):
        """Carga un programa en la máquina virtual."""
        self.instructions = instructions
        self.pc = 0
        self.running = True
    
    def push(self, value):
        """Empuja un valor a la pila."""
        self.stack.append(value)
        if self.debug:
            print(f"  PUSH {value} -> Stack: {self.stack}")
    
    def pop(self):
        """Saca un valor de la pila."""
        if not self.stack:
            raise RuntimeError("Stack underflow: intento de hacer pop en pila vacía")
        value = self.stack.pop()
        if self.debug:
            print(f"  POP {value} -> Stack: {self.stack}")
        return value
    
    def peek(self):
        """Mira el valor del tope de la pila sin sacarlo."""
        if not self.stack:
            raise RuntimeError("Stack empty: intento de hacer peek en pila vacía")
        return self.stack[-1]
    
    def store(self, address, value):
        """Guarda un valor en memoria."""
        self.memory[address] = value
        if self.debug:
            print(f"  STORE @{address} = {value}")
    
    def load(self, address):
        """Carga un valor de memoria."""
        if address not in self.memory:
            raise RuntimeError(f"Dirección de memoria {address} no inicializada")
        value = self.memory[address]
        if self.debug:
            print(f"  LOAD @{address} = {value}")
        return value
    
    def execute_instruction(self, instruction):
        """Ejecuta una instrucción individual."""
        if isinstance(instruction, VMInstruction):
            opcode = instruction.opcode
            operand = instruction.operand
        else:
            # Compatibilidad con strings
            parts = instruction.split()
            opcode = parts[0]
            operand = parts[1] if len(parts) > 1 else None
        
        if self.debug:
            print(f"PC:{self.pc:2d} {opcode} {operand if operand else ''}")
        
        # Instrucciones de pila
        if opcode == VMInstructionSet.PUSH:
            if isinstance(operand, int):
                self.push(operand)
            elif isinstance(operand, str):
                if operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
                    self.push(int(operand))
                else:
                    self.push(operand)
            else:
                self.push(operand)
        
        elif opcode == VMInstructionSet.POP:
            self.pop()
        
        elif opcode == VMInstructionSet.LOAD:
            address = int(operand)
            value = self.load(address)
            self.push(value)
        
        elif opcode == VMInstructionSet.STORE:
            address = int(operand)
            value = self.pop()
            self.store(address, value)
        
        elif opcode == VMInstructionSet.ALLOC:
            address = int(operand)
            self.memory[address] = 0  # Inicializar con 0
        
        # Instrucciones aritméticas
        elif opcode == VMInstructionSet.ADD:
            b = self.pop()
            a = self.pop()
            self.push(a + b)
        
        elif opcode == VMInstructionSet.SUB:
            b = self.pop()
            a = self.pop()
            self.push(a - b)
        
        elif opcode == VMInstructionSet.MUL:
            b = self.pop()
            a = self.pop()
            self.push(a * b)
        
        elif opcode == VMInstructionSet.DIV:
            b = self.pop()
            a = self.pop()
            if b == 0:
                raise RuntimeError("División por cero")
            self.push(a // b)  # División entera
        
        elif opcode == VMInstructionSet.MOD:
            b = self.pop()
            a = self.pop()
            self.push(a % b)
        
        # Instrucciones de control
        elif opcode == VMInstructionSet.HALT:
            self.running = False
        
        elif opcode == VMInstructionSet.NOP:
            pass  # No operación
        
        # Instrucciones de debugging
        elif opcode == VMInstructionSet.PRINT:
            if self.stack:
                print(f"Stack top: {self.peek()}")
            else:
                print("Stack is empty")
        
        elif opcode == VMInstructionSet.PRINT_VAR:
            address = int(operand)
            if address in self.memory:
                print(f"Variable @{address}: {self.memory[address]}")
            else:
                print(f"Variable @{address}: not initialized")
        
        else:
            raise RuntimeError(f"Instrucción desconocida: {opcode}")
    
    def run(self, debug=False):
        """Ejecuta el programa cargado."""
        self.debug = debug
        
        if debug:
            print("=== INICIANDO EJECUCIÓN ===")
            print(f"Programa: {len(self.instructions)} instrucciones")
        
        while self.running and self.pc < len(self.instructions):
            try:
                self.execute_instruction(self.instructions[self.pc])
                self.pc += 1
            except Exception as e:
                print(f"Error en PC {self.pc}: {e}")
                break
        
        if debug:
            print("=== EJECUCIÓN TERMINADA ===")
            print(f"Estado final - Stack: {self.stack}")
            print(f"Memoria: {self.memory}")
    
    def get_state(self):
        """Retorna el estado actual de la máquina."""
        return {
            'stack': self.stack.copy(),
            'memory': self.memory.copy(),
            'pc': self.pc,
            'running': self.running
        }
