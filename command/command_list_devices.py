"""
Command list devices
"""


import re
from command.command import CommandBase
from logger.logger import Logger


class CommandListDevices(CommandBase):
    def get_name(self):
        return "list_devices"

    def get_arguments_names(self):
        return {}

    def set_arguments(self, arguments):
        pass
        "Nothing to do"

    def run(self, engine, client, logger):
        script = "Get-PnpDevice -PresentOnly;"
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
