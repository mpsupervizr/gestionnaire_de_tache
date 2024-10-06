import os
import pandas as pd
from openpyxl import load_workbook

class VerificationData:
    def __init__(self):
        self.racine_directory = os.getcwd()

    def verification_folder_data(self) -> bool:
        try:
            if not os.path.exists(f"{self.racine_directory}/data"):
                self.create_folder_data()
                self.create_file_data()
                print("Le dossier data à été créé avec succès.")
            else:
                print("Le dossier data existe déjà.")
        except Exception as e:
            print("Une erreur s'est produite lors de la création du dossier :", e)
        return True

    def create_folder_data(self) -> bool:
        os.makedirs(f"{self.racine_directory}/data")
        return True

    def create_file_data(self):
        df = pd.DataFrame(columns=["id", "libelle", "description"])
        df.to_excel(f"{self.racine_directory}/data/data.xlsx", sheet_name="type_task", index=False)

    def verification_file_data(self):
        try:
            df = pd.read_excel(f"{self.racine_directory}/data", sheet_name="type_task")
        except FileNotFoundError:
            writer = pd.ExcelWriter(f"{self.racine_directory}/data", engine='openpyxl')
            writer.save()
            writer.close()
            df = pd.DataFrame(columns=["id", "libelle", "description"])
            df.to_excel(f"{self.racine_directory}/data", sheet_name="type_task", index=False)
