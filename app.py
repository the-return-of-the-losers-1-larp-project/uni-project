import streamlit as st
import pandas as pd
from pandasql import sqldf

st.title("Bot vs Human Session Detector")

df = pd.read_csv("data/data.csv")
st.write("Number of sessions:", len(df))
st.dataframe(df.head())
