from fastapi.exceptions import RequestValidationError
from neontology import BaseNode, BaseRelationship
from pydantic import Field, field_validator
from typing import ClassVar
import uuid


MAX_PORTS_PER_WIDGET = 3
MAX_PORT_PER_CONNECTION = 1


@staticmethod
def validate_is_port_supported(port: str) -> None:
    if not all(p in "PRQ" for p in port):
        raise RequestValidationError("Port not supported. " +
                                     "Must be one of 'P', 'R', or 'Q'.")
    return port


@staticmethod
def validate_port_max_constraint(ports: str, max_count: int) -> None:
    port_count = len(ports)
    if port_count > max_count:
        raise RequestValidationError(
            f"Maximum amount of ports allowed: {max_count}. You have {port_count} ports.")


class WidgetNode(BaseNode):
    __primarylabel__: ClassVar[str] = "Widget"
    __primaryproperty__: ClassVar[str] = "serial_number"

    serial_number: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    ports: str

    @field_validator('ports')
    @classmethod
    def validate_ports(cls, v: str):
        validate_port_max_constraint(v, MAX_PORTS_PER_WIDGET)
        validate_is_port_supported(v)
        return v


class ConnectedRel(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "CONNECTED"

    source: WidgetNode
    target: WidgetNode
    port: str

    @field_validator('port')
    @classmethod
    def validate_ports(cls, v: str):
        validate_port_max_constraint(v, MAX_PORT_PER_CONNECTION)
        validate_is_port_supported(v)
        return v
