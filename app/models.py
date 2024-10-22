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
def validate_ports_compatibility(source: 'Widget', target: 'Widget', port: str) -> None:
    if port not in source.ports or port not in target.ports:
        raise RequestValidationError(
            f"Port {port} is not supported by both widgets.")


class ConnectedRel(StructuredRel):
    __relationshiptype__ = "CONNECTED_TO"
    port = StringProperty(required=True)

    def save(self, *args, **kwargs):
        validate_port_max_constraint(self.port, MAX_PORTS_PER_WIDGET)
        validate_is_port_supported(self.port)
        validate_ports_compatibility(self.source, self.target, self.port)

        return super().save(*args, **kwargs)


class Widget(StructuredNode):
    __primarylabel__ = "Widget"
    __primaryproperty__ = "serial_number"

    serial_number = UniqueIdProperty()
    name = StringProperty(required=True)
    ports = StringProperty(required=True)
    # TODO: Optimization -> might want to use AsyncRelationshipTo instead
    conn_widgets = RelationshipTo("Widget", "CONNECTED_TO", model=ConnectedRel)

    def save(self, *args, **kwargs):
        validate_port_max_constraint(self.ports, MAX_PORTS_PER_WIDGET)
        validate_is_port_supported(self.ports)

        return super().save(*args, **kwargs)
