from parser.statements import parse_statement

def parser(tokens):
    tokens = tokens.copy()
    ast = []
    while tokens:
        stmt = parse_statement(tokens)
        ast.append(stmt)
    return ast