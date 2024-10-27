"""
Component Model
"""

from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Components(Base):
    """Components table"""

    __tablename__ = "components"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_raw_material = Column(Boolean)
    tier = Column(Integer)
