from fastapi.exceptions import RequestValidationError
import pytest
from app.models import WidgetNode


@pytest.mark.parametrize(
    "ports", ["", "P", "R", "Q", "PR", "QQ", "PRQ", "PPP"]
    )
def test_widget_node_creation(ports: str):
    widget = WidgetNode(
        name="Test Widget",
        ports=ports
        )
    assert widget.name == "Test Widget"
    assert widget.ports == ports


@pytest.mark.parametrize(
    "ports", ["A", "PA", "RA", "Q3", "PR-", "AQQ", "AAA", "XYZ"]
    )
def test_widget_node_creation_with_invalid_ports(ports: str):
    with pytest.raises(RequestValidationError,
                       match="A widget can only have ports P, R, or Q"
                       ):
        WidgetNode(
            name="Test Widget",
            ports=ports
            )


def test_widget_node_creation_with_too_many_ports():
    with pytest.raises(RequestValidationError,
                       match="A widget can have at most 3 connection ports"
                       ):
        WidgetNode(
            name="Test Widget",
            ports="ABCD"
            )
