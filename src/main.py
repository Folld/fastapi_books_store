from pydantic import BaseModel

from fastapi import FastAPI
from typing import Union, Optional

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get('/')
async def get_books(offset: int = 0, limit: int = 10, short: bool = None):
    result = [fake_items_db[offset: offset + limit]]
    if not short:
        result.append('Those items are awesome!')
    return result
