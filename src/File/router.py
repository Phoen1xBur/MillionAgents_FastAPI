import aiofiles
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends, BackgroundTasks
from magic import magic
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.File.models import file
from src.config import DOWNLOAD_DIR
from src.database import get_async_session
from src.utils import dir_create, dir_exists, get_unique_filename, FileExt

router = APIRouter(
    prefix='/file',
    tags=['File'],
)


def create_if_exists_dir():
    """Создание папки с сохраненными файлами в случае ее отсутствия"""
    if not dir_exists(DOWNLOAD_DIR):
        dir_create(DOWNLOAD_DIR)


@router.post('/upload')
async def upload_http(
        upload_file: UploadFile,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        create_if_exists_dir()
        # Получения уникального имени файла для сохранения, а так же его расширения
        _file: FileExt = get_unique_filename(DOWNLOAD_DIR, upload_file.filename)

        # Сохранение файла на диск
        async with aiofiles.open(DOWNLOAD_DIR + _file.name + _file.ext, 'wb') as out_file:
            content = await upload_file.read()  # async read
            await out_file.write(content)  # async write
        await upload_file.close()

        # Получение формата файла
        file_format = magic.from_buffer(content, mime=True)

        # Сохранение информации о загруженном файле в БД
        query = insert(file).values(
            path_filename=_file.name + _file.ext,
            original_name=upload_file.filename,
            format=file_format,
            extension=_file.ext,
            size=len(content),
        )
        await session.execute(query)
        await session.commit()

        return {'Result': 'OK'}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Потоковое сохранение файла на диск
@router.post('/upload_stream')
async def upload_stream(
        upload_file: UploadFile,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)
):
    create_if_exists_dir()
    # Получения уникального имени файла для сохранения, а так же его расширения
    _file: FileExt = get_unique_filename(DOWNLOAD_DIR, upload_file.filename)

    # Сохранение файла на диск
    async with aiofiles.open(DOWNLOAD_DIR + _file.name + _file.ext, 'wb') as out_file:
        Mb50 = 1024*1024*50
        chunk = await upload_file.read(Mb50)
        file_format = magic.from_buffer(chunk, mime=True)  # Получаем формат файла
        size = 0  # Размер файла в байтах
        while chunk:
            size += len(chunk)
            await out_file.write(chunk)
            chunk = await upload_file.read(Mb50)  # Получаем следующую часть файла
    await upload_file.close()

    # Сохранение информации о загруженном файле в БД
    query = insert(file).values(
        path_filename=_file.name + _file.ext,
        original_name=upload_file.filename,
        format=file_format,
        extension=_file.ext,
        size=size,
    )
    await session.execute(query)
    await session.commit()
    return {'Result': 'OK'}
