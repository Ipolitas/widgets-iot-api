from fastapi import APIRouter, Response
from app.models import ConnectedRel, Widget
from app.schemas import WidgetResponse, WidgetCreateRequest, ConnectedRelResponse
from fastapi.exceptions import RequestValidationError


router = APIRouter(prefix="/widgets")


@staticmethod
def validate_port_open(widget: 'Widget', port: str) -> None:
    busy_port_count = len(widget.conn_widgets.match(port=port))
    total_port_count = widget.ports.count(port)

    open_port_count = total_port_count - busy_port_count
    if open_port_count <= 0:
        raise RequestValidationError(f"No available ports of type '{port}' for widget id {widget.serial_number}.")


@router.get("/{serial_number}")
async def get_widget(serial_number: str) -> WidgetResponse:
    widget: Widget = Widget.nodes.get(serial_number=serial_number)
    return widget


@router.post("/")
async def add_widget(widget_request: WidgetCreateRequest) -> WidgetResponse:
    widget = Widget(
        name=widget_request.name,
        ports=widget_request.ports
    )
    widget.save()
    return widget


@router.delete("/{serial_number}")
async def remove_widget(serial_number: str) -> None:
    widget: Widget = Widget.nodes.get(serial_number=serial_number)
    widget.delete()
    return Response(status_code=204)


@router.post("/{serial_number}/connections")
async def add_widget_connection(serial_number: str, target_serial_number: str, port: str) -> ConnectedRelResponse:
    source: Widget = Widget.nodes.get(serial_number=serial_number)
    target: Widget = Widget.nodes.get(serial_number=target_serial_number)

    # TODO: move business logic to service layer
    validate_port_open(source, port)
    validate_port_open(target, port)

    connection = ConnectedRel(port=port, source=source, target=target)
    connection.save()
    return connection


@router.get("/{serial_number}/{target_serial_number}")
async def get_widget_connections(serial_number: str, target_serial_number: str) -> ConnectedRelResponse:
    source: Widget = Widget.nodes.get(serial_number=serial_number)
    target: Widget = Widget.nodes.get(serial_number=target_serial_number)

    rel = source.conn_widgets.relationship(target)
    rel.source = source
    rel.target = target
    return rel
