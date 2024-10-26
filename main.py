"""
Satisfactory DB Backend
"""

from fastapi import Body, FastAPI

app = FastAPI()


COMPONENTS = [
    {"id": 1, "name": "Iron Ore", "is_raw_material": True, "tier": 0},
    {"id": 2, "name": "Copper Ore", "is_raw_material": True, "tier": 0},
    {"id": 3, "name": "Limestone", "is_raw_material": True, "tier": 0},
]


@app.get("/components")
async def get_all_components():
    """Get all components"""
    return COMPONENTS


@app.get("/components/filters")
async def get_all_components_with_filters(is_raw_material: bool, tier: int):
    """Get all components with filters"""
    components_to_return = []
    for comp in COMPONENTS:
        if comp.get("is_raw_material") == is_raw_material and comp.get("tier") == tier:
            components_to_return.append(comp)

    return components_to_return


@app.get("/components/{component_id}/")
async def get_component_by_id(component_id: int):
    """Path Parameter and Query Parameter"""
    rv = {}

    for comp in COMPONENTS:
        if comp.get("id") == component_id:
            rv = comp

    return rv


@app.post("/components/create_component")
async def create_component(new_component=Body()):
    """Create new component"""
    COMPONENTS.append(new_component)


@app.put("/components/update_component")
async def update_component(updated_component=Body()):
    """Update a component"""
    for i, comp in enumerate(COMPONENTS):
        if comp.get("id") == updated_component.get("id"):
            COMPONENTS[i] = updated_component


@app.delete("/components/delete_component/{component_id}")
async def delete_component(component_id: int):
    """Delete a component"""
    for i, comp in enumerate(COMPONENTS):
        if comp.get("id") == component_id:
            COMPONENTS.pop(i)
