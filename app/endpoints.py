from fastapi import APIRouter, Response
from app.models import WidgetNode
from pydantic import BaseModel


router = APIRouter(prefix="/widgets")


class WidgetCreateRequest(BaseModel):
    name: str
    ports: str = ""


@router.get("/{serial_number}")
async def get_widget(serial_number: str) -> WidgetNode:
    widget = WidgetNode.match(serial_number)
    return widget


@router.post("/")
async def add_widget(widget_request: WidgetCreateRequest) -> WidgetNode:
    widget = WidgetNode(
        name=widget_request.name,
        ports=widget_request.ports
    )
    widget.create()
    return widget


@router.delete("/{serial_number}")
async def remove_widget(serial_number: str) -> None:
    WidgetNode.delete(serial_number)
    return Response(status_code=204)
