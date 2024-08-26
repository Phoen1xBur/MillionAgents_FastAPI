import os
import uuid
from time import sleep


def dir_exists(path_to_dir: str) -> bool:
    return os.path.exists(path_to_dir)


def dir_create(path_to_dir: str):
    os.mkdir(path_to_dir)


def filename_exists(path_to_file: str, filename: str) -> bool:
    return os.path.exists(path_to_file + '\\' + filename)


def get_unique_filename(path_to_file: str, filename: str) -> str:
    name, ext = os.path.splitext(filename)
    new_filename = name + '_' + uuid.uuid4().hex[:12] + ext
    if filename_exists(path_to_file, new_filename):
        return get_unique_filename(path_to_file, filename)
    return new_filename


def test_task():
    print('sleep 10s')
    sleep(10)
    print('Done')
