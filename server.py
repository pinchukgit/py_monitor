import socketserver
import settings
import pickle
from PIL import Image
import os
from io import BytesIO
import datetime
import zlib
from base_commands import Dispatcher, Command, Invoker

screenshot_dir = os.path.join(settings.BASE_DIR, "screenshots")


class ScreenshotCommand(Command):

    def __init__(self, context):
        self.context = context

    def execute(self):
        username = self.context['username']
        file_name = self.context['name']
        date = datetime.datetime.strptime(file_name, "%Y%m%d%H%M%S%f")

        img = Image.frombytes("RGB",
                              self.context["size"],
                              zlib.decompress(self.context["bgra"]))

        path = os.path.join(
            settings.SCREEN_DIR,
            f"{username}/{date.year}/{date.month}/{date.day}"
        )
        os.makedirs(path, exist_ok=True)

        # print("SAVE_TO", os.path.join(path, self.context['name']))
        img.save(os.path.join(path, self.context['name'] + '.png'))


commands = {
    "screenshot": ScreenshotCommand
}


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        dispatcher = Dispatcher(commands)
        data = b""

        while True:
            res = self.request.recv(1024)
            if not res:
                break
            data += res
        byt = BytesIO(data)
        byt.seek(0)
        command = dispatcher("screenshot")
        invoker = Invoker(command)

        while True:
            try:
                obj = pickle.load(byt)
                print(type(obj))
            except EOFError:
                break
            else:
                invoker.run_command(obj)


if __name__ == "__main__":
    with socketserver.ForkingTCPServer(
            ("10.71.71.79", settings.SERVER_PORT), Handler) as server:
        server.serve_forever()
