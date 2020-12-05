"""
Command kill process
"""


from command.command import CommandBase
from logger.logger import Logger


class CommandKillProcess(CommandBase):
    def __init__(self):
        self._arguments = {}

    def get_name(self):
        return "kill_process"

    def get_arguments_names(self):
        return {"name": "Process name"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        name = self._arguments.get(0)
        if name:
            script = f"Stop-Process -Name {name} -Force "
            engine.run_script(script)
            return True
        logger.log_message("Name not specified")
        return False

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        return output

    def drive_changed(self):
        pass
        "Nothing to do"
