"""
Dropbox Watcher
"""


import threading
import client_dropbox
from drive.drive_watcher import DriveWatcherBase


class DropboxWatcher(DriveWatcherBase):
    def __init__(self, _dropbox):
        super(DropboxWatcher, self).__init__()
        self._dropbox = _dropbox
        self._watching = False
        self._thread_watcher = None

    def is_watching(self) -> bool:
        return self._watching

    def start(self) -> bool:
        if self._watching:
            return True

        self._watching = True
        self._thread_watcher = threading.Thread(target=self._watch)
        self._thread_watcher.start()

    def stop(self):
        self._watching = False
        if self._thread_watcher:
            if self._thread_watcher.is_alive():
                self._thread_watcher.join()

    def _watch(self):
        while self._dropbox and self._watching:
            response = self._dropbox.files_list_folder("")
            if response:
                result = self._dropbox.files_list_folder_longpoll(response.cursor)
                changed = result.changes
                if changed:
                    super()._notify_about_changes()
