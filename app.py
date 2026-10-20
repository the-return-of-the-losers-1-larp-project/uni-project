import ui
import data
import model

df = data.load_data()
model_files = model.load_model()

class AppData:
    def __init__(self):
        self.df = df
        self.model_files = model_files

ui.main(AppData())

