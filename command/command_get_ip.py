"""
Command get ip
"""


import re
from command.command import CommandBase
from logger.logger import Logger


class CommandGetIp(CommandBase):
    def get_name(self):
        return "get_ip"

    def get_arguments_names(self):
        return {}

    def set_arguments(self, arguments):
        pass
        "Nothing to do"

    def run(self, engine, client, logger):
        script = "$wc=New-Object net.webclient;" \
                 "$wc.downloadstring('http://checkip.dyndns.com');"
        engine.run_script(script)
        return True

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ls = pattern.search(output)
        if ls:
            return ls[0]
        return output

    def drive_changed(self):
        pass
        "Nothing to do"
