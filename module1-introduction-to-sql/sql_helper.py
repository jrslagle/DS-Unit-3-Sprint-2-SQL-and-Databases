import sqlite3

class SQL_Interface:
    def __init__(self, db_name="rpg_db.sqlite3"):
        self.conn = sqlite3.connect(db_name)
        self.curs = self.conn.cursor()

    def query(self, query):
        self.curs.execute(query)
        return self.curs.fetchall()
    
    def query_value(self, query):
        return self.query(query)[0][0]