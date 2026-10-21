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
    bots_df = df[df["bot"] == 1]

    st.title("Bot vs Human Session Detector")
    st.text("The app helps the web shop's anti-abuse team see which interaction patterns " \
    "are associated with automated sessions, and check whether a live session looks like " \
    "a bot or a human without relying on country or IP address. The design below follows " \
    "the approved requirements: explore and filter the recorded sessions, query them " \
    "without, chart the differences between bots and humans, and return a verdict from " \
    "a trained classifier together with the three most similar historical sessions.")

    # this is for centering the items inside each column
    # i hate streamlit for not having a way to do this natively
    st.markdown(
        """<style>
        [data-testid="stColumn"] {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        [data-testid="stMetric"] {
            text-align: center;
            align-items: center;
        }
        [data-testid="stMetricValue"] {
            justify-content: center;
        }
        </style>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, border=True)

    col1.metric("Sessions", len(df))
    col2.metric("Bot sessions", len(bots_df))
    col3.metric("Bot share", f"{len(bots_df) / len(df) * 100 :.2f}%")

    st.header("Here's the head of our dataset")
    st.text("for cool demonstrative purposes")
    st.dataframe(df.head())

    if st.button("Explore the dataset", icon=":material/dataset:", type="primary", width="stretch"):
        st.switch_page(app_data.pages[1])
        
    if st.button("Try your own values", icon=":material/tune:", width="stretch"):
        st.switch_page(app_data.pages[2])
