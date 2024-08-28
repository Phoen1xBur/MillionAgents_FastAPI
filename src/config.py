from dotenv import load_dotenv
import os

from src.CloudManager.YandexDiskCloudManager import YandexDiskCloudManager

DOWNLOAD_DIR = os.getcwd() + '\\downloads\\'

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

YNDX_AUTH = os.environ.get('YNDX_AUTH')

cloud_manager = YandexDiskCloudManager('MillionAgentsTest', YNDX_AUTH)

