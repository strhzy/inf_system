import sqlite3

class SQLiteDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_text = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_text})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def select_data(self, table_name, condition=None):
        if condition!=None:
            query = f"SELECT * FROM {table_name} WHERE {condition}"
        else:
            query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, table_name, data, condition):
        set_values = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values())
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_data(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
