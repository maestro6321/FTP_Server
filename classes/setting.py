import flet as ft

class FTPServerApp:
    def __init__(self):
        # Window settings
        self.title = "FTP SERVER"
        self.window_width = 800
        self.window_height = 500
        self.resizable = False

        # Layout settings
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.START

    def setup_page(self, page: ft.Page):
        page.title = self.title
        page.horizontal_alignment = self.horizontal_alignment
        page.vertical_alignment = self.vertical_alignment
        page.window.width = self.window_width
        page.window.height = self.window_height
        page.window.resizable = self.resizable

    def run(self, page: ft.Page):
        """Main application logic"""
        self.setup_page(page)