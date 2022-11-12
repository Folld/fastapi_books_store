from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, root_validator
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class Statuses(str, Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


class Error(BaseModel):
    code: int
    message: str


class Response(GenericModel, Generic[DataT]):
    status: Statuses = 'SUCCESS'
    error: Optional[Error]
    data: Optional[DataT]

    @root_validator
    def check_consistency(cls, values):
        error = values['error']
        if error is not None and values['data'] is not None:
            raise ValueError('must not provide both data and error')
        if error is None and values.get('data') is None:
            raise ValueError('must provide data or error')
        return values
