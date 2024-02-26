import tkinter as tk
import customtkinter as customtk
from login_frame import LoginFrame
from menu_frame import MenuFrame
from player_frame import PlayerFrame
from Fixture import FixtureFrame
from shop_frame import ShopFrame
from news_frame import Newsframe
from database import Database

class Application(customtk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("600x400")

        customtk.set_appearance_mode("system")
        customtk.set_default_color_theme("blue")

        self.frames = {
            "Login": LoginFrame(self),
            "Menu": MenuFrame(self),
            "Player": PlayerFrame(self),
            "Fixture": FixtureFrame(self),
            "Shop": ShopFrame(self),
            "News":Newsframe(self)

        }

        for frame in self.frames.values():
            frame.pack(fill=tk.BOTH, expand=True)

        self.show_frame("Login")

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill=tk.BOTH, expand=True)

    def return_to_menu(self):  # Define the return_to_menu method
        self.show_frame("Menu")
    
    def search_players(self):
        search_term = self.frames["Player"].search_entry.get().lower()  # Accessing search_entry from PlayerFrame
        all_data = self.frames["Player"].all_data  # Accessing all_data from PlayerFrame
        filtered_data = [row for row in all_data if any(str(value).lower().find(search_term) != -1 for value in row)]
        self.frames["Player"].populate_playertreeview(filtered_data) 


        

if __name__ == "__main__":
    app = Application()
    app.mainloop()
