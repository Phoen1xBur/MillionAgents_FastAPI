from src.CloudManager.CloudManager import CloudManager


def upload_file(cloud_manager: CloudManager, file_path: str, bucket_path: str):
    try:
        cloud_manager.upload_file(file_path, bucket_path)
    except Exception as e:
        print(f"Error uploading file: {e}")
