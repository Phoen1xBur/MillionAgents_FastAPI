from enum import Enum

import requests
from src.CloudManager.CloudManager import CloudManager


class UrlType(str, Enum):
    download = 'download'
    upload = 'upload'


class YandexDiskCloudManager(CloudManager):
    """
    Реализация класса для работы с сервисом Яндекс Диск
    API doc: https://yandex.ru/dev/disk-api/doc/ru/
    """
    def __init__(self, app_name: str, OAuthToken: str):
        self.app_name = app_name
        self._api_key = OAuthToken

    def upload_file(self, file_path: str, bucket_path: str):
        """
        Загружает файл в Яндекс Диск
        :param file_path: путь к файлу который нужно загрузить
        :param bucket_path: путь для файла в Яндекс Диск
        :return: True если файл успешно загружен, False если не удалось
        """
        upload_url = self._get_url(UrlType.upload, bucket_path)
        data = requests.put(upload_url, headers=self._get_headers(), files={'file': open(file_path, 'rb')})
        print(data, data.content)

        # 201 - Файл загружен успешно
        return data.status_code == 201

    def download_file(self, file_path: str, bucket_path: str):
        """
        Загружает файл из Яндекс Диска
        :param file_path: путь куда нужно сохранить файл
        :param bucket_path: путь до файла в Яндекс Диск, который нужно скачать
        :return: True если файл успешно скачан, False если не удалось
        """
        download_url = self._get_url(UrlType.download, bucket_path)

    def _get_headers(self) -> dict:
        token = self._api_key if self._api_key.startswith('OAuth') else 'OAuth ' + self._api_key
        return {
            'Authorization': token
        }

    def _get_url(self, url_type: UrlType, bucket_path: str) -> str:
        url = f'https://cloud-api.yandex.net/v1/disk/resources/{url_type.value}?path=disk:/Приложения/{self.app_name}/{bucket_path}'
        data = requests.get(url, headers=self._get_headers())
        href_url = data.json()['href']
        print(href_url)
        return href_url


if __name__ == '__main__':
    cloud_manager = YandexDiskCloudManager('MillionAgentsTest', 'OAuth y0_AgAAAAAUe_XeAAxP6gAAAAEOgy_LAAD1PBizqghGP5G5EqB2qRF-CuQCbQ')
    cloud_manager.upload_file('file_path', 'bucket_path')
