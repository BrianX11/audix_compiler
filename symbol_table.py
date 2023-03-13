from audix_lex import Tok

# Tipos: FUNC, NOTA, CALL

class Symbol:
    def __init__(self, type, tok, parent=None):
        self.type = type
        self.tok = tok
        self.prop = {}
        self.parent = parent
        self.children = None
    
    def add_prop(self, key, value):
        self.prop[key] = value

class SymbolTable:
    def __init__(self):
        self.table = []
    
    def add(self, symbol):
        self.table.append(symbol)