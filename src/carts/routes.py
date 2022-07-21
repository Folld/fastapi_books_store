from pydantic import BaseModel, Field

from fastapi import Cookie, Header, status
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv


router = InferringRouter()


@cbv(router)
class CartsView:
    pass
