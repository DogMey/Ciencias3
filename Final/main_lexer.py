import re
from lexer.lexer_tokens import KEYWORDS, TOKEN_DEFINITIONS
from lexer.lexer_utils import add_token

def compile_token_regex(token_defs):
    return [(ttype, re.compile(pattern)) for ttype, pattern in token_defs]

TOKEN_REGEX_COMPILED = compile_token_regex(TOKEN_DEFINITIONS)

def lexer(source_code):
    position = 0
    found_tokens = []
    line = 1
    col = 1

    while position < len(source_code):
        match = None
        for token_type, regex in TOKEN_REGEX_COMPILED:
            match = regex.match(source_code, position)
            if match:
                token_value = match.group(0)
                start_line = line
                start_col = col

                lines = token_value.split('\n')
                if len(lines) > 1:
                    line += len(lines) - 1
                    col = len(lines[-1]) + 1
                else:
                    col += len(token_value)

                if token_type not in ('WHITESPACE', 'COMMENT'):
                    add_token(found_tokens, token_type, token_value, start_line, start_col, KEYWORDS)

                position = match.end()
                break

        if not match:
            char_error = source_code[position]
            raise SyntaxError(f"Token no reconocido '{char_error}' en línea {line}, columna {col}")

    return found_tokens