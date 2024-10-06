import pandas as pd
from .BaseUI import Base
import flet as ft
from ..Logic import TypeTaskLogic


class TypeTask(Base):
    def __init__(self, page):
        # Initialisation du DataFrame depuis la logique
        self.df = TypeTaskLogic.TypeTask().df
        self.filtered_df = self.df  # Créez une copie filtrée
        self.search_text_field = None  # Référence pour le TextField
        self.bottom_sheet = None  # BottomSheet sera initialisé plus tard
        self.text_error = None
        super().__init__(page, "Gestion des types de tâches")
        # Construction du contenu de la page
        self.page_content = self.build_page()

    def bottom_sheet_ui(self):
        # Création et retour d'un BottomSheet avec une fonction de fermeture
        self.bottom_sheet = ft.BottomSheet(
            bgcolor=ft.colors.RED,
            content=ft.Container(
                ft.Column(
                    controls=[
                        ft.Text(self.text_error, color=ft.colors.WHITE),
                    ],
                    tight=True,
                ),
                padding=10,
            )
        )
        return self.bottom_sheet

    def verif_add_data(self, e):
        # Accéder à la valeur actuelle du TextField
        search_value = self.search_text_field.value  # Récupérer la valeur du TextField
        if search_value == "" or search_value is None:
            print(f"est vide : {search_value}")
            self.text_error = "Le libellé est vide."
            self.page.dialog = self.bottom_sheet_ui()
            self.page.dialog.open = True
            self.page.update()
        elif self.filtered_df.shape[0] != 0:
            self.text_error = "Type de tâche existant avec ce libellé."
            print(f"égale à Zéro")

            self.page.dialog = self.bottom_sheet_ui()
            self.page.dialog.open = True
            self.page.update()
        else:
            print(f"Valeur du champ de texte : {search_value}")

    def on_search(self, e):
        # Filtrer le DataFrame en fonction du texte saisi dans le champ de texte
        search_text = e.control.value.lower()
        self.filtered_df = self.df[self.df["libelle"].str.contains(search_text, case=False, na=False)]
        # Mettre à jour la vue des ExpansionTiles
        self.page_content.controls[2] = self.make_view_expansion_tile_ui()
        self.page.update()

    def text_field_ui(self):
        # Champ de recherche avec bouton d'ajout qui déclenche `verif_add_data`
        self.search_text_field = ft.TextField(  # Stocker la référence dans un attribut
            expand=True,
            label="Libellé",
            autofill_hints=ft.AutofillHint.NAME,
            on_change=self.on_search  # Appel de la fonction de recherche
        )
        return ft.Row(
            controls=[
                self.search_text_field,  # Utiliser le champ de texte ici
                ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.verif_add_data)  # Bouton d'ajout
            ]
        )

    def make_view_expansion_tile_ui(self):
        # Utilisation du DataFrame filtré pour générer les `ExpansionTile`
        controls_list = self.filtered_df.apply(
            lambda row: self.expansion_tile_ui(row["libelle"], row["description"]), axis=1
        ).tolist()  # Transformation en liste

        # Retour d'une `ListView` contenant les `ExpansionTile`
        return ft.ListView(
            controls=controls_list  # Utilisation de la liste créée
        )

    @staticmethod
    def expansion_tile_ui(title: str, description: str):
        # Construction d'une `ExpansionTile` avec le titre et la description
        return ft.ExpansionTile(
            title=ft.Text(title),
            subtitle=ft.Text(description),
            affinity=ft.TileAffinity.LEADING,
            collapsed_text_color=ft.colors.BLACK,
            text_color=ft.colors.BLUE,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        )

    def build_page(self):
        # Construction de la page avec un champ de recherche et les `ExpansionTile`
        return ft.Column(
            expand=True,
            controls=[
                self.add_header(),
                self.text_field_ui(),  # Champ de recherche
                self.make_view_expansion_tile_ui()  # Affichage des `ExpansionTile`
            ]
        )