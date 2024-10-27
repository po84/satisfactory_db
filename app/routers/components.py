"""
Components Router
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal
from ..models import Components

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def get_db():
    """Get a DB connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBDependency = Annotated[Session, Depends(get_db)]


class ComponentRequest(BaseModel):
    """Component Request"""

    name: str = Field(min_length=1)
    is_raw_material: bool
    tier: int = Field(gt=-2)

    model_config = {
        "json_schema_extra": {
            "example": {"name": "Pioneer Ore", "is_raw_material": True, "tier": 0}
        }
    }


### Pages ###
@router.get("/components-page")
async def render_components_page(request: Request, db: DBDependency):
    """Componenets page rendering"""
    components = db.query(Components).all()

    return templates.TemplateResponse(
        "components.html.j2", {"request": request, "components": components}
    )


@router.get("/add-component-page")
async def render_add_component_page(request: Request):
    """Add componenet page rendering"""

    return templates.TemplateResponse("add-component.html.j2", {"request": request})


@router.get("/edit-component-page/{component_id}")
async def render_edit_component_page(
    request: Request, db: DBDependency, component_id: int = Path(gt=0)
):
    """Edit component page rendering"""
    component = db.query(Components).filter(Components.id == component_id).first()

    return templates.TemplateResponse(
        "edit-component.html.j2", {"request": request, "component": component}
    )


### Endpoints ###
@router.get("/components", status_code=status.HTTP_200_OK)
async def get_all_components(db: DBDependency):
    """Get all components"""
    return db.query(Components).all()


@router.get("/components/{component_id}", status_code=status.HTTP_200_OK)
async def get_component_by_id(db: DBDependency, component_id: int = Path(gt=0)):
    """Get a component by ID"""
    comp_model = db.query(Components).filter(Components.id == component_id).first()
    if comp_model is not None:
        return comp_model

    raise HTTPException(status_code=404, detail="Component not found")


@router.post("/components", status_code=status.HTTP_201_CREATED)
async def create_component(db: DBDependency, comp_request: ComponentRequest):
    """Create new component"""
    comp_model = Components(**comp_request.model_dump())

    db.add(comp_model)
    db.commit()


@router.put("/components/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_component(
    db: DBDependency, comp_request: ComponentRequest, component_id: int = Path(gt=0)
):
    """Update a component"""
    comp_model = db.query(Components).filter(Components.id == component_id).first()
    if comp_model is None:
        raise HTTPException(status_code=404, detail="Component not found")

    comp_model.name = comp_request.name
    comp_model.tier = comp_request.tier
    comp_model.is_raw_material = comp_request.is_raw_material

    db.add(comp_model)
    db.commit()


@router.delete("/components/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_component(db: DBDependency, component_id: int = Path(gt=0)):
    """Delete a component"""

    comp_model = db.query(Components).filter(Components.id == component_id).first()
    if comp_model is None:
        raise HTTPException(status_code=404, detail="Component not found")

    db.query(Components).filter(Components.id == component_id).delete()
    db.commit()
