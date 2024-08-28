from src.CloudManager.CloudManager import CloudManager


class EmulatorCloudManager(CloudManager):
    def upload_file(self, file_path, bucket_path) -> bool:
        return True

    def download_file(self, file_path, bucket_path) -> bool:
        return True
