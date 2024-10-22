from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from neomodel.exceptions import NeomodelException, DoesNotExist


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def neomodel_exception_handler(request: Request, exc: NeomodelException):
    if isinstance(exc, DoesNotExist):
        return JSONResponse(
            status_code=404,
            content={"detail": "Resource not found."}
        )

    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )
