import audix_compiler

def get_id_list(symbol_table):
    id_list = []
    for symbol in symbol_table.table:
        if symbol.tok.stype == 'types':
            if symbol.prop:
                if "name" in symbol.prop:
                    id_list.append(symbol.prop['name'])
    return id_list

def check_duplicate_id(id_list):
    for i in range(len(id_list)):
        for j in range(i+1, len(id_list)):
            if id_list[i] == id_list[j]:
                print(f"Error: ID duplicado '{id_list[i]}'")
                return False
    return True

def check_id_exist(id_list, id):
    for i in id_list:
        if i == id:
            return True
    return False

def check_call_args(symbol_table):
    exists = False
    for symbol in symbol_table.table:
        if symbol.type == "CALL":
            if symbol.prop:
                if "name" in symbol.prop:
                    exists = check_id_exist(get_id_list(symbol_table), symbol.prop['name'])
                    if not exists:
                        parent = symbol.parent
                        while parent:
                            id_list = get_id_list(parent)
                            exists = check_id_exist(id_list, symbol.prop['name'])
                            if exists:
                                break
                            parent = parent.table[-1].parent
                    if not exists:
                        print(f"Error: ID no existe '{symbol.prop['name']}'")
    return exists

def recursive_check(symbol_table):
    valid = True
    valid = check_rules(symbol_table)
    
    for symbol in symbol_table.table:
        if symbol.children:
            valid = recursive_check(symbol.children)
    return valid

def check_rules(symbol_table):
    id_list = get_id_list(symbol_table)

    valid = True

    valid = check_duplicate_id(id_list)
    valid = check_call_args(symbol_table)
    return valid

def check(symbol_table):
    audix_compiler.generate_code(symbol_table)
    return recursive_check(symbol_table)

