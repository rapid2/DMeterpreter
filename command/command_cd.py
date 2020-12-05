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
        path = self._arguments.get(0)
        if path:
            script = "cd " + f"\"{path}\""
            engine.run_script(script)
            return True
        logger.log_message("Remote path not specified")
        return False

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        return output

    def drive_changed(self):
        pass
        "Nothing to do"
