import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from neomodel import NeomodelException
from .handlers import validation_exception_handler, http_exception_handler, neomodel_exception_handler

from .db import establish_connection
from .endpoints import router as widget_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Neo4j connection
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    pwd = os.getenv("NEO4J_PASSWORD")
    establish_connection(uri, user, pwd)
    yield


app = FastAPI(lifespan=lifespan)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(NeomodelException, neomodel_exception_handler)


# Include the router
app.include_router(widget_router)
