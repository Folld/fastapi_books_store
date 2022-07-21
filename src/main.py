from fastapi import FastAPI
from carts import cart_router
from catalog import catalog_router

app = FastAPI()


app.include_router(cart_router)
app.include_router(catalog_router)
