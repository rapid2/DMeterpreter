"""
Command get antivirus name
"""


import re
from command.command import CommandBase
from logger.logger import Logger


class CommandGetAVName(CommandBase):
    def get_name(self):
        return "get_av_name"

    def get_arguments_names(self):
        return {}

    def set_arguments(self, arguments):
        pass
        "Nothing to do"

    def run(self, engine, client, logger):
        script = "$AntivirusProduct = Get-WmiObject -Namespace \"root\SecurityCenter2\" -Query \"SELECT * FROM AntiVirusProduct\"  @psboundparameters;" \
                 "Write-host $AntivirusProduct.displayName;"
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
