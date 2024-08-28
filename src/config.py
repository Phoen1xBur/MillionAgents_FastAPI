from dotenv import load_dotenv
import os

from src import CloudManager

DOWNLOAD_DIR = os.getcwd() + '/downloads/'

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

USE_YANDEX_CLOUD = False
YNDX_AUTH = os.environ.get('YNDX_AUTH')

if USE_YANDEX_CLOUD:
    cloud_manager = CloudManager.YandexDiskCloudManager('MillionAgentsTest', YNDX_AUTH)
else:
    cloud_manager = CloudManager.EmulatorCloudManager()
