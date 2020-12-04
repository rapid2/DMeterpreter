"""
Command list programs
"""


import re
from command.command import CommandBase
from logger.logger import Logger


class CommandListPrograms(CommandBase):
    def get_name(self):
        return "list_programs"

    def get_arguments_names(self):
        return {}

    def set_arguments(self, arguments):
        pass
        "Nothing to do"

    def run(self, engine, client, logger):
        script = "dir 'C:\Program Files\';" \
                 "dir 'C:\Program Files (x86)';"
        engine.run_script(script)
        return True

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        return output

    def drive_changed(self):
        pass
        "Nothing to do"
