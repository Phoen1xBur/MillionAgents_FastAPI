from abc import ABC, abstractmethod


class CloudManager(ABC):
    @abstractmethod
    def upload_file(self, file_path, bucket_path) -> bool:
        raise NotImplementedError

    @abstractmethod
    def download_file(self, file_path, bucket_path) -> bool:
        raise NotImplementedError
