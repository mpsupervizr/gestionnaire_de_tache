import pandas as pd
import os


class Task:
    def __init__(self):
        self.file_path = f"{os.getcwd()}/data/data.xlsx"
        self.sheet_name = "tasks"
        self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
