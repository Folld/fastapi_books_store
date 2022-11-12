from database import ASession
from fastapi import HTTPException
from sqlalchemy.orm.decl_api import DeclarativeMeta


async def check_model_id_exists(model, model_id: int, raise_exception: bool = False) -> bool:
    if not isinstance(model, DeclarativeMeta):
        raise ValueError('Model arg must be Declarative Database instance')
    async with ASession() as session:
        instance = await session.get(model, model_id)
        if not instance and raise_exception:
            raise HTTPException(detail=f'{model.__name__} id {model_id} does not exists', status_code=400)
        return bool(instance)
