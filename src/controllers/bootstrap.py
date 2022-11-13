from fastapi import HTTPException

from . import books_router, authors_router
from .handlers import http_exc_handler


def setup_routers(app):
    app.include_router(books_router)
    app.include_router(authors_router)


def setup_handlers(app):
    app.add_exception_handler(HTTPException, http_exc_handler)
