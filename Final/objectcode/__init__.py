"""
Módulo de generación de código objeto.
Traduce código intermedio a instrucciones ejecutables por una máquina virtual de pila.
"""

from .vm_instructions import VMInstructionSet
from .stack_machine import StackMachine
from .code_translator import translate_intermediate_to_object
from .variable_manager import VariableManager

__all__ = [
    'VMInstructionSet',
    'StackMachine',
    'translate_intermediate_to_object',
    'VariableManager'
]
