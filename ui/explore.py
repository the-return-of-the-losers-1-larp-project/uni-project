"""Explore page: filters -> SQL query (pandasql) -> results and charts."""
import pandas as pd
import streamlit as st
from pandasql import sqldf

# every bot is 1, every human is 0; this turns that into a readable label in SQL
LABEL = "CASE WHEN bot = 1 THEN 'Bot' ELSE 'Human' END"



def init(_data):
    global app_data
    app_data = _data


def run_sql(df, query):
    """Run an SQL query on the table called df."""
    try:
        return sqldf(query, {"df": df})
    except AttributeError:
        
        import sqlite3
        con = sqlite3.connect(":memory:")
        df.to_sql("df", con, index=False)
        result = pd.read_sql_query(query, con)
        con.close()
        return result


def main():
    df = app_data.df

    st.title("Session Explorer")
    st.caption("Explore which behaviour patterns are associated with automated sessions.")

    
    st.subheader("Filters")
    st.write("Select conditions to see the matching recorded sessions.")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Session**")
        session_type = st.selectbox("Session type", ["All", "Human", "Bot"])
        duration = st.slider("Session duration (ms)", int(df["session_duration_ms"].min()),
                             int(df["session_duration_ms"].max()),
                             (int(df["session_duration_ms"].min()), int(df["session_duration_ms"].max())))

    with col2:
        st.markdown("**Behaviour**")
        clicks = st.slider("Clicks", int(df["clicks"].min()), int(df["clicks"].max()),
                           (int(df["clicks"].min()), int(df["clicks"].max())))
        idle = st.slider("Idle ratio", 0.0, 1.0, (0.0, 1.0))

    with col3:
        st.markdown("**Technical**")
        timezone = st.selectbox("Timezone mismatch", ["All", "No", "Yes"])
        webdriver = st.selectbox("Webdriver flag", ["All", "No", "Yes"])

    
    conditions = [f"session_duration_ms BETWEEN {duration[0]} AND {duration[1]}",
                  f"clicks BETWEEN {clicks[0]} AND {clicks[1]}",
                  f"idle_ratio BETWEEN {idle[0]} AND {idle[1]}"]
    if session_type != "All":
        conditions.append(f"bot = {1 if session_type == 'Bot' else 0}")
    if timezone != "All":
        conditions.append(f"timezone_mismatch = {1 if timezone == 'Yes' else 0}")
    if webdriver != "All":
        conditions.append(f"webdriver_flag = {1 if webdriver == 'Yes' else 0}")
    where = " AND ".join(conditions)

    
    query = f"""SELECT COUNT(*) AS sessions, SUM(bot) AS bots,
       AVG(clicks) AS avg_clicks, AVG(session_duration_ms) AS avg_duration
FROM df
WHERE {where}"""
    result = run_sql(df, query).iloc[0]

    st.divider()
    st.subheader("Results")
    if result["sessions"] == 0:
        st.warning("No sessions match these filters.")
        return

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Sessions matching", int(result["sessions"]))
    r2.metric("Bot share", f"{result['bots'] / result['sessions'] * 100:.1f}%")
    r3.metric("Average clicks", f"{result['avg_clicks']:.1f}")
    r4.metric("Average duration", f"{result['avg_duration']:.0f} ms")
    with st.expander("Show the SQL query"):
        st.code(query, language="sql")

    
    def averages(columns):
        """Average of some columns, for bots and for humans (an SQL query)."""
        parts = ", ".join(f"ROUND(AVG({c}), 2) AS {c}" for c in columns)
        table = run_sql(df, f"SELECT {LABEL} AS label, {parts} FROM df WHERE {where} GROUP BY label")
        return table.set_index("label")

    st.divider()
    st.subheader("Detailed Analysis")
    tab1, tab2, tab3 = st.tabs(["Bots vs humans", "Click behaviour", "Mouse and scrolling"])

    with tab1:
        counts = run_sql(df, f"SELECT {LABEL} AS label, COUNT(*) AS sessions FROM df WHERE {where} GROUP BY label")
        st.bar_chart(counts.set_index("label"))

    with tab2:
        clicking = averages(["median_click_interval_ms", "click_interval_std_ms", "button_hover_ms"])
        st.dataframe(clicking)
        st.bar_chart(clicking[["median_click_interval_ms"]])

    with tab3:
        mouse = averages(["mouse_path_curvature", "idle_ratio", "scroll_entropy"])
        st.dataframe(mouse)
        st.bar_chart(mouse[["mouse_path_curvature"]])