from pydantic import BaseModel


class WidgetCreateRequest(BaseModel):
    name: str
    ports: str = ""


class WidgetResponse(BaseModel):
    serial_number: str
    name: str
    ports: str = ""


class ConnectedRelResponse(BaseModel):
    port: str = ""
