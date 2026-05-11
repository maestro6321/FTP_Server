import asyncio
import flet as ft
from .functions import Functions

class ControlsPage:
    def __init__(self):
        # Instance variables
        self.console_log = ft.TextField(
            value="Waiting for logs...",
            read_only=True,
            multiline=True,
            expand=True,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK,
            border=ft.InputBorder.NONE,
            text_align=ft.TextAlign.LEFT
        )
        self.functions = Functions(self)  # Pass reference to this class

    async def _flush_log_queue(self):
        while True:
            flushed = False
            while not self.functions.log_queue.empty():
                msg = self.functions.log_queue.get()
                if self.console_log.value == "Waiting for logs...":
                    self.console_log.value = msg
                else:
                    self.console_log.value += f"\n{msg}"
                flushed = True
            if flushed:
                self.page.update()
            await asyncio.sleep(0.1)

    async def pick_directory(self, e):
        path = await ft.FilePicker().get_directory_path()
        if path:
            self.url.value = path
            self.page.update()

    def clear_console(self, e):
        self.console_log.value = ""
        self.page.update()

    async def run(self, page: ft.Page):
        self.page = page

        self.url = ft.TextField(label="Enter Path", hint_text=r"C:\Your_Folder\Your_Folder", expand=True)
        input_row = ft.Row(
            controls=[
                self.url,
                ft.ElevatedButton(
                    content="Open directory",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=self.pick_directory),
            ]
        )
        self.host = ft.TextField(label="Enter URL", hint_text="127.0.0.1", value="0.0.0.0")
        self.port = ft.TextField(label="Enter PORT", hint_text="1234", value="2121")
        row_1 = ft.Row(
            controls=[
                self.host,
                self.port,
                ft.ElevatedButton(
                    content="Start",
                    icon=ft.Icons.START,
                    on_click=lambda e: self.functions.start_server(self.url.value, self.host.value, self.port.value, self.user.value, self.password.value, page)
                ),
            ]
        )
        self.user = ft.TextField(label="Enter User Name", hint_text="UserName", value="admin")
        self.password = ft.TextField(label="Enter Password", hint_text="Password", value="12345", password=True, can_reveal_password=True)
        row_2 = ft.Row(
            controls=[
                self.user,
                self.password,
                ft.ElevatedButton(
                    content="Stop",
                    icon=ft.Icons.STOP,
                    on_click=lambda e: self.functions.stop_server(page)
                )
            ]
        )

        console = ft.Container(
            content=ft.Column([
                ft.Row(
                    controls=[
                        ft.Text("📺 CONSOLE LOGS", size=14, weight=ft.FontWeight.W_700, color=ft.Colors.GREEN_400),
                        ft.ElevatedButton(
                            content="Clear Logs",
                            icon=ft.Icons.CLEAR_ALL,
                            on_click=self.clear_console
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(),
                self.console_log,
            ], spacing=5, expand=True),
            bgcolor=ft.Colors.BLACK,
            expand=True,
            border_radius=5,
            padding=10,
        )


        panel = ft.Column(
            spacing=12,
            controls=[
                input_row,
                row_1,
                row_2,
                console,
            ],
            expand=True
        )
        page.add(panel)
        asyncio.create_task(self._flush_log_queue())