from .BaseUI import Base
import flet as ft
import datetime

from ..Logic import TypeTaskLogic, TaskLogic


class Home(Base):
    def __init__(self, page):
        super().__init__(page, "Page d'accueil")
        self.df_type_task = TypeTaskLogic.TypeTask().df  # Contient les types de tâches
        self.filtered_df = TaskLogic.Task().df  # Contient toutes les tâches
        self.search_text_field = ft.TextField(expand=True)
        self.text_error = None
        self.bottom_sheet = None
        self.tab_ids = []  # Liste pour stocker les id_type_task
        self.selected_id_type_task = None  # Variable pour stocker l'ID de l'onglet sélectionné
        self.selected_statuses = {"IN PROGRESS"}  # Statuts sélectionnés par défaut
        self.selected_index_tabs = 0
        self.text_field_update_libelle = None
        self.text_field_update_description = None
        self.dropdown_update_status = None
        self.dropdown_update_type_task = None
        self.selected_date_echeance = ft.Text("")
        self.page_content = self.build_page()

        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2026, 12, 31),
            on_change=self.change_date,
        )

        # Initialiser l'id_type_task du premier onglet
        if self.tab_ids:
            self.selected_id_type_task = self.tab_ids[0]  # Sélectionner l'id_type_task du premier onglet

    def change_date(self, e):
        self.selected_date_echeance.value = self.date_picker.value
        print(self.selected_date_echeance.value)
        self.page.update()

    def open_date_picker(self, e):
        self.page.open(self.date_picker)

    def on_search(self, e):
        search_text = e.control.value.lower()
        self.actualise_search_view(search_text)

    def actualise_search_view(self, search_text: str | None):
        self.filtered_df = TaskLogic.Task().df[
            (TaskLogic.Task().df["libelle"].str.contains(search_text, case=False, na=False)) &
            (TaskLogic.Task().df["id_type_task"] == self.selected_id_type_task) &
            (TaskLogic.Task().df["statut"].isin(self.selected_statuses))
        ]
        self.page_content.controls[3] = self.tabs_view()
        self.page.update()

    def bottom_sheet_ui(self):
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
        search_value = self.search_text_field.value.strip()

        if self.selected_id_type_task is None:
            print("Aucun onglet sélectionné.")
            self.text_error = "Veuillez sélectionner un type de tâche."
            self.page.dialog = self.bottom_sheet_ui()
            self.page.dialog.open = True
            self.page.update()
            return

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
            print(f"Libellé : {search_value}, ID Type Task : {self.selected_id_type_task}")
            TaskLogic.Task().add_data(libelle=search_value, id_type_task=self.selected_id_type_task)
            self.actualise_search_view(search_value)

    def list_view_view(self, id_type_task):
        # Filtrer les tâches en fonction de l'id_type_task et des statuts sélectionnés
        filtered_tasks = self.filtered_df[
            (self.filtered_df['id_type_task'] == id_type_task) &
            (self.filtered_df['statut'].isin(self.selected_statuses))
        ]

        controls_list = [
            self.expansion_tile_ui(
                row["id"], row["libelle"], row["description"], row["date_echeance"],
                row["date_derniere_modif"], row["statut"], row["id_type_task"]
            )
            for _, row in filtered_tasks.iterrows()
        ]
        return ft.ListView(
            expand=True,
            controls=controls_list
        )

    def text_field_update_libelle_ui(self, libelle: str):
        self.text_field_update_libelle = ft.TextField(
            expand=True,
            label="Libellé",
            autofill_hints=ft.AutofillHint.NAME,
            value=libelle,
            # on_change=self.get_libelle
        )
        return self.text_field_update_libelle

    def text_field_update_description_ui(self, description: str):
        self.text_field_update_description = ft.TextField(
            label="Description",
            max_lines=10,
            autofill_hints=ft.AutofillHint.NAME,
            multiline=True,
            value=description,
            # on_change=self.get_libelle
        )
        return self.text_field_update_description

    def dropdown_update_status_ui(self, status):
        self.dropdown_update_status = ft.Dropdown(
            expand=True,
            label="Statut",
            hint_text="Choisissez le statut",
            value=status,
            options=[
                ft.dropdown.Option(key="IN PROGRESS", text="En cours"),
                ft.dropdown.Option(key="FINISHED", text="Terminée"),
                ft.dropdown.Option(key="CANCELLED", text="Annulée"),
            ]
        )
        return self.dropdown_update_status

    def dropdown_update_type_task_ui(self, id_type_task):
        self.dropdown_update_type_task = ft.Dropdown(
            expand=True,
            label="Type de tâche",
            hint_text="Choisissez le type de tâche",
            value=id_type_task,
            options=[ft.dropdown.Option(key=row["id"], text=row["libelle"]) for _, row in self.df_type_task.iterrows()]
        )
        return self.dropdown_update_type_task

    def delete_task(self, e):
        TaskLogic.Task().delete_task(e.control.data)
        self.actualise_search_view("")

    def update_task(self, e):
        TaskLogic.Task().update_task(
            e.control.data["id"], e.control.data["libelle"].value, e.control.data["description"].value,
            e.control.data["date_echeance"].value, e.control.data["status"].value, e.control.data["id_type_task"].value
        )
        self.actualise_search_view("")

    def expansion_tile_ui(self, id_task: int, libelle: str, description: str, date_echeance, date_derniere_modif,
                          status, id_type_task):
        return ft.ExpansionTile(
            title=ft.Text(libelle),
            subtitle=ft.Text(f"Date échéance: {date_echeance}, Date de dernière modification: {date_derniere_modif}", color=TaskLogic.Task().get_color_by_date(date_echeance, status)),
            collapsed_text_color=ft.colors.BLACK,
            text_color=ft.colors.BLUE,
            controls=[
                ft.Container(
                    expand=True,
                    padding=12,
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                expand=8,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            self.text_field_update_libelle_ui(libelle),
                                            self.dropdown_update_status_ui(status),
                                            self.dropdown_update_type_task_ui(id_type_task)
                                        ]
                                    ),
                                    self.text_field_update_description_ui(description)
                                ]
                            ),
                            ft.Column(
                                expand=2,
                                controls=[
                                    ft.TextButton(
                                        "Date d'échéance",
                                        icon=ft.icons.CALENDAR_MONTH,
                                        on_click=self.open_date_picker
                                    ),
                                    ft.TextButton(
                                        "Modifier",
                                        icon=ft.icons.MODE,
                                        data={
                                            "id": id_task,
                                            "libelle": self.text_field_update_libelle,
                                            "description": self.text_field_update_description,
                                            "date_echeance": self.selected_date_echeance,
                                            "status": self.dropdown_update_status,
                                            "id_type_task": self.dropdown_update_type_task
                                        },
                                        on_click=self.update_task
                                    ),
                                    ft.TextButton(
                                        "Supprimer",  icon=ft.icons.DELETE, icon_color=ft.colors.RED,
                                        style=ft.ButtonStyle(
                                            color=ft.colors.RED
                                        ),
                                        data=id_task,
                                        on_click=self.delete_task
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def tab_ui(self, id_type_task: int, libelle: str):
        return ft.Tab(
            text=libelle,
            content=ft.Container(
                padding=12,
                content=ft.Column(
                    controls=[self.list_view_view(id_type_task)]
                )
            )
        )

    def tabs_view(self):
        self.tab_ids = [row["id"] for _, row in self.df_type_task.iterrows()]

        controls_list = [
            self.tab_ui(row["id"], row["libelle"]) for _, row in self.df_type_task.iterrows()
        ]

        return ft.Tabs(
            expand=True,
            selected_index=self.selected_index_tabs,  # Sélectionne l'onglet par défaut (le premier)
            animation_duration=300,
            tabs=controls_list,
            on_change=self.handle_tab_change  # Gérer le changement d'onglet
        )

    def handle_tab_change(self, e):
        selected_index = e.control.selected_index
        self.selected_index_tabs = selected_index
        self.selected_id_type_task = self.tab_ids[self.selected_index_tabs]
        print(f"Onglet sélectionné : {selected_index}, ID Type Task : {self.selected_id_type_task}")
        self.actualise_search_view(self.search_text_field.value)
        # self.page.update()

    def segmented_button_view(self):
        return ft.SegmentedButton(
            selected_icon=ft.Icon(ft.icons.CHECK),
            selected=self.selected_statuses,  # Statuts sélectionnés par défaut
            allow_multiple_selection=True,
            segments=[
                ft.Segment(value="IN PROGRESS", label=ft.Text("En cours")),
                ft.Segment(value="FINISHED", label=ft.Text("Terminées")),
                ft.Segment(value="CANCELLED", label=ft.Text("Annulées")),
                ft.Segment(value="DELETED", label=ft.Text("Supprimées")),
            ],
            on_change=self.handle_segmented_button_change  # Gérer le changement de statut
        )

    def handle_segmented_button_change(self, e):
        # Met à jour les statuts sélectionnés
        self.selected_statuses = e.control.selected
        print(f"Statuts sélectionnés : {self.selected_statuses}")
        self.actualise_search_view(self.search_text_field.value)
        # self.page.update()  # Actualise la page pour refléter les changements dans les statuts sélectionnés

    def text_field_view(self):
        self.search_text_field = ft.TextField(  # Stocker la référence dans un attribut
            expand=True,
            label="Libellé",
            autofill_hints=ft.AutofillHint.NAME,
            on_change=self.on_search  # Appel de la fonction de recherche
        )

        return ft.Row(
            controls=[
                self.search_text_field,
                ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.verif_add_data)
            ]
        )

    def build_page(self):
        return ft.Column(
            expand=True,
            controls=[
                self.add_header(),
                self.text_field_view(),
                self.segmented_button_view(),
                self.tabs_view()
            ]
        )