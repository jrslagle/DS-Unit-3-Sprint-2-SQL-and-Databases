import sqlite3

class SQL_Interface:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def post_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def get_value(self, query):
        return self.get_query(query)[0][0]

    def get_tables(self):
        tables = self.get_value("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        return [table[0] for table in tables]

    def get_create_query(self, table):
        create_query = self.get_value(f"SELECT sql FROM sqlite_master WHERE name='{table}';")
        return create_query+';'

    def get_columns(self, table):
        table_info = self.get_query(f"PRAGMA table_info({table});")
        return [column[1] for column in table_info]

    def print_table(self, columns, values):
        print(''.join([f"{name:{width}}" for name, width in columns.items()]))
        widths = list(columns.values())
        for row in values:
            print(''.join([f"{value:{width}}" for value, width in zip(row, widths)]))

    def teardown(self):
        self.cursor.close()
        self.connection.close()