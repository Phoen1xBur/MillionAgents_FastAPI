import aiofiles
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends, BackgroundTasks
import magic
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.File.models import File
from src.File.schemas import SFile
from src.File.tasks import upload_file as upload_file_task
from src.config import DOWNLOAD_DIR, cloud_manager
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


@router.post('/upload', response_model=SFile)
async def upload_http(
        upload_file: UploadFile,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)
):
    """Сохранение файла"""
    try:
        create_if_exists_dir()
        # Получения уникального имени файла для сохранения, а так же его расширения
        _file: FileExt = get_unique_filename(DOWNLOAD_DIR, upload_file.filename)

        # Сохранение файла на диск
        async with aiofiles.open(DOWNLOAD_DIR + _file.fullname, 'wb') as out_file:
            content = await upload_file.read()  # async read
            await out_file.write(content)  # async write
        await upload_file.close()

        # Получение формата файла
        file_format = magic.from_buffer(content, mime=True)

        # Сохранение информации о загруженном файле в БД
        file = File(
            path_filename=_file.fullname,
            original_name=upload_file.filename,
            format=file_format,
            extension=_file.ext,
            size=len(content),
        )
        session.add(file)
        await session.commit()

        background_tasks.add_task(upload_file_task, cloud_manager, DOWNLOAD_DIR + _file.fullname, _file.fullname)

        return SFile.model_validate(file, from_attributes=True)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Потоковое сохранение файла на диск
@router.post('/upload_stream', response_model=SFile)
async def upload_stream(
        upload_file: UploadFile,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)
):
    """Потоковое сохранение файла"""
    try:
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
        file = File(
            path_filename=_file.fullname,
            original_name=upload_file.filename,
            format=file_format,
            extension=_file.ext,
            size=size,
        )
        session.add(file)
        await session.commit()

        background_tasks.add_task(upload_file_task, cloud_manager, DOWNLOAD_DIR + _file.fullname, _file.fullname)

        return SFile.model_validate(file, from_attributes=True)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/get/{file_id}')
async def download_file(file_id: int, download: bool = False, session: AsyncSession = Depends(get_async_session)):
    """Получение файла по id"""
    try:
        _file = await session.get(File, file_id)
        if not _file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')

        if download:
            return FileResponse(
                DOWNLOAD_DIR + _file.path_filename,
                media_type=_file.format,
                filename=_file.original_name
            )
        else:
            return SFile.model_validate(_file, from_attributes=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
