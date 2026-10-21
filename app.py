
import streamlit as st

st.title("startup diagnostic")
st.write("app.py started")

import ui
st.write("ui imported")

import data
st.write("data imported")

import model
st.write("model imported")

st.write("loading data")
df = data.load_data()
st.write("data loaded", df.shape)

st.write("loading model")
model_files = model.load_model()
st.write("model loaded")

class AppData:
    def __init__(self):
        self.df = df
        self.model_files = model_files

st.write("calling ui.main")
ui.main(AppData())
