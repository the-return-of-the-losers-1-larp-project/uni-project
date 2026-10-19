import sqlite3
import pandas as pd
from pandasql import sqldf
import os
import data.cleanup_data
import config

def load_data():
    # generate the database file if it's not there already
    if not os.path.exists(config.DATA_DB_PATH):
        data.cleanup_data.clean_up()

    with sqlite3.connect(config.DATA_DB_PATH) as conn:
        return pd.read_sql("SELECT * FROM data", conn)

