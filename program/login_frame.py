#loginframe
import tkinter as tk
import customtkinter as customtk
from database import Database

class LoginFrame(customtk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.username_label = customtk.CTkLabel(self, text="Username")
        self.username_label.pack()

        self.username_entry = customtk.CTkEntry(self)
        self.username_entry.pack()

        self.password_label = customtk.CTkLabel(self, text="Password")
        self.password_label.pack()

        self.password_entry = customtk.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = customtk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack()

        self.result_label = customtk.CTkLabel(self, text="")
        self.result_label.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db = Database()
        cursor = db.connection.cursor()
        query = "SELECT * FROM logintable WHERE username = %s AND passwd = %s"
        cursor.execute(query, (username, password))
  # Error occurs here
        data = cursor.fetchall()
        cursor.close()
        db.close()

        if len(data) == 0:
            self.result_label.configure(text="Invalid username or password")
        else:
            self.result_label.configure(text="Login successful")
            self.master.show_frame("Menu")
