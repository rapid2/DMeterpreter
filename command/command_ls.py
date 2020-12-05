"""
Command ls
"""


from command.command import CommandBase
from logger.logger import Logger


class CommandLS(CommandBase):
    def __init__(self):
        self._arguments = {}

    def get_name(self):
        return "ls"

    def get_arguments_names(self):
        return {"path": "Directory path"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        path = self._arguments.get(0)
        if path:
            engine.run_script("dir " + path)
        else:
            engine.run_script("dir")
        return True

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        return output

    def drive_changed(self):
        pass
        "Nothing to do"
