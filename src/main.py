import asyncio
import os
import aiofiles
import magic
import uvicorn
from fastapi import FastAPI, UploadFile, Request, HTTPException, status
from src.config import DOWNLOAD_DIR
from src.utils import dir_exists, dir_create, filename_exists, get_unique_filename, test_task

app = FastAPI(
    name='MillionAgentsAPI',
    title='MillionAgentsAPI',
)

if __name__ == '__main__':
    uvicorn.run('src.main:app', host='127.0.0.1', port=8000, reload=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def post(upload_file: UploadFile):
    if not dir_exists(DOWNLOAD_DIR):
        dir_create(DOWNLOAD_DIR)

    # Уникальное имя файла
    path_filename = upload_file.filename
    if filename_exists(DOWNLOAD_DIR, upload_file.filename):
        path_filename = get_unique_filename(DOWNLOAD_DIR, upload_file.filename)

    async with aiofiles.open(DOWNLOAD_DIR + path_filename, 'wb') as out_file:
        content = await upload_file.read()  # async read
        await out_file.write(content)  # async write
    await upload_file.close()
    format = magic.from_buffer(content, mime=True)
    return {'Result': 'OK'}


@app.post('/upload')
async def upload(request: Request):
    filename = request.headers.get('Filename')
    if not filename:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='The request header must specify the name of the file being uploaded')
    return {'Result': 'OK'}
