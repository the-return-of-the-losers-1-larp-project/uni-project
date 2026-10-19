import csv
import pandas as pd
import sqlite3

data = []
with open("data/data.csv") as f:
    for row in csv.reader(f):
        data.append(row)

# rows to remove
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
# the csv module reads every value as text, and bool("0") is True in Python,
# so the true/false columns must go through int first
bool_cols = [c for c, t in datatypes.items() if t == 'bool']
for c in bool_cols:
    df[c] = df[c].astype('int64')
df = df.astype(datatypes) # cast to type
with sqlite3.connect('data/data.db') as conn:
    df.to_sql('data', conn, if_exists='replace', index=False)

# csv for the Streamlit app and the model: 0/1 instead of True/False, without referrer_type
out = df.drop(columns=['referrer_type']).copy()
for c in bool_cols:
    out[c] = out[c].astype('int64')
out.to_csv('data/cleaned_data.csv', index=False)