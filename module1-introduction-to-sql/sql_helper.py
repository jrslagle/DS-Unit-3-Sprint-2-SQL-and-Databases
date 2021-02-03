import sqlite3

class SQL_Interface:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def query_value(self, query):
        return self.query(query)[0][0]