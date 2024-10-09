import tkinter as tk
from gui import SancharSaathiGUI
from form_filler import fill_sanchar_saathi_form

def submit_form(data):
    fill_sanchar_saathi_form(data)

if __name__ == "__main__":
    root = tk.Tk()
    app = SancharSaathiGUI(root)
    app.set_submit_callback(submit_form)
    root.mainloop()