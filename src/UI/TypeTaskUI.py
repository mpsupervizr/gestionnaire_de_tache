import pandas as pd
from .BaseUI import Base
import flet as ft
from ..Logic import TypeTaskLogic


class TypeTask(Base):
    def __init__(self, page):
        # Initialisation du DataFrame depuis la logique
        # self.type_task = TypeTaskLogic.TypeTask()
        # self.df = TypeTaskLogic.TypeTask().df
        self.text_field_update_libelle = None
        self.text_field_update_description = None
        self.filtered_df = TypeTaskLogic.TypeTask().df  # Créez une copie filtrée
        self.search_text_field = None  # Référence pour le TextField
        self.bottom_sheet = None  # BottomSheet sera initialisé plus tard
        self.text_error = None
        super().__init__(page, "Gestion des types de tâches")
        # Construction du contenu de la page
        self.page_content = self.build_page()

    def update_type_task(self, e):
        _id = e.control.data['id']
        _libelle = e.control.data['libelle'].value
        _description = e.control.data['description'].value
        TypeTaskLogic.TypeTask().update_data(_id, _libelle, _description)
        self.actualise_search_view("")

    def delete_type_task(self, e):
        TypeTaskLogic.TypeTask().delete_data(e.control.data)
        self.actualise_search_view("")

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
        search_value = self.search_text_field.value.strip()  # Récupérer la valeur du TextField
        if search_value == "" or search_value is None:
            self.text_error = "Le libellé est vide."
            self.page.dialog = self.bottom_sheet_ui()
            self.page.dialog.open = True
            self.page.update()
        elif self.filtered_df.shape[0] != 0:
            self.text_error = "Type de tâche existant avec ce libellé."
            self.page.dialog = self.bottom_sheet_ui()
            self.page.dialog.open = True
            self.page.update()
        else:
            TypeTaskLogic.TypeTask().add_data(libelle=search_value, description=None)
            self.actualise_search_view(search_value)

    def on_search(self, e):
        # Filtrer le DataFrame en fonction du texte saisi dans le champ de texte
        search_text = e.control.value.lower()
        self.actualise_search_view(search_text)

    def actualise_search_view(self, text: str | None):
        self.filtered_df = TypeTaskLogic.TypeTask().df[
            TypeTaskLogic.TypeTask().df["libelle"].str.contains(text, case=False, na=False)
        ]
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
            lambda row: self.expansion_tile_ui(row["id"], row["libelle"], row["description"]), axis=1
        ).tolist()  # Transformation en liste

        # Retour d'une `ListView` contenant les `ExpansionTile`
        return ft.ListView(
            expand=True,
            controls=controls_list  # Utilisation de la liste créée
        )

    def text_field_update_libelle_ui(self, libelle: str):
        self.text_field_update_libelle = ft.TextField(
            label="Libellé",
            autofill_hints=ft.AutofillHint.NAME,
            value=libelle,
            # on_change=self.get_libelle
        )
        return self.text_field_update_libelle

    def text_field_update_description_ui(self, description: str):
        self.text_field_update_description = ft.TextField(
            label="Description",
            autofill_hints=ft.AutofillHint.NAME,
            value=description,
            # on_change=self.get_libelle
        )
        return self.text_field_update_description

    def expansion_tile_ui(self, id_type_task: int, libelle: str, description: str):
        # Construction d'une `ExpansionTile` avec le titre et la description
        return ft.ExpansionTile(
            title=ft.Text(libelle),
            subtitle=ft.Text(description),
            affinity=ft.TileAffinity.LEADING,
            collapsed_text_color=ft.colors.BLACK,
            text_color=ft.colors.BLUE,
            controls=[
                ft.Container(
                    expand=True,
                    padding=12,
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                expand=8,
                                content=ft.Column(
                                    controls=[
                                        self.text_field_update_libelle_ui(libelle),
                                        self.text_field_update_description_ui(description)
                                    ]
                                )
                            ),
                            ft.Container(
                                expand=2,
                                content=ft.Column(
                                    controls=[
                                        ft.TextButton(
                                            "Modifier", icon=ft.icons.MODE,
                                            data={"id": id_type_task, "libelle": self.text_field_update_libelle,
                                                  "description": self.text_field_update_description},
                                            on_click=self.update_type_task
                                        ),
                                        ft.TextButton(
                                            "Supprimer", icon=ft.icons.DELETE_FOREVER, icon_color=ft.colors.RED,
                                            style=ft.ButtonStyle(
                                                color=ft.colors.RED
                                            ),
                                            data=id_type_task,
                                            on_click=self.delete_type_task,
                                        )
                                    ]
                                ),
                            )
                        ]
                    )
                )
            ]
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
