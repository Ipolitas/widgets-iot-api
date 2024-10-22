from fastapi.exceptions import RequestValidationError
import pytest
from app.models import ConnectedRel, WidgetNode


class TestWidgetNodeModel:

    WIDGET_NAME = "Test Widget"

    @pytest.mark.parametrize("ports", ["", "P", "R", "Q", "PR", "QQ", "PRQ", "PPP"])
    def test_widget_node_creation(self, ports: str):
        widget = WidgetNode(
            name=self.WIDGET_NAME,
            ports=ports
        )
        assert widget.name == self.WIDGET_NAME
        assert widget.ports == ports

    @pytest.mark.parametrize("ports", ["A", "PA", "RA", "Q3", "PR-", "AQQ", "AAA", "XYZ"])
    def test_widget_node_creation_with_invalid_ports(self, ports: str):
        expected_msg = "Port not supported. Must be one of 'P', 'R', or 'Q'."
        with pytest.raises(RequestValidationError, match=expected_msg):
            WidgetNode(
                name=self.WIDGET_NAME,
                ports=ports
            )

    def test_widget_node_creation_with_too_many_ports(self):
        ports = "ABCD"
        max_count = 3
        port_count = len(ports)
        expected_msg = f"Maximum # of ports allowed: {max_count}. You have {port_count}."

        with pytest.raises(RequestValidationError, match=expected_msg):
            WidgetNode(
                name=self.WIDGET_NAME,
                ports=ports
            )


class TestConnectedRelModel:

    @pytest.fixture
    def widget_nodes_compatible(self):
        widget1 = WidgetNode(name="Widget 1", ports="PRQ")
        widget2 = WidgetNode(name="Widget 2", ports="R")
        return widget1, widget2

    @pytest.fixture
    def widget_nodes_uncompatible(self):
        widget1 = WidgetNode(name="Widget 1", ports="PQ")
        widget2 = WidgetNode(name="Widget 2", ports="R")
        return widget1, widget2

    def _create_connection(self, widget1, widget2, port):
        return ConnectedRel(
            source=widget1,
            target=widget2,
            port=port
        )

    def test_creation(self, widget_nodes_compatible):
        port = "R"
        widget1, widget2 = widget_nodes_compatible
        rel = self._create_connection(widget1, widget2, port)

        assert rel.source == widget1
        assert rel.target == widget2
        assert rel.port == "R"

    def test_creation_validate_port_compatibility(self, widget_nodes_uncompatible):
        port = "R"
        widget1, widget2 = widget_nodes_uncompatible
        expected_msg = f"Port {port} is not supported by both widgets."

        with pytest.raises(RequestValidationError, match=expected_msg):
            self._create_connection(widget1, widget2, port)

    def test_creation_validate_port_max_constraint(self, widget_nodes_compatible):
        port = "PR"
        widget1, widget2 = widget_nodes_compatible
        max_count = 1
        expected_msg = f"Maximum # of ports allowed: {max_count}. You have {len(port)}."

        with pytest.raises(RequestValidationError, match=expected_msg):
            self._create_connection(widget1, widget2, port)

    def test_creation_validate_port_type(self, widget_nodes_compatible):
        port = "A"
        widget1, widget2 = widget_nodes_compatible
        expected_msg = "Port not supported. Must be one of 'P', 'R', or 'Q'."

        with pytest.raises(RequestValidationError, match=expected_msg):
            self._create_connection(widget1, widget2, port)
