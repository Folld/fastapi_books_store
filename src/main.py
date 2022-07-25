from fastapi import FastAPI
from books import book_router
from authors import author_router

app = FastAPI()

app.include_router(book_router)
app.include_router(author_router)
