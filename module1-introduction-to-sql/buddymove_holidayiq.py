import pandas as pd
from sql_helper import SQL_Interface
from query import *

if __name__ == "__main__":
    # Load buddymove_holidayiq.csv into a pandas df (you should have a shape of 249,7 and 0 nulls)
    df = pd.read_csv("buddymove_holidayiq.csv")
    print(df.head())
    print(f"Shape = {df.shape}")
    print(f"Nulls = {df.isna().sum().sum()}")


    # rpg = SQL_Interface(db_name="buddymove_holidayiq.sqlite3")

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    # insert the dataframe into a new table called "review"

    # count the rows in review. should be 249
    ROW_COUNT = """
    SELECT COUNT(*)
    FROM review
    """

    # How many users who reviewed at least 100 Nature in the category also reviewed at least 100 in the Shopping category?

    # (Stretch) What are the average number of reviews for each category?
    
    # print("In the RPG Data:")
    # print(f"There are {rpg.query_value(TOTAL_CHARACTERS)} total characters which have chosen these classes:")
    # for subclass in ['necromancer','mage','thief','cleric','fighter']:
    #     print(f"{subclass}s = {rpg.query_value(CLASS+subclass)}")
