"""
Command interface
"""


from abc import ABC, abstractmethod
from drive.drive_script_runner import DSRunner
from drive.drive_client import DriveClient
from logger.logger import Logger


class CommandBase(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_arguments_names(self) -> list:
        pass

    @abstractmethod
    def set_arguments(self, arguments: dict):
        pass

    @abstractmethod
    def run(self, engine: DSRunner, client: DriveClient, logger: Logger) -> bool:
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def process_output(self, output: str) -> str:
        pass

    @abstractmethod
    def drive_changed(self):
        pass
