"""
Command Runner
"""


from command.command_factory import CommandFactory
from drive.drive_client import DriveClient
from drive.drive_script_runner import DSRunner, DSState, DSStateListener
from logger.logger import Logger


# Script state listener
class ScriptStateListener(DSStateListener):
    def __init__(self, master):
        self._master = master

    def changed(self, state):
        self._master._script_state_changed(state)


class CommandRunner:
    def __init__(self, command_factory: CommandFactory, drive_client: DriveClient, path_prefix, logger: Logger):
        self._command_factory = command_factory
        self._drive_client = drive_client
        self._path_prefix = path_prefix
        self._script_state_listener = ScriptStateListener(self)
        self._script_runner = DSRunner(drive_client, path_prefix, self._script_state_listener)
        self._logger = logger
        self._current_command = None

    def reset(self):
        self._script_runner.reset()
        self._current_command = None

    def run(self, name: str, arguments: dict):
        try:
            script_state = self._script_runner.get_script_state()
            if script_state == DSState.Initial or script_state == DSState.Finished:
                command = self._command_factory.create(name)
                if command:
                    self._current_command = command
                    command.set_arguments(arguments)
                    if not command.run(self._script_runner, self._drive_client, self._logger):
                        self._logger.log_message(f"Failed to run '{command.get_name()}' command")
                else:
                    self._logger.log_message(f"Command '{name}' not found")
            else:
                self._logger.log_message("Command runner is busy")
        except Exception as ex:
            self._logger.log_message(str(ex))

    def _script_state_changed(self, state):
        if self._current_command:
            self._logger.log_message(f"({self._current_command.get_name()}) State: " + state.name)
            if state == DSState.Finished:
                output = self._script_runner.get_script_output()
                self._logger.log_message("output: " + output)
