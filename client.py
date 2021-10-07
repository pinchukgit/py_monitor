import socket
import threading
import settings
import os
import time


class Sender:

    def __init__(self, server_address):
        self.server_address = server_address
        self.socket = None

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.server_address)

    def send(self, data):
        self.socket.sendall(data)


class ScreenshotSenderThread(threading.Thread):
    def __init__(self, screen_maker):
        super().__init__()
        self.screen_maker = screen_maker

    def run(self):
        screen_dir = os.path.join(settings.BASE_DIR, "screenshots")
        while True:
            files = os.listdir(screen_dir)
            for file in files:
                try:
                    sender = Sender((settings.SERVER_IP,
                                     settings.SERVER_PORT))
                    sender.create_socket()
                except ConnectionRefusedError:
                    time.sleep(4)
                    continue
                if self.screen_maker.file and self.screen_maker.filename == \
                        file:
                    continue
                file_path = os.path.join(screen_dir, file)
                f = open(file_path, "rb")
                try:
                    sender.send(f.read())
                except ConnectionResetError:
                    continue
                f.close()
                os.remove(file_path)
            time.sleep(10)





