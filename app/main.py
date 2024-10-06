from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .models import WidgetNode
from .db import Neo4jConnection
from typing import ClassVar, Optional, List
from neontology import BaseNode, BaseRelationship


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Initialize Neo4j connection
conn = Neo4jConnection()


class FollowsRel(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "FOLLOWS"

    source: WidgetNode
    target: WidgetNode


@app.get("/")
def read_root():
    res = conn.query("MATCH (n) RETURN COUNT(n) as count")
    return {"node_count": res[0]["count"]}


@app.post("/widgets/")
async def add_widget(name: str, ports: str = ""):
    widget = WidgetNode(
        name=name,
        ports=ports
        )
    widget.create()
    return widget


@app.post("/tester/")
async def run_test():
    alice = WidgetNode(name="Motion Sensor")
    bob = WidgetNode(name="Speaker")

    alice.create()
    bob.create()

    return "done"


# Close the connection on shutdown
@app.on_event("shutdown")
def shutdown():
    conn.close()
