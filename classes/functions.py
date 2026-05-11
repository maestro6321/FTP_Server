import flet as ft
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
import logging
import queue


class LogHandler(logging.Handler):
    def __init__(self, update_func):
        super().__init__()
        self.update_func = update_func

    def emit(self, record):
        msg = self.format(record)
        self.update_func(msg)


class Functions:
    def __init__(self, controls_page):
        # Store reference to ControlsPage to access its variables
        self.controls_page = controls_page
        self.server = None
        self.thread = None
        self.log_queue = queue.Queue()

    def update_console(self, new_message):
        self.log_queue.put(f"• {new_message}")

    def start_server(self, directory, host, port, username, password, page):
        self.page = page
        try:
            # Set up logging
            logger = logging.getLogger('pyftpdlib')
            logger.setLevel(logging.INFO)
            handler = LogHandler(self.update_console)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            logger.addHandler(handler)

            authorizer = DummyAuthorizer()
            authorizer.add_user(username, password, directory, perm="elradfmw")
            handler = FTPHandler
            handler.authorizer = authorizer
            self.server = FTPServer((host, int(port)), handler)
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            self.update_console(f"FTP Server started on {host}:{port}")
            page.update()
        except Exception as e:
            self.update_console(f"Error starting server: {str(e)}")
            page.update()

    def stop_server(self, page):
        try:
            if self.server:
                self.server.close_all()
                self.thread.join()
                self.server = None
                self.thread = None
                self.update_console("FTP Server stopped")
                page.update()
            else:
                self.update_console("Server not running")
                page.update()
        except Exception as e:
            self.update_console(f"Error stopping server: {str(e)}")
            page.update()
