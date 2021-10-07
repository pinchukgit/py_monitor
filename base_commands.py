from abc import ABC, abstractmethod
from typing import Optional


class Command(ABC):

    @abstractmethod
    def execute(self):
        return

    def __call__(self, *args, **kwargs):
        super.__call__(*args, **kwargs)


class Dispatcher:

    """
        :param commands: dict, key = command name, value = command object
    """
    def __init__(self, commands: dict) -> None:
        self.commands = commands

    def __call__(self, command_name: str) -> Optional[Command]:
        return self.commands.get(command_name)


class Invoker:

    _on_start = None
    _on_stop = None

    def __init__(self, command: Command):
        self.command = command

    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_stop(self, command: Command):
        self._on_stop = command

    def run_command(self, *args, **kwargs):

        if isinstance(self._on_start, Command):
            self._on_start.execute()

        command = self.command(*args, **kwargs)
        command.execute()

        if isinstance(self._on_stop, Command):
            self._on_stop.execute()
