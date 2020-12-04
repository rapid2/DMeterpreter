"""
Command Runner
"""


import time
from command.command_factory import CommandFactory
from drive.drive_client import DriveClient
from drive.drive_watcher import DriveListener
from drive.drive_script_runner import DSRunner, DSState, DSStateListener
from logger.logger import Logger


# Script state listener
class ScriptStateListener(DSStateListener):
    def __init__(self, master):
        self._master = master

    def changed(self, state):
        self._master._script_state_changed(state)


# Drive changes listener
class DriveChangesListener(DriveListener):
    def __init__(self, master):
        self._master = master

    def changed(self):
        self._master._drive_changed()


class CommandRunner:
    def __init__(self, command_factory: CommandFactory, logger: Logger):
        self._command_factory = command_factory
        self._drive_client = None
        self._path_prefix = None
        self._drive_listener = DriveChangesListener(self)
        self._script_state_listener = None
        self._script_runner = None
        self._logger = logger
        self._current_command = None

    def init(self, drive_client: DriveClient, path_prefix: str):
        self._drive_client = drive_client
        self._path_prefix = path_prefix
        self._drive_client.get_watcher().register(self._drive_listener)
        self._script_state_listener = ScriptStateListener(self)
        self._script_runner = DSRunner()
        self._script_runner.init(drive_client, path_prefix, self._script_state_listener)

    def cleanup(self):
        self.reset()
        self._script_runner.cleanup()
        self._drive_client.get_watcher().unregister(self._drive_listener)
        self._drive_client = None
        self._path_prefix = None
        self._script_state_listener = None
        self._script_runner = None

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

    def reset(self):
        self._script_runner.reset()
        self._current_command = None

    def wait_for_finish(self, timeout=10):
        script_state = self._script_runner.get_script_state()
        while timeout > 0 and (script_state == DSState.Sending or
                               script_state == DSState.Sent or
                               script_state == DSState.Running or
                               script_state == DSState.GettingOutput):
            time.sleep(1)
            timeout -= 1
            script_state = self._script_runner.get_script_state()
        return timeout != 0

    def _script_state_changed(self, state):
        if self._current_command:
            if state == DSState.GettingOutput:
                output = self._script_runner.get_script_output()
                if output:
                    self._logger.log_message("output: " + output)
                self._script_runner.output_taken()

    def _drive_changed(self):
        if self._current_command:
            self._current_command.drive_changed()
