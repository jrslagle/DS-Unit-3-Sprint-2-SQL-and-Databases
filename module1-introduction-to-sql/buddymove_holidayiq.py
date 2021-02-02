import pandas as pd
from sql_helper import SQL_Interface
from query import *

if __name__ == "__main__":
    # Load buddymove_holidayiq.csv into a pandas df (you should have a shape of 249,7 and 0 nulls)
    df = pd.read_csv("buddymove_holidayiq.csv")
    print(df.head())
    print(f"Shape = {df.shape}")
    print(f"Nulls = {df.isna().sum().sum()}")


    buddy_db = SQL_Interface(db_name="buddymove_holidayiq.sqlite3")

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    # insert the dataframe into a new table called "review"
    df.to_sql("review", con=buddy_db.connection, if_exists='replace')

    # count the rows in review. should be 249
    ROW_COUNT = """
    SELECT COUNT(*)
    FROM review
    """
    row_count = buddy_db.query_value(ROW_COUNT)
    print(f"The new review table has {row_count} rows.")
    assert row_count == 249

    # How many users who reviewed at least 100 Nature in the category also reviewed at least 100 in the Shopping category?
    NATURE_SHOPPERS = """
    SELECT COUNT(*) AS nature_shoppers --review.Nature, review.Shopping
    FROM review
    WHERE Nature >= 100
    AND Shopping >=100
    """
    nature_shoppers = buddy_db.query_value(NATURE_SHOPPERS)
    print(f"{nature_shoppers} users made at least 100 Nature and Shopping reviews.")

    # (Stretch) What are the average number of reviews for each category?
    print("Column     Average")
    for column in ['User Id', 'Sports', 'Religious', 'Nature', 'Theatre', 'Shopping', 'Picnic']:
        query = f'SELECT AVG(review."{column}") FROM review'
        print(f"{column:10} {buddy_db.query_value(query):.1f}")
    