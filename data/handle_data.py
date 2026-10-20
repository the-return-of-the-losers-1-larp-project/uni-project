import sqlite3
import pandas as pd
import os
import data.cleanup_data
import config

def load_data() -> pd.DataFrame:
    # generate the database file if it's not there already
    if not os.path.exists(config.DATA_DB_PATH):
        data.cleanup_data.clean_up()

    with sqlite3.connect(config.DATA_DB_PATH) as conn:
        return pd.read_sql_query("SELECT * FROM data", conn)

def run_sql(query) -> pd.DataFrame:
    with sqlite3.connect(config.DATA_DB_PATH) as conn:
        return pd.read_sql_query(query, conn)