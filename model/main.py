from joblib import load
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import config


def load_model():
    # generate model files if they don't exist
    if (
        not os.path.exists(config.MODEL_PATH) or
        not os.path.exists(config.SCALER_PATH) or
        not os.path.exists(config.FEATURES_PATH)
    ):
        with open(config.MODEL_GEN_NOTEBOOK_PATH) as f:
            nb_in = nbformat.read(f, nbformat.NO_CONVERT)
        ExecutePreprocessor().preprocess(nb_in)

    model = load(config.MODEL_PATH)
    scaler = load(config.SCALER_PATH)
    expected_columns = load(config.FEATURES_PATH)

    return model, scaler, expected_columns