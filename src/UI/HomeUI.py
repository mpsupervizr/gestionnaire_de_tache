from .BaseUI import Base
import flet as ft


class Home(Base):
    def __init__(self, page):
        super().__init__(page, "Page d'accueil")
        self.page_content = self.build_page()

    def build_page(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.add_header(),
                    ft.Text("Bienvenue à la page d'accueil !")
                ]
            )
        )