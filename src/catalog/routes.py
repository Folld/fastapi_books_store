from pydantic import BaseModel, Field

from fastapi import Cookie, Header, status
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv


router = InferringRouter()


@cbv(router)
class BooksView:
    class RequestDTO(BaseModel):
        name: str = Field(example='Ring of the King', title='Name of book')
        desc: str | None = Field(None, alias='description', example='Description')
        tax: float | None = Field(ge=0, le=100)
        price: float

    class ResponseDTO(BaseModel):
        name: str
        description: str | None = Field(alias='desc')
        cookie: str | None
        user_agent: str | None

    @router.post('/', response_model=ResponseDTO, response_model_by_alias=True, status_code=status.HTTP_200_OK)
    async def get_book(self,
                       item: RequestDTO,
                       cook: str | None = Cookie(default=None),
                       user_agent: str = Header(default=None)):
        return self.ResponseDTO(**item.dict(), cookie=cook, user_agent=user_agent)
