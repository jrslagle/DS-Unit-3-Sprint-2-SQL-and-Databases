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

    # client = pymongo.MongoClient("mongodb+srv://jrslagle:<password>@cluster0.ticlc.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mongo_client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.ticlc.mongodb.net/{DB_NAME}?retryWrites=true&w=majority") # &ssl=true") # &ssl_cert_reqs=CERT_NONE")
    return mongo_client

def get_query(cursor, query):
    """Create cursor, query, fetch, close cursor, return"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_character_ids(cursor):
    """get list of character id's"""
    query = "SELECT character_id FROM charactercreator_character;"
    result = get_query(cursor, query)
    character_ids = [row[0] for row in result]
    return character_ids
    

# For each character
def make_character_document(rpg_cursor, character_id):
    # tables_of_interest = ['charactercreator_character_inventory', 'armory_item', 'armory_weapon']
    main_stats_query = f"SELECT name, level, exp, hp, strength, intelligence, dexterity, wisdom FROM charactercreator_character WHERE character_id = {character_id};"
    main_stats = get_query(rpg_cursor, main_stats_query)[0]

    # get a character's items
    items_query = """SELECT items.name
        FROM charactercreator_character_inventory as inventory, armory_item as items
        WHERE inventory.character_id = {}
        AND inventory.item_id = items.item_id;""".format(character_id)
    items = get_query(rpg_cursor, items_query)
    items = [item[0] for item in items]

    # get a character's weapons
    weapon_query = """
        SELECT weapon.name
        FROM (
            SELECT w.item_ptr_id as id, item.name as name
            FROM 
                armory_weapon as w,
                armory_item as item
            WHERE item.item_id = w.item_ptr_id
            ) as weapon,
            charactercreator_character_inventory AS inventory
        WHERE inventory.item_id = weapon.id
        AND inventory.character_id = {};
        """.format(character_id)
    weapons = get_query(rpg_cursor, weapon_query)
    if len(weapons) > 0:
        weapons = [weapon[0] for weapon in weapons]
    
    character_document = {
        "name": main_stats[0],
        "level": main_stats[1],
        "exp": main_stats[2],
        "hp": main_stats[3],
        "strength": main_stats[4],
        "intelligence": main_stats[5],
        "dexterity": main_stats[6],
        "wisdom": main_stats[7],
        "items": items,
        "weapons": weapons,
    }

    return character_document

def upload_documents(database, documents):
    database.test2.insert_many(documents)

    # get the CREATE query for all the columns
    # rpg_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
    # create = rpg_cursor.fetchone()[0]
    # create = create.replace(' AUTOINCREMENT','')  # autoincrement is implied and throws a syntax error
    # create = create.replace(' datetime',' timestamp')
    # print(create)
    
    # get the data in the rows
    # rpg_cursor.execute("SELECT * FROM %s;" %table)
    # rows = rpg_cursor.fetchall()

    # if len(rows) > 0:
    #     column_count = len(rows[0])
    #     place_holder = '%s,'*column_count
    #     new_holder = place_holder[:-1]
    # else:
    #     column_count = 0
    #     place_holder = ''
    #     new_holder = '%s,'
    # print(f"{table} has {column_count} columns")
    # try:
        

    #     db.test.insert_one(character_document)


    #     elephant_cursor = elephant_connection.cursor()
    #     elephant_cursor.execute("DROP TABLE IF EXISTS %s;" %table)
    #     elephant_cursor.execute(create)

    #     # new_holder = '%s,'
    #     elephant_cursor.executemany("INSERT INTO %s VALUES (%s);" % (table, new_holder), rows)
    #     elephant_connection.commit()
    #     print(f"Created {table}")
    # except psycopg2.DatabaseError as e:
    #     print("Error", e)
    #     sys.exit(1)

# db.test.insert_one({'x': 1})

# print(db.test.count_documents({'x': 1}))

# print(list(db.test.find({'x': 1})))

# nick = {
#     'food': 'Mexican',
#     'color': 'Yellow',
#     'city': ['New York', 'Amsterdam']
# }
# nate = {
#     'food': 'Italian',
#     'color': 'Blue',
#     'number': 212
# }
# all_docs = [nick, nate]
# db.test.insert_many(all_docs)

# print(list(db.test.find()))
# print(list(db.test.find({'color':"Blue"})))

# collection = db.pokemon_test  # whatever
# print("------------")
# print("COLLECTION:", type(collection), collection)

# collection.insert_one({
#     'name':'Pikachu',
#     'level': 30,
#     'exp': 76000000000,
#     'hp': 400
# })
# print("DOCS:", collection.count_documents({}))
# print(collection.count_documents({}))
# pprint(dir(collection))

if __name__ == "__main__":
    rpg_connection = sqlite3.connect("module1-introduction-to-sql\\rpg_db.sqlite3")
    rpg_cursor = rpg_connection.cursor()
    character_ids = get_character_ids(cursor=rpg_cursor)
    character_documents = [make_character_document(rpg_cursor, character_id) for character_id in character_ids]
    print(f"Created {len(character_documents)} character documents")
    rpg_connection.close()

    mongo_client = create_mongodb_connection()
    db = mongo_client.test2
    # upload_documents(db, character_documents)
    doc_count = db.test2.count_documents()
    print(f"Counted {doc_count} records on your MongoDB cluster")