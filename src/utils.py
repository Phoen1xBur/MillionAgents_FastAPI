import os
import uuid
from typing import NamedTuple

FileExt = NamedTuple(
    'FileExt',
    name=str,
    ext=str,
)


def dir_exists(path_to_dir: str) -> bool:
    """Проверка наличия директории"""
    return os.path.exists(path_to_dir)


def dir_create(path_to_dir: str):
    """Создание директории"""
    os.mkdir(path_to_dir)


def filename_exists(path_to_file: str, filename: str) -> bool:
    """Проверка наличия файла"""
    return os.path.exists(path_to_file + '\\' + filename)


def get_unique_filename(path_to_file: str, filename: str) -> FileExt:
    """Получение уникального имени файла"""
    def generate_filename(_filename):
        """Генерация хэша к имени файла для уникальности"""
        return _filename + '_' + uuid.uuid4().hex[:12]

    # Извлечение имени и расширения
    name, ext = os.path.splitext(filename)
    new_filename = name

    # Проверка наличия полученного имени в директории
    while filename_exists(path_to_file, new_filename + ext):
        # Если имя уже существует, генерируем новое
        new_filename = generate_filename(name)
    # Возвращаем уникальное имя с расширением этого файла
    return FileExt(new_filename, ext)
