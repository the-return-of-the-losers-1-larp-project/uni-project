from joblib import load

def load_model():
    model = load("model/bvh_knn_model48.joblib")
    scaler = load("model/bvh_scaler48.joblib")
    expected_columns = load("model/bvh_features48.joblib")

    return model, scaler, expected_columns