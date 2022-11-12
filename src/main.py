from fastapi import FastAPI, HTTPException
from config import uvicorn_config

from books import book_router
from authors import author_router
import uvicorn

from utils.handlers import http_exc_handler

app = FastAPI()

app.include_router(book_router)
app.include_router(author_router)
app.add_exception_handler(HTTPException, http_exc_handler)


if __name__ == '__main__':
    uvicorn.run('main:app', **uvicorn_config)
