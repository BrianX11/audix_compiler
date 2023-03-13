import ply.yacc as yacc
from symbol_table import Symbol, SymbolTable
import audix_semantic
from audix_lex import tokens, lexer

start = "start"

grammar = '''
start : program

program : pista program
        | patron program
        | pista
        | patron

pista : PISTA ID LCURLY pista_bloque RCURLY

pista_bloque : funcion
            | pista_bloque funcion

funcion : PLAY ID

patron : PATRON ID LCURLY patron_bloque RCURLY

patron_bloque : voz 
            | patron_bloque voz

voz : VOZ ID LCURLY voz_bloque RCURLY

voz_bloque : NOTA FRACCION
            | voz_bloque NOTA FRACCION
'''

def get_rules(grammar):
    lines = grammar.split('\n') 
    i = 0
    
    while i < len(lines) - 1:
        lines[i] = lines[i].strip()
        if lines[i+1].lstrip().startswith('|'):
            lines[i] = lines[i].strip() + '\n\t' +  lines[i+1].strip()
            lines.pop(i+1)
        elif lines[i].strip() == '':
            lines.pop(i)
        else:
            i += 1
    return lines
  
rules = get_rules(grammar)
for rule in rules:
    if(rule.strip()==''):
        continue
    name = rule.split(':')[0].strip()
    exec(f"def p_{name}(p):\n\t'''{rule}'''\n\tpass\n")

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def build_symbol_table(tokens, parent=None):
    symbol_table = SymbolTable()
    i = 0
    while True:
        if tokens:
            token = tokens.pop(0)
        else:
            break
        if token.stype == "types":
            i=0
            symbol_table.add(Symbol("FUNC", token, parent))
        if token.token == "NOTA": 
            symbol_table.add(Symbol("NOTA", token, parent))
        if token.stype == "functions":
            symbol_table.add(Symbol("CALL", token, parent))
        elif token.stype == "ID":
            symbol_table.table[-1].add_prop("name", token.value)
        elif token.stype == "data_types":
            symbol_table.table[-1].add_prop(f"arg{i}", token.value)
            i+=1
        elif token.token == "LCURLY":
            symbol_table.table[-1].children = build_symbol_table(tokens, symbol_table)
        elif token.token == "RCURLY":
            break    
    return symbol_table

def parse(input, token_table):
    r = parser.parse(input=input, lexer=lexer)
    return build_symbol_table(token_table[:])

