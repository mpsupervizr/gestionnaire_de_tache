from .BaseUI import Base
import flet as ft
from ..Logic import TypeTaskLogic, TaskLogic


class Home(Base):
    def __init__(self, page):
        super().__init__(page, "Page d'accueil")
        self.df_type_task = TypeTaskLogic.TypeTask().df
        self.search_text_field = ft.TextField(expand=True)  # Initialisé directement pour éviter None
        self.filtered_df = TaskLogic.Task().df
        self.page_content = self.build_page()

    def verif_add_data(self, e):
        search_value = self.search_text_field.value.strip()  # Gérer les espaces inutiles
        if not search_value:
            print("Le champ de recherche est vide.")
        else:
            print(f"Recherche: {search_value}")
            # Logique supplémentaire à ajouter ici pour filtrer

    def list_view_view(self):
        controls_list = [
            self.expansion_tile_ui(
                row["id"], row["libelle"], row["description"], row["date_echeance"],
                row["date_derniere_modif"], row["status"], row["id_type_task"]
            )
            for _, row in self.filtered_df.iterrows()
        ]
        return ft.ListView(
            expand=True,
            controls=controls_list
        )

    def expansion_tile_ui(self, id_task: int, libelle: str, description: str, date_echeance, date_derniere_modif,
                          status, id_type_task):
        # Dynamique et personnalisable
        return ft.ExpansionTile(
            title=ft.Text(libelle),
            subtitle=ft.Text(description),
            collapsed_text_color=ft.colors.BLACK,
            text_color=ft.colors.BLUE,
            controls=[
                ft.ListTile(title=ft.Text(f"Échéance : {date_echeance}")),
                ft.ListTile(title=ft.Text(f"Modifié le : {date_derniere_modif}")),
                ft.ListTile(title=ft.Text(f"Statut : {status}")),
                ft.ListTile(title=ft.Text(f"Type de tâche : {id_type_task}")),
            ]
        )

    @staticmethod
    def segmented_button_view():
        return ft.SegmentedButton(
            selected_icon=ft.Icon(ft.icons.CHECK),
            selected={"IN PROGRESS"},
            allow_multiple_selection=True,
            segments=[
                ft.Segment(value="IN PROGRESS", label=ft.Text("En cours")),  # Utilise ft.Text
                ft.Segment(value="FINISHED", label=ft.Text("Terminées")),  # Utilise ft.Text
                ft.Segment(value="CANCELLED", label=ft.Text("Annulées")),  # Utilise ft.Text
                ft.Segment(value="DELETED", label=ft.Text("Supprimées")),  # Utilise ft.Text
            ],
        )

    def text_field_view(self):
        return ft.Row(
            controls=[
                self.search_text_field,
                ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.verif_add_data)
            ]
        )

    def tab_ui(self, libelle: str):
        return ft.Tab(
            text=libelle,
            content=ft.Container(
                padding=12,
                content=ft.Column(
                    controls=[
                        self.text_field_view(),
                        self.segmented_button_view(),
                        self.list_view_view()
                    ]
                )
            ),
        )

    def tabs_view(self):
        controls_list = [
            self.tab_ui(row["libelle"]) for _, row in self.df_type_task.iterrows()
        ]
        return ft.Tabs(
            expand=True,
            selected_index=1,
            animation_duration=300,
            tabs=controls_list
        )

    def build_page(self):
        return ft.Column(
            expand=True,
            controls=[
                self.add_header(),
                self.tabs_view()
            ]
        )