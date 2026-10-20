"""Check page: enter a session -> verdict, three most similar sessions, comparison."""
import pandas as pd
import streamlit as st
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


#
def init(_data):
    global app_data
    app_data = _data



class ScalerAndModel:
    """Only used if load_model() returns the scaler and the model separately."""
    def __init__(self, scaler, model):
        self.scaler, self.model = scaler, model
        self.feature_names_in_ = getattr(scaler, "feature_names_in_", None)

    def predict(self, X):
        return self.model.predict(self.scaler.transform(X))

    def predict_proba(self, X):
        return self.model.predict_proba(self.scaler.transform(X))


def find_model(model_files):
    if model_files is None or hasattr(model_files, "predict"):
        return model_files
    items = list(model_files.values()) if isinstance(model_files, dict) else list(model_files)
    model = next((i for i in items if hasattr(i, "predict")), None)
    scaler = next((i for i in items if hasattr(i, "transform") and not hasattr(i, "predict")), None)
    if model is not None and scaler is not None and not hasattr(model, "steps"):
        return ScalerAndModel(scaler, model)
    return model



def main():
    df = app_data.df
    model = find_model(app_data.model_files)

    st.title("Check a Session")
    st.caption("Enter the behaviour of a live session to get a human-or-bot verdict.")

    if model is None:
        st.error("No trained model found.")
        return

    
    columns = list(model.feature_names_in_)
    referrers = [c.replace("referrer_type_", "") for c in columns if c.startswith("referrer_type_")]
    features = [c for c in columns if not c.startswith("referrer_type_")]
    df = df.copy()
    df[features] = df[features].astype(float)

    
    st.subheader("Enter Session Behaviour")

    
    recorded_rows = df[features].copy()
    for r in referrers:
        recorded_rows["referrer_type_" + r] = (df["referrer_type"] == r).astype(int) if "referrer_type" in df else 0
    bot_probability = pd.Series(model.predict_proba(recorded_rows[columns])[:, 1], index=df.index)
    sure_bot = df.loc[bot_probability[df["bot"] == 1].idxmax()]
    sure_human = df.loc[bot_probability[df["bot"] == 0].idxmin()]

    start_from = st.selectbox("Start from", ["Median session", "A recorded bot", "A recorded human"])
    st.caption("The model is not right for every session, see the accuracy in the report.")
    if start_from == "Median session":
        start = df[features].median()
        start_referrer = referrers[0] if referrers else None
    else:
        recorded = sure_bot if start_from == "A recorded bot" else sure_human
        start = recorded[features]
        start_referrer = recorded.get("referrer_type")

    values = {}
    cols = st.columns(3)
    for i, name in enumerate(features):
        key = f"{name}_{start_from}"                          
        with cols[i % 3]:
            if df[name].nunique() <= 2:                      
                values[name] = st.selectbox(name, [0, 1], index=int(start[name]), key=key)
            else:                                             
                values[name] = st.number_input(name, value=float(start[name]), key=key)
    if referrers:                                             
        index = referrers.index(start_referrer) if start_referrer in referrers else 0
        referrer = st.selectbox("referrer_type", referrers, index=index, key=f"referrer_{start_from}")

    compare = st.selectbox("Metric to compare with the averages", features)

    
    if st.button("Classify session", type="primary"):
        session = pd.DataFrame([values])[features].astype(float)

        model_input = session.copy()
        for r in referrers:
            model_input["referrer_type_" + r] = int(referrer == r)
        model_input = model_input[columns]

        st.divider()
        st.subheader("Verdict")
        if model.predict(model_input)[0] == 1:
            st.error("Verdict: BOT")
        else:
            st.success("Verdict: HUMAN")
        if hasattr(model, "predict_proba"):
            st.write(f"Model confidence: {model.predict_proba(model_input)[0].max():.0%}")

       
        scaler = StandardScaler().fit(df[features])
        neighbours = NearestNeighbors(n_neighbors=3).fit(scaler.transform(df[features]))
        distance, index = neighbours.kneighbors(scaler.transform(session))
        similar = df.iloc[index[0]].copy()
        similar.insert(0, "label", similar["bot"].map({0: "Human", 1: "Bot"}))
        st.subheader("Three most similar recorded sessions")
        st.dataframe(similar)

        
        st.subheader("Session Comparison")
        comparison = pd.DataFrame(
            {compare: [session[compare].iloc[0],
                       df[df["bot"] == 0][compare].mean(),
                       df[df["bot"] == 1][compare].mean()]},
            index=["Your session", "Human average", "Bot average"])
        st.bar_chart(comparison)