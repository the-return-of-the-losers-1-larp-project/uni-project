import ui
import data
import model

df = data.load_data()
model, scaler, expected_columns = model.load_model()

ui.main(df)

