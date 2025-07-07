from .utils import match_keyword, match
from .declaration import parse_declaration
from .ifblock import parse_if
from .forblock import parse_for
from .assignment import parse_assignment
from .functions import parse_function_call

def parse_statement(tokens):
    if match_keyword(tokens, 'int') or match_keyword(tokens, 'float'):
        return parse_declaration(tokens)
    elif match_keyword(tokens, 'if'):
        return parse_if(tokens)
    elif match_keyword(tokens, 'for'):
        return parse_for(tokens)
    elif match(tokens, 'IDENTIFIER'):
        # Soporte para llamada a función: identificador seguido de LPAREN
        if len(tokens) > 1 and tokens[1][0] == 'LPAREN':
            return parse_function_call(tokens)
        return parse_assignment(tokens)
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: sentencia inválida, token inesperado '{val}'")