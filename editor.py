from tkinter import ttk, filedialog
from editor_tooltip import Tooltip
from tokens_dict import token_types, token_editor_colors

import tkinter as tk
import uuid

class Editor:
    def __init__(self, master):
        self.master = master
        self.master.title("Compilador Audix")
        #self.master.state('zoomed')
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.minimized_width = int(self.screen_width // 1.4)
        self.minimized_height = int(self.screen_height // 1.4)
        self.master.minsize(self.minimized_width, self.minimized_height)
        
        self.text = tk.Text(self.master, undo=True, maxundo=-1, autoseparators=True)
        self.text.pack(expand=True, fill="both")
        self.scrollbar = tk.Scrollbar(self.text)
        self.scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side="top", fill="x")

        self.open_button = ttk.Button(self.toolbar, text="Open File", command=self.open_file)
        self.open_button.pack(side="left")

        self.lex_button = ttk.Button(self.toolbar, text="Analizador Lexico", command=self.on_lex_button_click)
        self.lex_button.pack(side="left")

        self.parse_button = ttk.Button(self.toolbar, text="Analizador Sintactico", command=self.on_parse_button_click)
        self.parse_button.pack(side="left")

        self.semantic_button = ttk.Button(self.toolbar, text="Analizador Semantico", command=self.on_semantic_button_click)
        self.semantic_button.pack(side="left")

        self.token_table = None

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                file_contents = file.read()
                self.text.delete("1.0", "end")
                self.text.insert("end", file_contents)

    def on_lex_button_click(self):

        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        import audix_lex
        self.token_table = audix_lex.get_tokens(self.text.get("1.0", "end"))
        for tok in self.token_table:
            self.highlight_token(tok.token, tok.stype, tok.start, tok.end, tok.line)

    def on_parse_button_click(self):
        if self.token_table is not None:
            import audix_yacc
            self.symbol_table = audix_yacc.parse(self.text.get("1.0", "end"), self.token_table)
        else:
            print("No hay tokens")
    
    def on_semantic_button_click(self):
        if self.token_table is not None:
            import audix_semantic
            if audix_semantic.check(self.symbol_table):
                pass
            else:
                print("Hay errores en el codigo")
        else:
            print("No hay tokens")

    def highlight_token(self, token, type, start_position, end_position, line_number):
        start_index = self.text.index(f"1.0+{start_position}c")
        end_index = self.text.index(f"1.0+{end_position}c")
        uu = uuid.uuid4()

        tp_message = f"TOKEN:{token}\nTYPE:{type}\nLSE:({line_number},{start_index.split('.')[1]},{end_index.split('.')[1]})"
        
        tip = Tooltip(self.text, tp_message)
        self.text.tag_add(uu, start_index, end_index)
        self.text.tag_configure(uu, background=token_editor_colors[type])
        self.text.tag_bind(uu, "<Enter>", tip.enter)
        self.text.tag_bind(uu, "<Leave>", tip.leave)
