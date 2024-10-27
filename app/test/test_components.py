"""
Components Test
"""

from starlette import status

from app.models import Components

from ..main import app
from ..routers.components import get_db
from .utils import TestingSessionLocal, client, override_get_db

app.dependency_overrides[get_db] = override_get_db


def test_get_all_components(_test_components):
    """
    Test get_all_components
    """
    response = client.get("/components")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "Test Ore", "is_raw_material": False, "tier": 2}
    ]


def test_get_component_by_id(_test_components):
    """
    Test get_component_by_id
    """
    response = client.get("/components/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "Test Ore",
        "is_raw_material": False,
        "tier": 2,
    }


def test_get_component_by_id_not_found(_test_components):
    """
    Test get_component_by_id when component is not found
    """
    response = client.get("/components/99")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Component not found"}


def test_create_component(_test_components):
    """
    Test create_component
    """
    request_data = {"name": "New Mat", "is_raw_material": True, "tier": 2}

    response = client.post("/components", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Components).filter(Components.id == 2).first()
    assert model.name == request_data.get("name")
    assert model.is_raw_material == request_data.get("is_raw_material")
    assert model.tier == request_data.get("tier")


def test_update_component(_test_components):
    """
    Test update_component
    """
    request_data = {"name": "New Mat", "is_raw_material": False, "tier": 4}

    response = client.put("/components/1", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Components).filter(Components.id == 1).first()
    assert model.name == request_data.get("name")
    assert model.is_raw_material == request_data.get("is_raw_material")
    assert model.tier == request_data.get("tier")


def test_update_component_not_found(_test_components):
    """
    Test update_component
    """
    request_data = {"name": "New Mat", "is_raw_material": False, "tier": 4}

    response = client.put("/components/2", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Component not found"}


def test_delete_component(_test_components):
    """
    Test delete_component
    """

    response = client.delete("/components/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Components).filter(Components.id == 1).first()
    assert model is None


def test_delete_component_not_found(_test_components):
    """
    Test delete_component
    """

    response = client.delete("/components/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Component not found"}
