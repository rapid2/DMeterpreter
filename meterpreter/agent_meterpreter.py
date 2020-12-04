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
        self._command_factory = CommandFactory()
        self._command_runner = None
        self._logger = logger

        self._command_factory.init()

    def init(self, drive_client: DriveClient, agent_id: str):
        if self._command_runner:
            return False

        self._command_runner = CommandRunner(self._command_factory, drive_client, "/" + agent_id, self._logger)
        return True

    def cleanup(self):
        self._command_runner = None

    def run_command(self, name: str, args: dict):
        if self._command_runner:
            self._command_runner.run(name, args)
