"""
Fixtures
"""

import pytest
from sqlalchemy import text

from app.models import Components

from .utils import TestingSessionLocal, engine


@pytest.fixture
def _test_components():
    """
    Component Fixture
    """
    comp = Components(name="Test Ore", is_raw_material=False, tier=2)

    db = TestingSessionLocal()
    db.add(comp)
    db.commit()
    yield comp
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM components;"))
        connection.commit()
