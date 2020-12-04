"""
Command ls
"""


from command.command import CommandBase
from logger.logger import Logger


class CommandLS(CommandBase):
    def __init__(self):
        self._logger = None

    def get_name(self):
        return "ls"

    def get_arguments_names(self):
        return {}

    def set_arguments(self, arguments):
        pass
        "Nothing to do"

    def run(self, engine, client, logger):
        engine.run_script("dir")
        return True

    def stop(self):
        pass
        "Nothing to do"

    def drive_changed(self):
        pass
        "Nothing to do"
