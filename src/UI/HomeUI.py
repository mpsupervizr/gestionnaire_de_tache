from .BaseUI import Base
import flet as ft
from ..Logic import TypeTaskLogic
from ..Logic import TaskLogic


class Home(Base):
    def __init__(self, page):
        self.df_type_task = TypeTaskLogic.TypeTask().df
        self.search_text_field = None
        self.filtered_df = TaskLogic.Task().df
        super().__init__(page, "Page d'accueil")
        self.page_content = self.build_page()

    def list_view_view(self):
        controls_list = [self.expansion_tile_ui(row["id"], row["libelle"], row["description"], row["date_echeance"],
                                                row["date_derniere_modif"], row["status"], row["id_type_task"])
                         for index, row in self.filtered_df.iterrows()]
        # controls_list = self.filtered_df.apply(
        #     lambda row: self.expansion_tile_ui(row["id"], row["libelle"], row["description"], row["date_echeance"],
        #                                        row["date_derniere_modif"], row["status"], row["id_type_task"]), axis=1
        # ).tolist()
        return ft.ListView(
            expand=True,
            controls=controls_list
        )

    def expansion_tile_ui(self, id_task: int, libelle: str, description: str, date_echeance, date_derniere_modif,
                          status, id_type_task):
        return ft.ExpansionTile(
            title=ft.Text(libelle),
            subtitle=ft.Text(description),
            affinity=ft.TileAffinity.LEADING,
            collapsed_text_color=ft.colors.BLACK,
            text_color=ft.colors.BLUE,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ]
        )

    @staticmethod
    def segmented_button_view():
        return ft.SegmentedButton(
            selected_icon=ft.Icon(ft.icons.CHECK),
            selected={"IN PROGRESS"},
            allow_multiple_selection=True,
            segments=[
                ft.Segment(
                    value="IN PROGRESS",
                    label=ft.Text("En cours"),
                    # icon=ft.Icon(ft.icons.LOOKS_ONE),
                ),
                ft.Segment(
                    value="FINISHED",
                    label=ft.Text("Terminées"),
                    # icon=ft.Icon(ft.icons.LOOKS_TWO),
                ),
                ft.Segment(
                    value="CANCELLED",
                    label=ft.Text("Annulées"),
                    # icon=ft.Icon(ft.icons.LOOKS_3),
                ),
                ft.Segment(
                    value="DELETED",
                    label=ft.Text("Supprimées"),
                    # icon=ft.Icon(ft.icons.LOOKS_4),
                ),
            ],
        )

    def text_field_view(self):
        self.search_text_field = ft.TextField(
            expand=True,
            label="Libellé",
            autofill_hints=ft.AutofillHint.NAME
        )
        return ft.Row(
            controls=[
                self.search_text_field,
                ft.FloatingActionButton(icon=ft.icons.ADD)
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
        controls_list = [self.tab_ui(row["libelle"]) for index, row in self.df_type_task.iterrows()]
        # controls_list = self.df_type_task.apply(
        #     lambda row: self.tab_ui(row["libelle"]), axis=1
        # ).tolist()

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
