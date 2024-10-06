import flet as ft
from src.Route.InitRoute import InitRouter
from src.Utils.VerificationData import VerificationData


def main(page: ft.Page):
    page.title = "Gestion des tâches équipe HYPERVISION"
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.theme_mode = ft.ThemeMode.LIGHT

    # Vérification des data
    VerificationData().verification_folder_data()
    router = InitRouter(page)
    page.on_route_change = lambda e: router.navigate(e.route)

    page.go("/")

ft.app(target=main)
