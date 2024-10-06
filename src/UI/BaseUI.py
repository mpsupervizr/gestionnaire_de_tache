import flet as ft


class Base:
    def __init__(self, page, title):
        self.page = page
        self.title = title

    def add_header(self):
        return ft.Text(self.title, size=30)

    def add_navigation_button(self, label, target_route):
        return ft.ElevatedButton(label, on_click=lambda _: self.page.go(target_route))
