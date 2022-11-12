from fastapi import FastAPI
from books import book_router
from authors import author_router
import uvicorn
from config import uvicorn_config


app = FastAPI()

app.include_router(book_router)
app.include_router(author_router)

if __name__ == '__main__':
    uvicorn.run('main:app', **uvicorn_config)
