from fastapi import APIRouter, Response
from app.models import WidgetNode, ConnectedRel
from pydantic import BaseModel


router = APIRouter(prefix="/widgets")


class WidgetCreateRequest(BaseModel):
    name: str
    ports: str = ""


@staticmethod
def validate_port_open(widget: 'WidgetNode', port: str) -> None:
    conns_all = widget.match_nodes()
    conns_of_port = [conn for conn in conns_all if conn.port == port]

    open_port_count = widget.ports.count(port) - len(conns_of_port)
    if open_port_count == 0:
        raise ValueError(f"No available ports of type '{port}' for widget id {widget.serial_number}.")


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


@router.post("/{serial_number}/connections")
async def add_widget_connection(serial_number: str, target_serial_number: str, port: str) -> None:
    source = WidgetNode.match(serial_number)
    target = WidgetNode.match(target_serial_number)
    rel = ConnectedRel(source=source, target=target, port=port)

    # TODO: validate if port is open
    # TODO: move business logic to service layer
    validate_port_open(source, port)
    validate_port_open(target, port)

    rel.merge()
    return source


@router.get("/{serial_number}/connections")
async def get_widget_connections(serial_number: str) -> list:
    widget = WidgetNode.match(serial_number)
    return widget.match_nodes()
