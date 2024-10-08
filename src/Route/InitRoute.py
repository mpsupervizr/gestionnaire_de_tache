import flet as ft
from ..UI.HomeUI import Home
from ..UI.TypeTaskUI import TypeTask


class InitRouter:
    def __init__(self, page):
        self.page = page
        self.nav_rail = self.create_nav_rail()

    def create_nav_rail(self):
        return ft.NavigationRail(
            selected_index=0,
            bgcolor=ft.colors.RED_900,
            on_change=self.on_nav_change,
            min_width=100,
            min_extended_width=400,
            destinations=[
                ft.NavigationRailDestination(icon=ft.icons.HOME, label_content=ft.Text("Accueil",
                                                                                       color=ft.colors.WHITE, )),
                ft.NavigationRailDestination(icon=ft.icons.MERGE_TYPE,
                                             label_content=ft.Text("Gestion des type de tâche",
                                                                   color=ft.colors.WHITE, ))
            ]
        )

    def on_nav_change(self, e):
        selected_route = "/" if e.control.selected_index == 0 else "/type_task"
        self.page.go(selected_route)

    def navigate(self, route):
        if route == "/":
            self.page.views.clear()
            self.page.views.append(
                ft.View(
                    controls=[
                        ft.Row([
                            self.nav_rail,
                            Home(self.page).page_content
                        ],
                            expand=True
                        )
                    ]
                )
            )
        elif route == "/type_task":
            self.page.views.clear()
            self.page.views.append(
                ft.View(
                    controls=[
                        ft.Row([
                            self.nav_rail,
                            TypeTask(self.page).page_content
                        ],
                            expand=True
                        )
                    ]
                )
            )
        self.page.update()
