import ply.lex as lex
import re
from tokens_dict import *

class Tok:
    def __init__(self, stype, token, value, line, start, end, parent=None):
        self.stype = stype
        self.token = token
        self.value = value
        self.line = line
        self.start = start
        self.end = end

lexer = None
tokens = ['ID']

for key, value in token_arr.items():
    tokens.append(key)
    exec("t_"+key+f"=r'{value}'")

for value in types.values():
    if value.upper() not in tokens:
        tokens.append(value.upper())

exec(f"""
def t_ID(t):
    r"(?!{'|'.join(token_arr.values())})\\b[a-zA-Z_]\\w*\\b"
    t.type = token_arr.get(t.value, 'ID')
    return t
""")

def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

def identify_token_type(token):
    for token_type_str, token_type_dict in token_types.items():
        for token_type, token_value in token_type_dict.items():
            if re.match(token_value, token):
                return token_type_str
    return "UNKNOWN"

def get_tokens(input):
    lexer = lex.lex()
    lexer.input(input)

    token_table = []

    while True:
        tok = lexer.token()
        if not tok: 
            break
        token_table.append(Tok(identify_token_type(str(tok.value)), tok.type, tok.value, tok.lineno, tok.lexpos, tok.lexpos+(len(str(tok.value)))))
    return token_table
