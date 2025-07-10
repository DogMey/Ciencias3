"""
Traductor de código intermedio a código objeto.
"""

from .vm_instructions import VMInstructionSet, VMInstruction
from .variable_manager import VariableManager

class CodeTranslator:
    """Traduce código intermedio a código objeto."""
    
    def __init__(self):
        self.variable_manager = VariableManager()
        self.object_code = []
    
    def reset(self):
        """Reinicia el traductor."""
        self.variable_manager.reset()
        self.object_code = []
    
    def translate_intermediate_instruction(self, instruction):
        """Traduce una instrucción intermedia a código objeto."""
        instruction = instruction.strip()
        
        if instruction.startswith('DECLARE'):
            return self._translate_declare(instruction)
        
        elif instruction.startswith('ASSIGN'):
            return self._translate_assign(instruction)
        
        elif '=' in instruction and not instruction.startswith('ASSIGN'):
            return self._translate_expression(instruction)
        
        else:
            raise ValueError(f"Instrucción intermedia no reconocida: {instruction}")
    
    def _translate_declare(self, instruction):
        """Traduce instrucción DECLARE."""
        # Formato: DECLARE tipo nombre
        parts = instruction.split()
        var_type = parts[1]
        var_name = parts[2]
        
        # Declarar variable y obtener dirección
        address = self.variable_manager.declare_variable(var_name, var_type)
        
        # Generar instrucción de asignación de memoria
        return [VMInstruction(VMInstructionSet.ALLOC, address, f"Declarar {var_name}")]
    
    def _translate_assign(self, instruction):
        """Traduce instrucción ASSIGN."""
        # Formato: ASSIGN variable = valor
        parts = instruction.split('=')
        var_part = parts[0].strip().split()
        var_name = var_part[1]  # Omitir "ASSIGN"
        value_part = parts[1].strip()
        
        instructions = []
        
        # Si el valor es un número
        if value_part.isdigit() or (value_part.startswith('-') and value_part[1:].isdigit()):
            instructions.append(VMInstruction(VMInstructionSet.PUSH, int(value_part), f"Valor {value_part}"))
        
        # Si el valor es una variable
        else:
            # Verificar si es variable temporal
            if self.variable_manager.is_temp_variable(value_part):
                if value_part not in self.variable_manager.temp_variables:
                    self.variable_manager.declare_temp_variable(value_part)
            
            var_address = self.variable_manager.get_variable_address(value_part)
            instructions.append(VMInstruction(VMInstructionSet.LOAD, var_address, f"Cargar {value_part}"))
        
        # Guardar en la variable destino
        dest_address = self.variable_manager.get_variable_address(var_name)
        instructions.append(VMInstruction(VMInstructionSet.STORE, dest_address, f"Guardar en {var_name}"))
        
        return instructions
    
    def _translate_expression(self, instruction):
        """Traduce instrucción de expresión."""
        # Formato: temp = operando1 operador operando2
        parts = instruction.split('=')
        result_var = parts[0].strip()
        expression = parts[1].strip()
        
        # Declarar variable temporal si no existe
        if self.variable_manager.is_temp_variable(result_var):
            if result_var not in self.variable_manager.temp_variables:
                self.variable_manager.declare_temp_variable(result_var)
        
        instructions = []
        
        # Parsear expresión
        expr_parts = expression.split()
        operand1 = expr_parts[0]
        operator = expr_parts[1]
        operand2 = expr_parts[2]
        
        # Cargar primer operando
        if operand1.isdigit() or (operand1.startswith('-') and operand1[1:].isdigit()):
            instructions.append(VMInstruction(VMInstructionSet.PUSH, int(operand1), f"Valor {operand1}"))
        else:
            # Verificar si es variable temporal
            if self.variable_manager.is_temp_variable(operand1):
                if operand1 not in self.variable_manager.temp_variables:
                    self.variable_manager.declare_temp_variable(operand1)
            
            addr1 = self.variable_manager.get_variable_address(operand1)
            instructions.append(VMInstruction(VMInstructionSet.LOAD, addr1, f"Cargar {operand1}"))
        
        # Cargar segundo operando
        if operand2.isdigit() or (operand2.startswith('-') and operand2[1:].isdigit()):
            instructions.append(VMInstruction(VMInstructionSet.PUSH, int(operand2), f"Valor {operand2}"))
        else:
            # Verificar si es variable temporal
            if self.variable_manager.is_temp_variable(operand2):
                if operand2 not in self.variable_manager.temp_variables:
                    self.variable_manager.declare_temp_variable(operand2)
            
            addr2 = self.variable_manager.get_variable_address(operand2)
            instructions.append(VMInstruction(VMInstructionSet.LOAD, addr2, f"Cargar {operand2}"))
        
        # Aplicar operador
        if operator == '+':
            instructions.append(VMInstruction(VMInstructionSet.ADD, None, "Sumar"))
        elif operator == '-':
            instructions.append(VMInstruction(VMInstructionSet.SUB, None, "Restar"))
        elif operator == '*':
            instructions.append(VMInstruction(VMInstructionSet.MUL, None, "Multiplicar"))
        elif operator == '/':
            instructions.append(VMInstruction(VMInstructionSet.DIV, None, "Dividir"))
        elif operator == '%':
            instructions.append(VMInstruction(VMInstructionSet.MOD, None, "Módulo"))
        else:
            raise ValueError(f"Operador no soportado: {operator}")
        
        # Guardar resultado
        result_address = self.variable_manager.get_variable_address(result_var)
        instructions.append(VMInstruction(VMInstructionSet.STORE, result_address, f"Guardar en {result_var}"))
        
        return instructions
    
    def translate_program(self, intermediate_code):
        """Traduce un programa completo de código intermedio a código objeto."""
        self.reset()
        
        for instruction in intermediate_code:
            object_instructions = self.translate_intermediate_instruction(instruction)
            self.object_code.extend(object_instructions)
        
        # Agregar instrucción de parada
        self.object_code.append(VMInstruction(VMInstructionSet.HALT, None, "Fin del programa"))
        
        return self.object_code
    
    def get_object_code(self):
        """Retorna el código objeto generado."""
        return self.object_code
    
    def print_object_code(self):
        """Imprime el código objeto de forma legible."""
        print("=== CÓDIGO OBJETO ===")
        for i, instruction in enumerate(self.object_code):
            print(f"{i+1:2d}: {instruction}")
        print("====================")
    
    def get_variable_info(self):
        """Retorna información sobre las variables."""
        return {
            'variables': self.variable_manager.get_all_variables(),
            'count': self.variable_manager.get_variable_count()
        }


def translate_intermediate_to_object(intermediate_code):
    """Función de conveniencia para traducir código intermedio a objeto."""
    translator = CodeTranslator()
    return translator.translate_program(intermediate_code)
