from fastapi import HTTPException, status


class BaseError(HTTPException):
    ...


class BookNotFoundError(BaseError):
    def __init__(self, detail='Книга не найдена', status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail=detail)
