"""
Manejador de variables para la generación de código objeto.
"""

class VariableManager:
    """Maneja las variables y su mapeo a direcciones de memoria."""
    
    def __init__(self):
        self.variables = {}  # nombre -> dirección
        self.next_address = 0
        self.temp_variables = {}  # variables temporales
    
    def declare_variable(self, var_name, var_type='int'):
        """Declara una variable y asigna una dirección."""
        if var_name in self.variables:
            raise ValueError(f"Variable '{var_name}' ya declarada")
        
        self.variables[var_name] = self.next_address
        self.next_address += 1
        return self.variables[var_name]
    
    def get_variable_address(self, var_name):
        """Obtiene la dirección de una variable."""
        if var_name in self.variables:
            return self.variables[var_name]
        elif var_name in self.temp_variables:
            return self.temp_variables[var_name]
        else:
            raise ValueError(f"Variable '{var_name}' no declarada")
    
    def declare_temp_variable(self, temp_name):
        """Declara una variable temporal."""
        if temp_name not in self.temp_variables:
            self.temp_variables[temp_name] = self.next_address
            self.next_address += 1
        return self.temp_variables[temp_name]
    
    def is_temp_variable(self, var_name):
        """Verifica si una variable es temporal."""
        return var_name.startswith('t') and var_name[1:].isdigit()
    
    def get_all_variables(self):
        """Retorna todas las variables declaradas."""
        return {**self.variables, **self.temp_variables}
    
    def get_variable_count(self):
        """Retorna el número total de variables."""
        return len(self.variables) + len(self.temp_variables)
    
    def reset(self):
        """Reinicia el manejador de variables."""
        self.variables = {}
        self.temp_variables = {}
        self.next_address = 0
