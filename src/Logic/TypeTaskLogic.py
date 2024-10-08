import pandas as pd
import os
from ..Utils import DataUtils


class TypeTask:
    def __init__(self):
        self.file_path = f"{os.getcwd()}/data/data.xlsx"
        self.sheet_name = "type_task"
        self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

    def add_data(self, libelle: str | None, description: str | None):
        new_data = pd.DataFrame([[self.df.shape[0] + 1, libelle, description]],
                                columns=["id", "libelle", "description"])
        self.df = pd.concat([self.df, new_data], ignore_index=True)
        DataUtils.Data().save_data(df_type_task=self.df, df_task=None)

    # def save_data(self):
    #     with pd.ExcelWriter(self.file_path, mode="w", engine="openpyxl") as writer:
    #         self.df.to_excel(writer, sheet_name=self.sheet_name, index=False)

    def delete_data(self, id_type_task: int):
        self.df = self.df[self.df["id"] != id_type_task]
        DataUtils.Data().save_data(df_type_task=self.df, df_task=None)

    def update_data(self, id_type_task, libelle, description):
        row_index = self.df.index[self.df['id'] == id_type_task].tolist()[0]
        self.df.at[row_index, 'libelle'] = libelle
        self.df.at[row_index, 'description'] = str(description)
        DataUtils.Data().save_data(df_type_task=self.df, df_task=None)
