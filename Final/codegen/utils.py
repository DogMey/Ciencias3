"""
Utilidades para la generación de código intermedio.
"""

class TempVariableManager:
    """Manejador de variables temporales para código intermedio."""
    
    def __init__(self):
        self.temp_counter = 0
    
    def get_temp_var(self):
        """Genera una nueva variable temporal."""
        temp_var = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_var
    
    def reset(self):
        """Reinicia el contador de variables temporales."""
        self.temp_counter = 0


class CodeGenerator:
    """Generador principal de código intermedio."""
    
    def __init__(self):
        self.temp_manager = TempVariableManager()
        self.instructions = []
        self.symbol_table = {}
    
    def add_instruction(self, instruction):
        """Añade una instrucción al código intermedio."""
        self.instructions.append(instruction)
    
    def get_temp_var(self):
        """Obtiene una nueva variable temporal."""
        return self.temp_manager.get_temp_var()
    
    def reset(self):
        """Reinicia el generador."""
        self.temp_manager.reset()
        self.instructions = []
        self.symbol_table = {}
    
    def get_code(self):
        """Retorna el código intermedio generado."""
        return self.instructions
    
    def print_code(self):
        """Imprime el código intermedio de forma legible."""
        print("=== CÓDIGO INTERMEDIO ===")
        for i, instruction in enumerate(self.instructions):
            print(f"{i+1:2d}: {instruction}")
        print("========================")
    
    def declare_variable(self, var_type, var_name, value=None):
        """Registra una variable en la tabla de símbolos."""
        self.symbol_table[var_name] = {
            'type': var_type,
            'value': value
        }
    
    def is_variable_declared(self, var_name):
        """Verifica si una variable está declarada."""
        return var_name in self.symbol_table
    
    def get_variable_type(self, var_name):
        """Obtiene el tipo de una variable."""
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]['type']
        return None
