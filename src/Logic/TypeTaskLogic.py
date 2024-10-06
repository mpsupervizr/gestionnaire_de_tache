import pandas as pd
import os

class TypeTask:
    def __init__(self):
        self.df = pd.read_excel(f"{os.getcwd()}/data/data.xlsx", sheet_name="type_task")
