import pymongo
import os
from dotenv import load_dotenv
from pprintpp import pprint

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")
DB_NAME = os.getenv("MONGO_DB", default="OOPS")


# client = pymongo.MongoClient("mongodb+srv://jrslagle:<password>@cluster0.ticlc.mongodb.net/<dbname>?retryWrites=true&w=majority")
client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.ticlc.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
# print(client)
db = client.test_database

collection = db.pokemon_test  # whatever
print("------------")
print("COLLECTION:", type(collection), collection)

# collection.insert_one({
#     'name':'Pikachu',
#     'level': 30,
#     'exp': 76000000000,
#     'hp': 400
# })
print("DOCS:", collection.count_documents({}))
# print(collection.count_documents({}))
# pprint(dir(collection))