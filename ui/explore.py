"""Explore page: filters -> SQL query (pandasql) -> results and charts."""
import streamlit as st
import data
import re

# every bot is 1, every human is 0; this turns that into a readable label in SQL
LABEL = "CASE WHEN bot = 1 THEN 'Bot' ELSE 'Human' END"

def init(_data):
    global app_data
    app_data = _data

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
        dur_min = int(df["session_duration_ms"].min())
        dur_max = int(df["session_duration_ms"].max())
        duration = st.slider("Session duration (ms)", dur_min, dur_max, (dur_min, dur_max))

    with col2:
        st.markdown("**Behaviour**")
        clicks_min = int(df["clicks"].min())
        clicks_max = int(df["clicks"].max())
        clicks = st.slider("Clicks", clicks_min, clicks_max, (clicks_min, clicks_max))
        idle = st.slider("Idle ratio", 0.0, 1.0, (0.0, 1.0))

    with col3:
        st.markdown("**Technical**")
        timezone = st.selectbox("Timezone mismatch", ["All", "No", "Yes"])
        webdriver = st.selectbox("Webdriver flag", ["All", "No", "Yes"])

    
    conditions = [
        f"session_duration_ms BETWEEN {duration[0]} AND {duration[1]}",
        f"clicks BETWEEN {clicks[0]} AND {clicks[1]}",
        f"idle_ratio BETWEEN {idle[0]} AND {idle[1]}"
    ]
    
    if session_type != "All":
        conditions.append(f"bot = {1 if session_type == 'Bot' else 0}")
    if timezone != "All":
        conditions.append(f"timezone_mismatch = {1 if timezone == 'Yes' else 0}")
    if webdriver != "All":
        conditions.append(f"webdriver_flag = {1 if webdriver == 'Yes' else 0}")
    where = " AND ".join(conditions)

    
    query = f"""
        SELECT COUNT(*) AS sessions, SUM(bot) AS bots,
        AVG(clicks) AS avg_clicks, AVG(session_duration_ms) AS avg_duration
        FROM data
        WHERE {where}
    """
    query = re.sub(r" +", " ", query)
    result = data.run_sql(query).iloc[0]

    st.divider()
    st.subheader("Results")
    if result["sessions"] == 0:
        st.warning("No sessions match these filters.")
        return

    r1, r2, r3, r4 = st.columns(4, border=True)
    r1.metric("Sessions matching", int(result["sessions"]))
    r2.metric("Bot share", f"{result['bots'] / result['sessions'] * 100:.2f}%")
    r3.metric("Average clicks", f"{result['avg_clicks']:.2f}")
    r4.metric("Average duration", f"{result['avg_duration']/1000:.2f} s")

    with st.expander("Show the SQL query"):
        st.code(query.replace(" +", " "), language="sql")
    
    def averages(columns):
        """Average of some columns, for bots and for humans (an SQL query)."""
        parts = ", ".join(f"ROUND(AVG({c}), 2) AS {c}" for c in columns)
        table = data.run_sql(f"SELECT {LABEL} AS label, {parts} FROM data WHERE {where} GROUP BY label")
        return table.set_index("label")

    st.divider()
    st.subheader("Detailed Analysis")
    tab1, tab2, tab3 = st.tabs(["Bots vs humans", "Click behaviour", "Mouse and scrolling"])

    with tab1:
        counts = data.run_sql(f"SELECT {LABEL} AS label, COUNT(*) AS sessions FROM data WHERE {where} GROUP BY label")
        st.dataframe(counts)
        st.bar_chart(counts.set_index("label"), horizontal=True)

    with tab2:
        clicking = averages(["median_click_interval_ms", "click_interval_std_ms", "button_hover_ms"])
        st.dataframe(clicking)
        st.bar_chart(clicking[["median_click_interval_ms"]], horizontal=True)

    with tab3:
        mouse = averages(["mouse_path_curvature", "idle_ratio", "scroll_entropy"])
        st.dataframe(mouse)
        st.bar_chart(mouse[["mouse_path_curvature"]], horizontal=True)