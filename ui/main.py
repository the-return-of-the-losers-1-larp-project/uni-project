import streamlit as st
import pandas as pd
import data

def main():
    df = data.get_data()

    st.title("Bot vs Human Session Detector")

    st.write("Number of sessions:", len(df))
    st.write("head of our data:")
    st.dataframe(df.head())
