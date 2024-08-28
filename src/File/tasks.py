from src.CloudManager import CloudManager


def upload_file(cloud_manager: CloudManager, file_path: str, bucket_path: str):
    try:
        if not cloud_manager.upload_file(file_path, bucket_path):
            raise Exception('Unknown error')
    except Exception as e:
        # Запись в лог сообщения об ошибке, а так же повторное назначение задачи если это возможно
        print(f"Error uploading file: {e}")
