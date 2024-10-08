from fastapi.exceptions import RequestValidationError
from neontology import BaseNode, BaseRelationship
from pydantic import Field, field_validator
from typing import ClassVar
import uuid


class WidgetNode(BaseNode):
    __primarylabel__: ClassVar[str] = "Widget"
    __primaryproperty__: ClassVar[str] = "serial_number"

    serial_number: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    ports: str

    @field_validator('ports')
    def validate_ports(cls, v):
        if len(v) > 3:
            raise RequestValidationError(
                "A widget can have at most 3 connection ports")
        if not cls.is_port_supported(v):
            raise RequestValidationError(
                "A widget can only have ports P, R, or Q")
        return v

    @staticmethod
    def is_port_supported(port: str) -> bool:
        return all(p in "PRQ" for p in port)


class ConnectedRel(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "CONNECTED"

    source: WidgetNode
    target: WidgetNode
