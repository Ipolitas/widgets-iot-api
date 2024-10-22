from fastapi.exceptions import RequestValidationError
from neomodel import (StructuredNode, StructuredRel, UniqueIdProperty,
                      StringProperty, RelationshipTo)


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
            f"Maximum # of ports allowed: {max_count}. You have {port_count}.")


@staticmethod
def validate_port_compatibility(widget: 'Widget', port: str) -> None:
    if port not in widget.ports:
        raise RequestValidationError(
            f"Port {port} is not supported by widget {widget.serial_number}")


@staticmethod
def validate_port_open(widget: 'Widget', port: str) -> None:
    busy_port_count = len(widget.conn_widgets.match(port=port))
    total_port_count = widget.ports.count(port)

    open_port_count = total_port_count - busy_port_count
    if open_port_count <= 0:
        raise RequestValidationError(f"No available ports of type '{port}' for widget id {widget.serial_number}.")


class ConnectedRel(StructuredRel):
    __relationshiptype__ = "CONNECTED_TO"
    port = StringProperty(required=True)


class Widget(StructuredNode):
    __primarylabel__ = "Widget"
    __primaryproperty__ = "serial_number"

    serial_number = UniqueIdProperty()
    name = StringProperty(required=True)
    ports = StringProperty(required=True)
    # TODO: Optimization -> might want to use AsyncRelationshipTo instead
    conn_widgets = RelationshipTo("Widget", "CONNECTED_TO", model=ConnectedRel)

    def pre_save(self):
        validate_port_max_constraint(self.ports, MAX_PORTS_PER_WIDGET)
        validate_is_port_supported(self.ports)

    def validate_on_connect(self, port):
        validate_port_max_constraint(port, MAX_PORT_PER_CONNECTION)
        validate_is_port_supported(port)
        validate_port_compatibility(self, port)
        validate_port_open(self, port)
