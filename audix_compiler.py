def generate_code_recursive(symbol_table, code=None):
    code = ""
    for symbol in symbol_table.table:
        if symbol.tok.stype == "types" or symbol.tok.stype == "functions" or symbol.tok.token == "NOTA":
            code += "\n"
            code += symbol.tok.token + " "
            for key, value in symbol.prop.items():
                 code += value + " "
        if symbol.children is not None:
            code += generate_code_recursive(symbol.children)
    return code

def generate_code_x(code):
    new_code = ""
    temp = ""
    p_temp = ""

    def get_voices(code):
        voices = []
        for line in code.split('\n'):
            if "VOZ" in line:
                voices.append(line.split('=')[0])
        return ','.join(voices)

    for line in code.split('\n'):
        if line.startswith("PATRON"):
            temp = line.replace(" ", "_")
        if line.startswith("PISTA"):
            temp = f"\ndef {line.split(' ')[1]}():"
        if line.startswith("PLAY"):
            new_code += temp + f"\n\treproducir(({get_voices(new_code)}), 128, 75)"
        if line.startswith("VOZ"):
            p_temp = "\n" + temp
            new_code += p_temp + line.replace(" ", "_") + "=("
        if line.startswith("NOTA"):
            temp_line = line.replace("NOTA ", "")
            temp_line = "(\"" + temp_line.split(" ")[0] + "\"" +","+temp_line.split(" ")[1] + "),"
            new_code += " " + temp_line

    new_code = "from audio import reproducir" + new_code
    new_code = new_code.split('\n')
    for line in new_code:
        if "VOZ" in line:
            line = line[:-1] + ")"
    new_code = '\n'.join(new_code)
    return new_code

def generate_code(symbol_table):
    code = generate_code_recursive(symbol_table)
    a = generate_code_x(code)
    print(a)
    pass
