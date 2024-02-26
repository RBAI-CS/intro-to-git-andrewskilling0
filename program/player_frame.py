import tkinter as tk
from tkinter import ttk
import customtkinter as customtk
import mysql.connector  # Import MySQL Connector

class PlayerFrame(customtk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.all_data = None  # Initialize all_data attribute

        self.tree = self.create_tree()
        self.tree.pack(padx=10, pady=10)

        self.button_frame = customtk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.add_button = customtk.CTkButton(self.button_frame, text="Add Player", command=self.add_player)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = customtk.CTkButton(self.button_frame, text="Edit Player", command=self.edit_player)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = customtk.CTkButton(self.button_frame, text="Delete Player", command=self.delete_player)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.back_button = customtk.CTkButton(self, text="Back to Menu", command=self.master.return_to_menu)
        self.back_button.pack()

        self.search_entry = customtk.CTkEntry(self.button_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = customtk.CTkButton(self.button_frame, text="Search", command=self.search_players)
        self.search_button.pack(side=tk.LEFT)

        self.fetch_and_populate()  # Fetch and populate data upon initialization

    def load_data(self):
        # Your MySQL connection details
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="login_database"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_database.players")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return rows  # Return the fetched data

    def fetch_and_populate(self):
        self.all_data = self.load_data()
        self.populate_playertreeview(self.all_data)

    def create_tree(self):
        tree = ttk.Treeview(self, columns=('PlayerID', 'Player_Firstname', 'Player_Lastname', 'Player_DOB', 'Player_Phonenum', 'Player_postion'), show='headings')
        tree.heading('PlayerID', text='PlayerID')
        tree.heading('Player_Firstname', text='Players Firstname')
        tree.heading('Player_Lastname', text='Players Lastname')
        tree.heading('Player_DOB', text='DOB')
        tree.heading('Player_Phonenum', text='Phonenumber')
        tree.heading('Player_postion', text='Postion')
        return tree

    def populate_playertreeview(self, data):
        for record in data:
            self.tree.insert('', 'end', values=record)

    def add_player(self):
        add_window = customtk.CTkToplevel(self)
        add_window.title("Add Player")

        labels = ['First Name', 'Last Name', 'DOB', 'Phone Number', 'Position']
        entries = {}
        for idx, label in enumerate(labels):
            customtk.CTkLabel(add_window, text=label).grid(row=idx, column=0)
            entries[label] = tk.Entry(add_window)
            entries[label].grid(row=idx, column=1)

        def save_player():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Password123",
                database="login_database"
            )
            cursor = conn.cursor()

            values = [entries[label].get() for label in labels]
            cursor.execute("INSERT INTO players (Player_Firstname, Player_Lastname, Player_DOB, Player_Phonenum, Player_postion) VALUES (%s, %s, %s, %s, %s)", values)

            conn.commit()
            cursor.close()
            conn.close()

            self.tree.delete(*self.tree.get_children())
            self.fetch_and_populate()  # Refresh the player list after adding a new player
            add_window.destroy()
        customtk.CTkButton(add_window, text="Save", command=save_player).grid(row=len(labels), columnspan=2)

    def edit_player(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, 'values')
        if not item_values:
            return

        edit_window = customtk.CTkToplevel(self)
        edit_window.title("Edit Player")

        labels = ['PlayerID','First Name', 'Last Name', 'DOB', 'Phone Number', 'Position']
        entries = {}
        for idx, label in enumerate(labels):
            customtk.CTkLabel(edit_window, text=label).grid(row=idx, column=0)
            entries[label] = customtk.CTkEntry(edit_window)
            entries[label].grid(row=idx, column=1)
            entries[label].insert(tk.END, item_values[idx])

        def update_player():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Password123",
                database="login_database"
            )
            cursor = conn.cursor()

            values = [entries[label].get() for label in labels]
            cursor.execute("UPDATE players SET Player_Firstname = %s, Player_Lastname = %s, Player_DOB = %s, Player_Phonenum = %s, Player_postion = %s WHERE PlayerID = %s", 
                           (values[1], values[2], values[3], values[4], values[5], item_values[0]))

            conn.commit()
            cursor.close()
            conn.close()

            self.tree.delete(*self.tree.get_children())

            
            self.fetch_and_populate()  # Refresh the player list after updating player information
            edit_window.destroy()
        update_button = customtk.CTkButton(edit_window, text="Update", command=update_player)
        update_button.grid(row=len(labels), columnspan=2)

    def delete_player(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, 'values')
        if not item_values:
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="login_database"
        )
        cursor = conn.cursor()

        cursor.execute("DELETE FROM players WHERE PlayerID = %s", (item_values[0],))

        conn.commit()
        cursor.close()
        conn.close()

        self.tree.delete(*self.tree.get_children())

        self.fetch_and_populate()

    def search_players(self):
        # Here you can implement the functionality to search players
        # For example:
        search_term = self.search_entry.get().lower()
        filtered_data = [row for row in self.all_data if any(str(value).lower().find(search_term) != -1 for value in row)]
        self.tree.delete(*self.tree.get_children())
        self.populate_playertreeview(filtered_data)
