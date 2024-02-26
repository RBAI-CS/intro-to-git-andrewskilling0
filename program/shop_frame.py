import tkinter as tk
from tkinter import ttk
import customtkinter as customtk
import mysql.connector
from tkinter import filedialog

class ShopFrame(customtk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.shop_treeview = None
        self.create_treeview()
        self.display_shop_items()

        self.button_frame = customtk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.add_button = customtk.CTkButton(self.button_frame, text="Add Item", command=self.add_shop_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = customtk.CTkButton(self.button_frame, text="Edit Item", command=self.edit_shop_item)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = customtk.CTkButton(self.button_frame, text="Delete Item", command=self.delete_shop_item)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def get_shop_items(self):
        # Your MySQL connection details
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="login_database"
        )
        cursor = conn.cursor()

        # Fetch data from the shop table
        cursor.execute("SELECT * FROM shop")
        shop_data = cursor.fetchall()

        cursor.close()
        conn.close()

        return shop_data

    def populate_treeview(self, data):
        for item in data:
            self.shop_treeview.insert('', 'end', values=item)

    def display_shop_items(self):
        shop_items = self.get_shop_items()
        for child in self.shop_treeview.get_children():
            self.shop_treeview.delete(child)
        self.populate_treeview(shop_items)

    def create_treeview(self):
        self.shop_treeview = ttk.Treeview(self, columns=('ItemID', 'ItemName', 'Price', 'ItemPhoto'))
        self.shop_treeview.heading('ItemID', text='Item ID')
        self.shop_treeview.heading('ItemName', text='Item Name')
        self.shop_treeview.heading('Price', text='Price')
        self.shop_treeview.heading('ItemPhoto', text='Item Photo')
        self.shop_treeview.pack()

    def add_shop_item(self):
        add_window = customtk.CTkToplevel(self)
        add_window.title("Add Item")

        labels = ['ItemID', 'ItemName', 'Price','ItemPhoto']
        entries = {}
        for idx, label in enumerate(labels):
            customtk.CTkLabel(add_window, text=label).grid(row=idx, column=0)
            entries[label] = customtk.CTkEntry(add_window)
            entries[label].grid(row=idx, column=1)

        def select_photo():
            filename = filedialog.askopenfilename()
            if filename:
                entries['ItemPhoto'].insert(0, filename)

        photo_button = customtk.CTkButton(add_window, text="Select Photo", command=select_photo)
        photo_button.grid(row=len(labels), column=3, columnspan=2)
        
            

        def save_shop_item():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Password123",
                database="login_database"
            )
            cursor = conn.cursor()

            values = [entries[label].get() for label in labels]
            print(values)
            cursor.execute("INSERT INTO shop (Item_ID, Item_name, Item_price, Item_photo) VALUES (%s, %s, %s, %s)", values)

            conn.commit()
            cursor.close()
            conn.close()

            add_window.destroy()
            self.display_shop_items()

        save_button = customtk.CTkButton(add_window, text="Save", command=save_shop_item)
        save_button.grid(row=len(labels), columnspan=2)
    
    def edit_shop_item(self):
        selected_item = self.shop_treeview.selection()
        if not selected_item:
            return
       

        item_values = self.shop_treeview.item(selected_item, 'values')

        edit_window = customtk.CTkToplevel(self)
        edit_window.title("Edit Item")

        labels = ['ItemID', 'ItemName', 'Price', 'ItemPhoto']
        entries = {}
        for idx, label in enumerate(labels):
            customtk.CTkLabel(edit_window, text=label).grid(row=idx, column=0)
            entries[label] = customtk.CTkEntry(edit_window)
            entries[label].grid(row=idx, column=1)
            entries[label].insert(tk.END, item_values[idx])

        def select_photo():
            filename = filedialog.askopenfilename()
            if filename:
                entries['ItemPhoto'].insert(0, filename)

        photo_button = customtk.CTkButton(edit_window, text="Select Photo", command=select_photo)
        photo_button.grid(row=len(labels), column=3, columnspan=2)

        def update_shop_item():
            conn = mysql.connector.connect(
            host="localhost",
                user="root",
                password="Password123",
                database="login_database"
            )
            cursor = conn.cursor()

            values = [entries[label].get() for label in labels]
            cursor.execute("UPDATE shop SET Item_name = %s, Item_price = %s, Item_photo = %s WHERE Item_ID = %s", 
                        (values[1], values[2], values[3], values[0]))

            conn.commit()
            cursor.close()
            conn.close()

            edit_window.destroy()
            self.display_shop_items()

        update_button = customtk.CTkButton(edit_window, text="Update", command=update_shop_item)
        update_button.grid(row=len(labels), columnspan=2)

    def delete_shop_item(self):
        selected_item = self.shop_treeview.selection()
        if not selected_item:
            return

        item_values = self.shop_treeview.item(selected_item, 'values')

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="login_database"
        )
        cursor = conn.cursor()

        cursor.execute("DELETE FROM shop WHERE ItemID = %s", (item_values[0],))

        conn.commit()
        cursor.close()
        conn.close()

        self.display_shop_items()




