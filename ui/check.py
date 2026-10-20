import streamlit as st
import pandas as pd
import data

# stupid streamlit won't let us pass arguments into main()
# so we have to do this instead </3
def init(_data):
    global app_data
    app_data = _data

def main():
    st.title("check sessions, whatever that means")
    
