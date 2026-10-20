import streamlit_extras as stx
import streamlit as st
import pandas as pd
import data

# stupid streamlit won't let us pass arguments into main()
# so we have to do this instead </3
def init(_data):
    global app_data
    app_data = _data

def main():
    df: pd.DataFrame = app_data.df

    st.title("Explore the dataset")
    st.markdown("Here, you can examine the dataset more closely. Give it a go!")

    filtered_df: pd.DataFrame = stx.dataframe_explorer.dataframe_explorer(df, case=False)
    st.dataframe(filtered_df)

    bots_df_filtered = filtered_df[filtered_df["bot"] == 1]

    col1, col2, col3, col4 = st.columns(4, border=True)

    col1.metric("Sessions", len(filtered_df))
    col2.metric("Bot share", f"{len(bots_df_filtered) / len(filtered_df) * 100 :.2f}%")
    col3.metric("Average clicks", f"{filtered_df["clicks"].values.mean() :.2f}")
    col4.metric("Average session time", f"{filtered_df["session_duration_ms"].values.mean() / 1000 :.2f}s")

    st.header("Detailed analysis")
    st.write("comig soom")
    st.write("also, does this really have to be in sql???")
