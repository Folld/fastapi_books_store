from fastapi import FastAPI


from carts import cart_router
from catalog import catalog_router
from books import book_router
from authors import author_router

app = FastAPI()

app.include_router(cart_router)
app.include_router(catalog_router)
app.include_router(book_router)
app.include_router(author_router)
