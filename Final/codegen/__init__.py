"""
Módulo de generación de código intermedio.
Recorre el AST y genera código intermedio de tres direcciones.
"""

from .declaration import generate_declaration_code
from .assignment import generate_assignment_code
from .expressions import generate_expression_code
from .utils import CodeGenerator, TempVariableManager

__all__ = [
    'generate_declaration_code',
    'generate_assignment_code', 
    'generate_expression_code',
    'CodeGenerator',
    'TempVariableManager'
]
