import uvicorn
from fastapi import FastAPI

from src.File.router import router as router_file

app = FastAPI(
    name='MillionAgentsAPI',
    title='MillionAgentsAPI',
)

app.include_router(router_file)

if __name__ == '__main__':
    uvicorn.run('src.main:app', host='127.0.0.1', port=8000, reload=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}
