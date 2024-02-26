import tkinter as tk
from tkinter import ttk
import mysql.connector

class FixtureFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.treeview = self.create_treeview()

        self.display_fixtures()

        add_button = tk.Button(self, text="Add Fixture", command=self.add_fixture)
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(self, text="Edit Fixture", command=self.edit_fixture)
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(self, text="Delete Fixture", command=self.delete_fixture)
        delete_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(self, text="Back to Menu", command=self.master.return_to_menu)
        back_button.pack()

    def create_treeview(self):
        tree = ttk.Treeview(self, columns=('Date', 'Home Team', 'Score', 'Away Team'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Home Team', text='Home Team')
        tree.heading('Score', text='Score')
        tree.heading('Away Team', text='Away Team')
        tree.pack(fill='both', expand=True)
        return tree

    def get_fixtures_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="login_database"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fixtures")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def populate_fixturetreeview(self, data):
        self.treeview.delete(*self.treeview.get_children())
        for record in data:
            self.treeview.insert('', 'end', values=record)

    def display_fixtures(self):
        fixtures_data = self.get_fixtures_data()
        self.populate_fixturetreeview(fixtures_data)

    def add_fixture(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Fixture")

        labels = ['Date', 'Home Team', 'Score', 'Away Team']
        entries = {}
        for idx, label in enumerate(labels):
            tk.Label(add_window, text=label).grid(row=idx, column=0)
            entries[label] = tk.Entry(add_window)
            entries[label].grid(row=idx, column=1)

        def save_fixture():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Password123",
                database="login_database"
            )
            cursor = conn.cursor()

            values = [entries[label].get() for label in labels]
            cursor.execute("INSERT INTO fixtures (Date, Home_Team, Score, Away_Team) VALUES (%s, %s, %s, %s)", values)

            conn.commit()
            cursor.close()
            conn.close()

            add_window.destroy()
            self.display_fixtures()

        save_button = tk.Button(add_window, text="Save", command=save_fixture)
        save_button.grid(row=len(labels), columnspan=2)

    def edit_fixture(self):
        def edit_selected():
            selected_item = self.treeview.selection()
            if not selected_item:
                return

            item_values = self.treeview.item(selected_item, 'values')
            if not item_values:
                return

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Fixture")

            labels = ['Date', 'Home Team', 'Score', 'Away Team']
            entries = {}
            for idx, label in enumerate(labels):
                tk.Label(edit_window, text=label).grid(row=idx, column=0)
                entries[label] = tk.Entry(edit_window)
                entries[label].grid(row=idx, column=1)
                entries[label].insert(tk.END, item_values[idx])

            def update_fixture():
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Password123",
                    database="login_database"
                )
                cursor = conn.cursor()

                values = [entries[label].get() for label in labels]
                cursor.execute("UPDATE fixtures SET Date = %s, Home_Team = %s, Score = %s, Away_Team = %s WHERE Date = %s AND Home_Team = %s AND Score = %s AND Away_Team = %s", 
                            (values[0], values[1], values[2], values[3], item_values[0], item_values[1], item_values[2], item_values[3]))

                conn.commit()
                cursor.close()
                conn.close()

                edit_window.destroy()
                self.display_fixtures()

            update_button = tk.Button(edit_window, text="Update", command=update_fixture)
            update_button.grid(row=len(labels), columnspan=2)

        edit_selected()

    def delete_fixture(self):
        
        def delete_selected():
            selected_item = self.treeview.selection()
            if not selected_item:
                return

            item_values = self.treeview.item(selected_item, 'values')
            if not item_values:
                return

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Password123",
                database="login_database"
            )
            cursor = conn.cursor()

            cursor.execute("DELETE FROM fixtures WHERE Date = %s AND Home_Team = %s AND Score = %s AND Away_Team = %s", item_values)

            conn.commit()
            cursor.close()
            conn.close()

            self.display_fixtures()

        delete_selected()
