import tkinter as tk

class Newsframe(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
    
        self.back_button = tk.Button(self, text="Back to Menu", command=self.master.return_to_menu)
        self.back_button.pack()