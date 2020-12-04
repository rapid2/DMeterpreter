"""
Command Factory
"""


from command.command import CommandBase
from command.command_ls import CommandLS
from command.command_pwd import CommandPWD
from command.command_cd import CommandCD


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
        cls._commands.append("ls")
        cls._commands.append("pwd")
        cls._commands.append("cd")

        return True

    @classmethod
    def cleanup(cls):
        cls._commands.clear()

    @classmethod
    def get_command_names(cls):
        return cls._commands

    @classmethod
    def create(cls, name) -> CommandBase:
        if name in cls._commands:
            if name == "ls":
                return CommandLS()
            elif name == "pwd":
                return CommandPWD()
            elif name == "cd":
                return CommandCD()
