import re

types = {
    "PISTA": "pista", 
    "PATRON": "patron",
    "VOZ": "voz"
}

data_types = {
    "FRACCION": r'(?:[1-9][0-9]*|0)(?:\/[1-9][0-9]*)?',
    "NOTA": r'[A-G][b#]?\d|S0',
    "INSTRUMENTO": r"sine|square|triangle|saw"
}

functions = {
    "PLAY": "play"
}

ignore = {
    "ignore": re.escape(" \t\r\n\f"),
    "ignore_COMMENT": r'\#.*',
}

delimiters = {  
    "LCURLY": r"\{",
    "RCURLY": r"\}",
}

token_arr = {**delimiters, **functions, **data_types, **ignore, **types}

token_types = {
    "types": types,
    "data_types": data_types, 
    "functions": functions,
    "ignore": ignore,
    "delimiters": delimiters,
    "ID": {"ID": r"\b[a-zA-Z_]\w*\b"}
}

token_editor_colors ={
    "types": "#E6E6FA",
    "data_types": "#F0FFFF",
    "functions": "#F5DEB3",
    "params": "#E0EEE0",
    "delimiters": "#F5F5F5",
    "ID": "#FFF0F5",
}