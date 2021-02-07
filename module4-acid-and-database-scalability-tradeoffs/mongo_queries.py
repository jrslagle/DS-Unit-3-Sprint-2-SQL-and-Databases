import sqlite3
import pymongo
import os
from dotenv import load_dotenv
from pprintpp import pprint


def create_mongodb_connection():
    DB_USER = os.getenv("MONGO_USER", default="OOPS")
    DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
    CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")
    DB_NAME = os.getenv("MONGO_DB", default="OOPS")

    # client = pymongo.MongoClient("mongodb+srv://jrslagle:<password>@cluster0.ticlc.mongodb.net/<dbname>?retryWrites=true&w=majority")  # example that Mongo provides
    mongo_client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.ticlc.mongodb.net/{DB_NAME}?retryWrites=true&w=majority") # &ssl=true") # &ssl_cert_reqs=CERT_NONE")
    return mongo_client

if __name__ == "__main__":

    # Open a connection
    mongo_client = create_mongodb_connection()
    db = mongo_client.rgb_characters

    # How many total documents are there?
    doc_count = db.rgb_characters.count_documents({})
    print(f"Counted {doc_count} documents on your MongoDB cluster")

    # How many total Characters are there?
    character_count = db.rgb_characters.count_documents({ 'name': { "$exists": True } })
    print(f"There are {character_count} characters")

    # How many total Items?
    characters_with_items = list(db.rgb_characters.find({ 'items': { "$exists": True } }))
    nested_list_of_items = [character['items'] for character in characters_with_items]
    list_of_items = [item for character_items in nested_list_of_items for item in character_items]
    print(f"Characters have many items: {list_of_items[:3]}")
    item_count = len(list_of_items)
    print(f"All characters together have a total of {item_count} items.")

    # How many of the Items are weapons? How many are not?
    characters_with_weapons = list(db.rgb_characters.find({ 'weapons': { "$exists": True } }))
    nested_list_of_weapons = [character['weapons'] for character in characters_with_weapons]
    list_of_weapons = [item for character_weapons in nested_list_of_weapons for item in character_weapons]
    print(f"Characters have many weapons too: {list_of_weapons[:3]}")
    weapon_count = len(list_of_weapons)
    print(f"All characters together have a total of {weapon_count} weapons.")
    weapon_portion = weapon_count/item_count
    print(f"This means that {100*weapon_portion:.2f}% of items are weapons (and {100*(1-weapon_portion):.2f}% are not).")

    # How many Items does each character have? (Return first 20 rows)
    characters_with_items = list(db.rgb_characters.find({ 'items': { "$exists": True } }))
    for character in characters_with_items[:20]:
        print(f"{character['name']} has {len(character['items'])} items")

    # How many Weapons does each character have? (Return first 20 rows)
    characters_with_weapons = list(db.rgb_characters.find({ 'weapons': { "$exists": True } }))
    for character in characters_with_weapons[:20]:
        print(f"{character['name']} has {len(character['weapons'])} weapons")

    # On average, how many Items does each Character have?
    print(f"On average, each character has {item_count/character_count:.2f} items.")

    # On average, how many Weapons does each character have?
    print(f"On average, each character has {weapon_count/character_count:.2f} weapons.")