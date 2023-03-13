import tkinter as tk

class Tooltip:
    active_tip = None

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        self.id = None
        self.x = self.y = 0
        
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        if Tooltip.active_tip:
            Tooltip.active_tip.hide_tip()
        self.show_tip(event.x_root + 10, event.y_root + 10)

    def leave(self, event=None):
        self.hide_tip()

    def show_tip(self, x, y):
        if self.tip:
            return
        self.x, self.y = x, y
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tip, text=self.text, justify=tk.LEFT,
                         background="#FFFFFF", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
        Tooltip.active_tip = self

    def hide_tip(self):
        if self.tip:
            self.tip.destroy()
        self.tip = None