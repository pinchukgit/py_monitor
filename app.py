import threading
import argparse
import client
import screenshots
import settings
from base_commands import Dispatcher, Command
import os


class ScreenshotCommand(Command):

    def __init__(self, *args, **kwargs):
        self.username = kwargs.get("username")

    def execute(self):
        os.makedirs(settings.SCREEN_DIR, exist_ok=True)
        screenshot_maker = screenshots.Screenshot(username=self.username)
        sender = client.ScreenshotSenderThread(screenshot_maker)
        sender.start()
        thread = threading.Thread(target=screenshot_maker.run_infinitive)
        thread.start()
        return thread


commands = {
    "screenshot": ScreenshotCommand
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--commands", action="append")
    parser.add_argument("--username")

    arguments = parser.parse_args()
    dispatcher = Dispatcher(commands)

    if not arguments.username:
        parser.print_help()
        exit(1)

    join_threads = []

    for command in arguments.commands:
        command_class = dispatcher(command)
        c = command_class(username=arguments.username)
        result = c.execute()
        if isinstance(result, threading.Thread):
            join_threads.append(result)

    for thread in join_threads:
        thread.join()
