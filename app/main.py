"""
Satisfactory DB Backend
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status

from .database import engine
from .models import Base
from .routers import components

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def redirect_to_components_page():
    """
    Redirect to components page
    Once more categories are implemented, like recipes, home page can be serve as
    an entry point to select which category to go to. For now we go straight to the
    components page since that's the only category.
    """
    return RedirectResponse(url="/components-page", status_code=status.HTTP_302_FOUND)


app.include_router(components.router)
