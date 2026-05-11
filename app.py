import flet as ft
from classes import FTPServerApp
from classes import ControlsPage

async def main(page: ft.Page) :
    app = FTPServerApp()
    controls = ControlsPage()


    app.run(page)
    await controls.run(page)
    page.update()

if __name__ == "__main__":
    ft.app(main)
