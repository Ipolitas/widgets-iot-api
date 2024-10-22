from fastapi import APIRouter, Response
from app.schemas import WidgetResponse, WidgetCreateRequest, ConnectedRelResponse
from app.context import WidgetContext as ctx


router = APIRouter(prefix="/widgets")


@router.get("/{serial_number}")
async def get_widget(serial_number: str) -> WidgetResponse:
    res = await ctx.get_widget(serial_number=serial_number)
    return res


@router.post("/")
async def add_widget(widget_request: WidgetCreateRequest) -> WidgetResponse:
    res = await ctx.add_widget(
        name=widget_request.name,
        ports=widget_request.ports
    )
    return res


@router.delete("/{serial_number}")
async def remove_widget(serial_number: str) -> None:
    await ctx.remove_widget(serial_number=serial_number)
    return Response(status_code=204)


@router.post("/{serial_number}/connections")
async def add_widget_connection(serial_number: str, target_serial_number: str, port: str) -> ConnectedRelResponse:
    res = await ctx.connect_widgets(
        serial_number=serial_number,
        target_serial_number=target_serial_number,
        port=port
    )
    return res
