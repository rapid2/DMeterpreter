"""
Command Factory
"""


from command.command import CommandBase
from command.command_ls import CommandLS


class CommandFactory:
    _commands = []
    _inited = False

    def is_inited(self):
        return _inited

    @classmethod
    def init(cls):
        if cls._inited:
            return True

        # Register commands
        # ls
        cls._commands.append("ls")

        return True

    def cleanup(self):
        cls._commands.clear()

    @classmethod
    def create(cls, name) -> CommandBase:
        if name in cls._commands:
            if name == "ls":
                return CommandLS()
