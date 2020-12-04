"""
Drive Watcher
"""


from abc import ABC, abstractmethod


class DriveListener(ABC):
    @abstractmethod
    def changed(self):
        pass


class DriveWatcherBase(ABC):
    def __init__(self):
        super(DriveWatcherBase, self).__init__()
        self._listeners = []

    def register(self, listener: DriveListener):
        if listener not in self._listeners:
            self._listeners.append(listener)
            return True
        return False

    def unregister(self, listener: DriveListener):
        self._listeners.remove(listener)

    def is_watching(self) -> bool:
        pass

    def start(self) -> bool:
        pass

    def stop(self):
        pass

    def _notify_about_changes(self):
        for listener in self._listeners:
            listener.changed()
