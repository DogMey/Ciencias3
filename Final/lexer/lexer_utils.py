# lexer_utils.py
def is_keyword(token_type, token_value, keywords):
    return token_type == 'IDENTIFIER' and token_value in keywords

def add_token(tokens, token_type, token_value, line, col, keywords):
    if is_keyword(token_type, token_value, keywords):
        token_type = 'KEYWORD'
    tokens.append((token_type, token_value, line, col))