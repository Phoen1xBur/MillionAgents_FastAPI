from abc import ABC, abstractmethod


class CloudManager(ABC):
    @abstractmethod
    def upload_file(self):
        raise NotImplementedError

    @abstractmethod
    def download_file(self):
        raise NotImplementedError
