"""
Drive Client
"""


from abc import ABC, abstractmethod
from enum import Enum
from drive.drive_watcher import DriveWatcherBase


class DriveClient(ABC):
    @abstractmethod
    def list_dir(self) -> list:
        pass

    @abstractmethod
    def make_dir(self, dir_path) -> bool:
        pass

    @abstractmethod
    def remove(self, path: str) -> bool:
        pass

    @abstractmethod
    def upload_file_content(self, content: bytes, remote_file_path: str) -> bool:
        pass

    @abstractmethod
    def upload_file(self, local_file_path: str, remote_file_path: str) -> bool:
        pass

    @abstractmethod
    def download_file_content(self, remote_file_path: str) -> bytes:
        pass

    @abstractmethod
    def download_file(self, remote_file_path: str, local_file_path: str) -> bool:
        pass

    @abstractmethod
    def get_watcher(self) -> DriveWatcherBase:
        pass
