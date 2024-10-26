"""
Satisfactory DB Backend
"""

from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Component:
    """Component"""

    id_: int
    name: str
    is_raw_material: bool
    tier: int

    def __init__(self, id_, name, is_raw_material, tier):
        self.id_ = id_
        self.name = name
        self.is_raw_material = is_raw_material
        self.tier = tier


COMPONENTS = [
    Component(1, "Iron Ore", True, 0),
    Component(2, "Copper Ore", True, 0),
    Component(3, "Limestone", True, 0),
]


class ComponentRequest(BaseModel):
    """Component Request"""

    id_: Optional[int] = Field(description="ID is not needed on create", default=None)
    name: str = Field(min_length=1)
    is_raw_material: bool
    tier: int = Field(gt=-2)

    model_config = {
        "json_schema_extra": {
            "example": {"name": "Pioneer Ore", "is_raw_material": True, "tier": 0}
        }
    }


@app.get("/components", status_code=status.HTTP_200_OK)
async def get_all_components():
    """Get all components"""
    return COMPONENTS


@app.get("/components/", status_code=status.HTTP_200_OK)
async def get_components_by_tier(tier: int = Query(gt=-1)):
    """Get all components of a tier"""
    components_to_return = []
    for comp in COMPONENTS:
        if comp.tier == tier:
            components_to_return.append(comp)

    return components_to_return


@app.get("/components/{component_id}/", status_code=status.HTTP_200_OK)
async def get_component_by_id(component_id: int = Path(gt=0)):
    """Get a component by ID"""

    for comp in COMPONENTS:
        if comp.id_ == component_id:
            return comp

    raise HTTPException(status_code=404, detail="Component not found")


@app.post("/components/create_component", status_code=status.HTTP_201_CREATED)
async def create_component(component_request: ComponentRequest):
    """Create new component"""
    new_comp = Component(**component_request.model_dump())
    COMPONENTS.append(find_comp_id(new_comp))


@app.put("/components/update_component", status_code=status.HTTP_204_NO_CONTENT)
async def update_component(component: ComponentRequest):
    """Update a component"""
    comp_changed = False
    for i, comp in enumerate(COMPONENTS):
        if comp.id_ == component.id_:
            COMPONENTS[i] = component
            comp_changed = True

    if not comp_changed:
        raise HTTPException(status_code=404, detail="Component not found")


@app.delete("/components/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_component(component_id: int = Path(gt=0)):
    """Delete a component"""
    comp_changed = False
    for i, comp in enumerate(COMPONENTS):
        if comp.id_ == component_id:
            COMPONENTS.pop(i)
            comp_changed = True
            break

    if not comp_changed:
        raise HTTPException(status_code=404, detail="Component not found")


def find_comp_id(comp: Component):
    """Find the proper id for a new component"""
    comp.id_ = 1 if len(COMPONENTS) == 0 else COMPONENTS[-1].id_ + 1

    return comp
