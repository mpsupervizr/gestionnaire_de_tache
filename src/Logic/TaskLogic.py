import pandas as pd
import os
from ..Utils import DataUtils
import locale
from datetime import datetime
import flet as ft
import math
from typing import Union


class Task:
    def __init__(self):
        self.file_path = f"{os.getcwd()}/data/data.xlsx"
        self.sheet_name = "tasks"
        self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        locale.setlocale(locale.LC_TIME, 'fr_FR')  # Pour Windows, cette ligne fonctionne souvent

    def add_data(self, libelle: str, id_type_task: int):
        new_data = pd.DataFrame(
            [
                [self.df.shape[0] + 1, libelle, None, None, datetime.now().strftime("%A, %d %B %Y"), "IN PROGRESS",
                 id_type_task]
            ],
            columns=["id", "libelle", "description", "date_echeance", "date_derniere_modif", "statut", "id_type_task"]
        )
        self.df = pd.concat([self.df, new_data], ignore_index=True)
        DataUtils.Data().save_data(df_type_task=None, df_task=self.df)

    def delete_task(self, id_task):
        row_index = self.df.index[self.df['id'] == id_task].tolist()[0]
        self.df.at[row_index, 'statut'] = "DELETED"
        DataUtils.Data().save_data(df_type_task=None, df_task=self.df)

    def update_task(self, id_task, libelle, description, date_echeance, status, id_type_task):

        date = (
            datetime.strptime(str(date_echeance), "%Y-%m-%d %H:%M:%S").strftime("%A, %d %B %Y").capitalize()
            if date_echeance is not None and date_echeance != ''
            else None
        )
        row_index = self.df.index[self.df['id'] == id_task].tolist()[0]
        self.df.at[row_index, 'libelle'] = libelle
        self.df.at[row_index, 'description'] = description
        self.df.at[row_index, 'date_echeance'] = date
        self.df.at[row_index, 'date_derniere_modif'] = datetime.now().strftime("%A, %d %B %Y")
        self.df.at[row_index, 'statut'] = status
        self.df.at[row_index, 'id_type_task'] = id_type_task
        DataUtils.Data().save_data(df_type_task=None, df_task=self.df)

    @staticmethod
    def get_color_by_date(date: Union[float, str], status):
        if isinstance(date, float) and not math.isnan(date):
            return ft.colors.RED
        elif isinstance(date, str) and status == "IN PROGRESS":
            _date = datetime.strptime(date, "%A, %d %B %Y")
            current_date = datetime.now()
            if _date.date() == current_date.date():
                return ft.colors.ORANGE
            elif _date.date() > current_date.date():
                return ft.colors.GREEN
            else:
                return ft.colors.RED
        else:
            return None
        #     return None
        # date = datetime.strptime(date, "%A, %d %B %Y")
        # current_date = datetime.now()
        #
        # if status == "IN PROGRESS":
        #     color = None
        #     if date.date() == current_date.date():
        #         color = ft.colors.YELLOW
        #     elif date.date() > current_date.date():
        #         color = ft.colors.GREEN
        #     else:
        #         return ft.colors.RED
        #
        #     return color
