"""
Command pwd
"""


from command.command import CommandBase
from logger.logger import Logger


class CommandPWD(CommandBase):
    def get_name(self):
        return "pwd"

    def get_arguments_names(self):
        return {}

    def set_arguments(self, arguments):
        pass
        "Nothing to do"

    def run(self, engine, client, logger):
        engine.run_script("pwd")
        return True

    def stop(self):
        pass
        "Nothing to do"

    def drive_changed(self):
        pass
        "Nothing to do"
