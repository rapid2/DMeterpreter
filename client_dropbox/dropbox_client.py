"""
Dropbox Client
"""


import dropbox
from drive.drive_client import DriveClient
from client_dropbox.dropbox_watcher import DropboxWatcher
from third_party.requester import get_encoding


class DropboxClient(DriveClient):
    def __init__(self):
        super(DropboxClient, self).__init__()
        self._dropbox = None
        self._dropbox_watcher = None

    def init(self, token):
        self.cleanup()

        self._dropbox = dropbox.Dropbox(token)
        self._dropbox_watcher = DropboxWatcher(self._dropbox)
        self._dropbox_watcher.start()

    def cleanup(self):
        if self._dropbox:
            self._dropbox.close()
            self._dropbox = None
        if self._dropbox_watcher:
            self._dropbox_watcher.stop()
            self._dropbox_watcher.stop()
            self._dropbox_watcher = None

    def list_dir(self, dir_path):
        _list = []
        if not self._dropbox:
            return _list

        response = self._dropbox.files_list_folder(dir_path)
        for file in response.entries:
            _list.append(file.name)
        while response.has_more:
            self._dropbox.files_list_folder_continue(response.cursor)
            for file in response.entries:
                _list.append(file.name)
        return _list

    def make_dir(self, dir_path):
        if not self._dropbox:
            return False

        result = self._dropbox.files_create_folder_v2(dir_path)
        return result is not None

    def remove(self, path: str):
        if not self._dropbox:
            return False

        try:
            result = self._dropbox.files_delete_v2(path)
            return result is not None
        except Exception as ex:
            print(f"Exception: {str(ex)}]")
        return False

    def upload_file_content(self, content, encoding, remote_file_path):
        if not self._dropbox:
            return False

        result = self._dropbox.files_upload(bytes(content, encoding), remote_file_path, mute=True)
        return result is not None

    def upload_file(self, local_file_path, remote_file_path):
        if not self._dropbox:
            return False

        with open(local_file_path, "rb") as file:
            result = self._dropbox.files_upload(file.read(), remote_file_path, mute=True)
        return result is not None

    def download_file_content(self, remote_file_path):
        if not self._dropbox:
            return False

        result = self._dropbox.files_download(remote_file_path)
        try:
            encoding = get_encoding(result[1])
            result = result[1].content.decode(encoding)
        except Exception as ex:
            result = result[1].content
            print(f"Exception: {str(ex)}]")
        return result

    def download_file(self, remote_file_path, local_file_path):
        if not self._dropbox:
            return False

        result = self._dropbox.files_download_to_file(local_file_path, remote_file_path)
        return result is not None

    def get_watcher(self):
        return self._dropbox_watcher
