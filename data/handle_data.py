import sqlite3
import pandas as pd
from pandasql import sqldf

def get_data():
    with sqlite3.connect("data/data.db") as conn:
        return pd.read_sql("SELECT * FROM data", conn)
