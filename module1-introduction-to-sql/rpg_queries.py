import sqlite3
from query import *

class SQL_Interface:
    def __init__(self, db_name="rpg_db.sqlite3"):
        self.conn = sqlite3.connect(db_name)
        self.curs = self.conn.cursor()

    def query(self, query):
        self.curs.execute(query)
        return self.curs.fetchall()
    
    def query_value(self, query):
        return self.query(query)[0][0]

if __name__ == "__main__":
    rpg = SQL_Interface(db_name="rpg_db.sqlite3")
    
    print("In the RPG Data:")
    print(f"There are {rpg.query_value(TOTAL_CHARACTERS)} total characters which have chosen these classes:")
    for subclass in ['necromancer','mage','thief','cleric','fighter']:
        print(f"{subclass}s = {rpg.query_value(CLASS+subclass)}")

    print(f"\nThere are {rpg.query_value(TOTAL_ITEMS)} total items: {rpg.query_value(WEAPONS)} weapons and {rpg.query_value(NON_WEAPONS)} non-weapons.")
    print(f"On average, each character has {rpg.query_value(AVG_CHARACTER_ITEMS):.2f} items and {rpg.query_value(AVG_CHARACTER_WEAPONS):.2f} weapons.\n")

    print("The first 20 characters have:")
    print(f"{'Name':30}Items")
    item_counts = rpg.query(CHARACTER_ITEMS)
    for name, items in item_counts:
        print(f"{name:30}{items:5}")

    print("\nThe first 20 characters have:")
    print(f"{'Name':30}Weapons")
    item_counts = rpg.query(CHARACTER_WEAPONS)
    for name, weapons in item_counts:
        print(f"{name:30}{weapons:7}")

