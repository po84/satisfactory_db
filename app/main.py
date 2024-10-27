"""
Satisfactory DB Backend
"""

from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import components

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(components.router)