import flet as ft

from browser import browser_page

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Flet Browser Example"

    page.window.maximized = True
    page.window.maximizable = False
    
    page.add(
        ft.SafeArea(
            ft.Container(
                content=browser_page(page),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
        
    )


ft.app(target=main)
