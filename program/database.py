# database.py

import mysql.connector

class Database:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="login_database"
        )

    def close(self):
        self.connection.close()

    def fetch_data(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
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

        return rows