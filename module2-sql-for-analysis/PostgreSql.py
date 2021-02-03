import os
import sys
import sqlite3
import json

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

# Open our connections to Elephant and the RPG data
elephant_connection = psycopg2.connect(
    dbname = os.getenv("ELEPHANT_DB", default="OOPS"),
    user = os.getenv("ELEPHANT_USER", default="OOPS"),
    password = os.getenv("ELEPHANT_PASSWORD", default="OOPS"),
    host = os.getenv("ELEPHANT_HOST", default="OOPS"),
    )
rpg_connection = sqlite3.connect("module1-introduction-to-sql\\rpg_db.sqlite3")
# print("ELEPHANT CONNECTION:", elephant_connection)
# print("RPG CONNECTION:", rpg_connection)

def get_query(connection, query):
    """Create cursor, query, fetch, close cursor, return"""
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def query_value(connection, query):
    return get_query(connection, query)[0][0]

def post_query(connection, query):
    """Create cursor, query, commit, close cursor"""
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()

# Create a new table (if it doesn't exist)
def create_table(connection, table):  # Add signature
    print("---------------")
    create_query = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id SERIAL PRIMARY KEY,
        name varchar(40) NOT NULL,
        data JSONB
    );
    """
    post_query(connection=elephant_connection, query=create_query)

# Insert a set of rows
def insert_rows(connection, table, column_names, values):
    insertion_query = f"INSERT INTO {table} {column_names} VALUES %s"
    cursor = connection.cursor()
    execute_values(cursor, insertion_query, values)
    connection.commit()
    cursor.close()

# Read from a table
def read_table(connection, table, limit):
    query = f'SELECT * from {table} LIMIT {limit};'
    rows = get_query(connection=connection, query=query)
    print("SQL:", query)
    print(f"--TABLE: {table}--")
    for row in rows:
        print(row)


# TOTAL_CHARACTERS = """
# SELECT COUNT(*) as number_of_characters
# FROM charactercreator_character;
# """
# print("In the RPG Data:")
# print(f"There are {query_value(connection=rpg_connection, query=TOTAL_CHARACTERS)} total characters which have chosen these classes:")

# Migrate the SQLite RPG data to my Elephant Postgress server
# Get the rpg table names
rpg_tables_query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
rpg_tables = get_query(connection=rpg_connection, query=rpg_tables_query)
rpg_tables = [table[0] for table in rpg_tables]

# For each table
for table in rpg_tables:
    rpg_cursor = rpg_connection.cursor()
    
    # get the CREATE query for all the columns
    rpg_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
    create = rpg_cursor.fetchone()[0]
    create = create.replace(' AUTOINCREMENT','')  # autoincrement is implied and throws a syntax error
    create = create.replace(' datetime',' timestamp')
    print(create)
    
    # get the data in the rows
    rpg_cursor.execute("SELECT * FROM %s;" %table)
    rows = rpg_cursor.fetchall()

    if len(rows) > 0:
        column_count = len(rows[0])
        place_holder = '%s,'*column_count
        new_holder = place_holder[:-1]
    else:
        column_count = 0
        place_holder = ''
        new_holder = '%s,'
    print(f"{table} has {column_count} columns")
    
    try:
        elephant_cursor = elephant_connection.cursor()
        elephant_cursor.execute("DROP TABLE IF EXISTS %s;" %table)
        elephant_cursor.execute(create)

        # new_holder = '%s,'
        elephant_cursor.executemany("INSERT INTO %s VALUES (%s);" % (table, new_holder), rows)
        elephant_connection.commit()
        print(f"Created {table}")
    except psycopg2.DatabaseError as e:
        print("Error", e)
        sys.exit(1)



# Read the first 10 rows of pg_user
# query = "SELECT usename, usecreatedb, usesuper, passwd FROM pg_user LIMIT 10;"
# read_table(connection=elephant_connection, table='pg_user', limit=10)


# table_name = "table_dspt92"
# create_table(connection=elephant_connection, table=table_name)

# Insert a single row
# my_dict =  {'a': 1, 'b': ['dog', 'cat', 42], 'c': True}
# insertion_query = f"INSERT INTO {table_name} (name, data) VALUES (%s, %s)"
# post_cursor.execute(insertion_query,
#     ('Keep on filling that table...', json.dumps(my_dict))
# )




# list_of_tuples = [
#     ('A rowwwww', 'null'),
#     ('Another row, with JSONNNNN', json.dumps(my_dict)),
#     ('Third row', "3")
#     ]
# insert_rows(connection=elephant_connection, table_name=table_name, column_names='(name, data)', list_of_tuples=list_of_tuples)
    
# read_table(connection=elephant_connection, table=table_name, rows=100)


# Tear down
elephant_connection.close()
rpg_connection.close()