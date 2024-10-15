import pytest
from fastapi.testclient import TestClient
from app.endpoints import router
from app.models import WidgetNode

client = TestClient(router)

NAME = "Test Widget"
SERIAL_NUMBER = "12345"
PORTS = "QP"


@pytest.fixture
def mock_widget_node(mocker):
    mocker.patch.object(WidgetNode, 'match', return_value={
        "name": NAME,
        "ports": PORTS,
        "serial_number": SERIAL_NUMBER
    })

    return WidgetNode


def test_add_widget(mocker):
    mock_create = mocker.patch.object(WidgetNode, 'create', return_value=None)

    payload = {
        "name": NAME,
        "ports": PORTS
    }
    response = client.post("/widgets/", json=payload)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == NAME
    assert json_response["ports"] == PORTS
    assert mock_create.clalled_once_with(name=NAME, ports=PORTS)


def test_get_widget(mock_widget_node):
    response = client.get(f"/widgets/{SERIAL_NUMBER}")

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["serial_number"] == SERIAL_NUMBER
    assert json_response["name"] == NAME
    assert json_response["ports"] == PORTS


def test_remove_widget(mocker):
    mock_delete = mocker.patch.object(WidgetNode, 'delete', return_value=None)

    response = client.delete(f"/widgets/{SERIAL_NUMBER}")

    assert response.status_code == 204
    mock_delete.assert_called_once_with(SERIAL_NUMBER)
