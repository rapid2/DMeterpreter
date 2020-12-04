"""
Command ls
"""


from command.command import CommandBase
from logger.logger import Logger


class CommandCD(CommandBase):
    def __init__(self):
        self._arguments = {}

    def get_name(self):
        return "cd"

    def get_arguments_names(self):
        return {"path": "Directory path"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        path = self._arguments.get("path")
        if not path:
            path = self._arguments.get(0)
        if path:
            engine.run_script("cd " + path)
            return True
        logger.log_message("'path' argument is missing")
        return False

    def stop(self):
        pass
        "Nothing to do"

    def drive_changed(self):
        pass
        "Nothing to do"
