from fastapi import HTTPException
from controllers.responses import Response, Error, Statuses
from starlette.requests import Request
from starlette.responses import JSONResponse


def http_exc_handler(request: Request, exc: HTTPException):  # noqa
    return JSONResponse(
        content=Response(
            status=Statuses.ERROR,
            error=Error(code=exc.status_code, message=exc.detail)).dict(),
        status_code=exc.status_code
    )
