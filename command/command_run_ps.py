"""
Command run powershell
"""


import os
from command.command import CommandBase
from logger.logger import Logger


class CommandRunPS(CommandBase):
    def __init__(self):
        self._arguments = {}

    def get_name(self):
        return "run_ps"

    def get_arguments_names(self):
        return {"path": "Powershell script path"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        path = self._arguments.get(0)
        if path:
            if not os.path.isabs(path):
                if not path.startswith("."):
                    if path.startswith("/"):
                        path = "." + path
                    else:
                        path = "./" + path
            elif path.startswith("/"):
                path = "." + path
            script = "powershell -ex bypass -w hidden -f " + f"\"{path}\""
            engine.run_script(script)
            return True
        logger.log_message("Powershell script file path not specified")
        return False

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        return output

    def drive_changed(self):
        pass
        "Nothing to do"
