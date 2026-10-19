import csv
import pandas as pd
import sqlite3

def clean_up():
    data = []
    with open("data/data.csv") as f:
        for row in csv.reader(f):
            data.append(row)

    # rows to remove
    # we chose these rows manuanlly since they were sort of outliers of the original data
    # and we believed the exclusion of them would help train the model be more accurate
    to_remove = [1,2,9,13,29,35,39,48,52,55,62,63,67,71,74,75,87,93,97,113,115,126,128,130,131,135,149,150,158,168,169,170,171,177,180,182,186,187,189,190,191,199,214,220,224,227,229,232,238,244,245,261,268,269,271,274,275,277,284,288,290,300,305,307,308,314,316,323,334,338,340,351,352,356,358,367,380,382,386]

    # column datatypes
    datatypes = {
        'clicks': 'int64',
        'median_click_interval_ms': 'int64',
        'click_interval_std_ms': 'int64',
        'mouse_path_curvature': 'float64',
        'mouse_distance_px': 'int64',
        'idle_ratio': 'float64',
        'scroll_entropy': 'float64',
        'digraph_latency_ms': 'int64',
        'dwell_field1_ms': 'int64',
        'dwell_field2_ms': 'int64',
        'dwell_field3_ms': 'int64',
        'session_duration_ms': 'int64',
        'pages_visited': 'int64',
        'timezone_mismatch': 'bool',
        'referrer_type': 'str',
        'webdriver_flag': 'bool',
        'button_hover_ms': 'int64',
        'copy_events': 'int64',
        'viewport_width': 'int64',
        'bot': 'bool'
    }

    new_data = []
    for i, row in enumerate(data):
        if i in to_remove:
            continue

        new_data.append(row)

    col_names = new_data.pop(0)

    df = pd.DataFrame(new_data, columns=col_names)
    df = df.astype(datatypes) # cast to type
    with sqlite3.connect('data/data.db') as conn:
        df.to_sql('data', conn, if_exists='replace', index=False)
