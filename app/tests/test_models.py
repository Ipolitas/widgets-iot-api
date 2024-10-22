from fastapi.exceptions import RequestValidationError
import pytest
from app.models import Widget


class TestWidgetModel:

    WIDGET_NAME = "Test Widget"

    @pytest.mark.parametrize("ports", ["", "P", "R", "Q", "PR", "QQ", "PRQ", "PPP"])
    def test_widget_node_creation(self, ports: str):
        widget = Widget(
            name=self.WIDGET_NAME,
            ports=ports
        )
        assert widget.name == self.WIDGET_NAME
        assert widget.ports == ports

    @pytest.mark.parametrize("ports", ["A", "PA", "RA", "Q3", "PR-", "AQQ", "AAA", "XYZ"])
    def test_widget_node_creation_with_invalid_ports(self, ports: str):
        expected_msg = "Port not supported. Must be one of 'P', 'R', or 'Q'."
        with pytest.raises(RequestValidationError, match=expected_msg):
            w = Widget(
                name=self.WIDGET_NAME,
                ports=ports
            )
            w.save()

    def test_widget_node_creation_with_too_many_ports(self):
        ports = "ABCD"
        max_count = 3
        port_count = len(ports)
        expected_msg = f"Maximum # of ports allowed: {max_count}. You have {port_count}."

        with pytest.raises(RequestValidationError, match=expected_msg):
            w = Widget(
                name=self.WIDGET_NAME,
                ports=ports
            )
            w.save()
