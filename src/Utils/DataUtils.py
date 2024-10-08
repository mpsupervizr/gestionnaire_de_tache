import os
import pandas as pd


class Data:
    def __init__(self):
        self.racine_directory = os.getcwd()
        self.file_path = f"{os.getcwd()}/data/data.xlsx"
        self.sheet_name_type_task = "type_task"
        self.sheet_name_task = "tasks"
        self.df_type_task = pd.read_excel(self.file_path, sheet_name=self.sheet_name_type_task)
        self.df_task = pd.read_excel(self.file_path, sheet_name=self.sheet_name_task)

    def save_data(self, df_type_task, df_task):
        df_type_task = self.df_type_task if df_type_task is None else df_type_task
        df_task = self.df_task if df_task is None else df_task
        with pd.ExcelWriter(f"{self.racine_directory}/data/data.xlsx") as writer:
            df_type_task.to_excel(writer, sheet_name=self.sheet_name_type_task, index=False)
            df_task.to_excel(writer, sheet_name=self.sheet_name_task, index=False)

