#menuframe
import tkinter as tk
import customtkinter as customtk

class MenuFrame(customtk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.player_button = customtk.CTkButton(self, text="Player", command=lambda: self.master.show_frame("Player"))
        self.player_button.pack()

        self.player_button = customtk.CTkButton(self, text="Fixture", command=lambda: self.master.show_frame("Fixture"))
        self.player_button.pack()

        self.player_button = customtk.CTkButton(self, text="News", command=lambda: self.master.show_frame("News"))
        self.player_button.pack()

        self.player_button = customtk.CTkButton(self, text="Shop", command=lambda: self.master.show_frame("Shop"))
        self.player_button.pack()

        
