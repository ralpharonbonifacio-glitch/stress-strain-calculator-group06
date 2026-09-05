try:
    from .properties import MaterialProperties 
    from .material import Material, Metal, Plastic, Composite
except ImportError:
    from properties import MaterialProperties
    from material import Material, Metal, Plastic, Composite

STEEL_PROPERTIES = MaterialProperties( density=7850, yield_strength=250, typical_youngs_modulus=200 )
ALUMINUM_PROPERTIES = MaterialProperties( density=2700, yield_strength=95, typical_youngs_modulus=69 )
TITANIUM_PROPERTIES = MaterialProperties( density=4500, yield_strength=880, typical_youngs_modulus=114 )
STEEL = Metal( name="Steel", properties=STEEL_PROPERTIES )
ALUMINUM = Metal( name="Aluminum", properties=ALUMINUM_PROPERTIES )
TITANIUM = Metal( name="Titanium", properties=TITANIUM_PROPERTIES )

MATERIAL_DATABASE = {
    "Steel": STEEL, 
    "Aluminum": ALUMINUM, 
    "Titanium": TITANIUM
}


def get_all_materials() -> dict:
    """Return all materials in the database."""
    return MATERIAL_DATABASE.copy()

def get_material(name: str) -> Material:
    if name not in MATERIAL_DATABASE:
        raise KeyError(f"Material '{name}' was not found." )
    return MATERIAL_DATABASE[name]

def material_exists(name: str) -> bool:
    return name in MATERIAL_DATABASE
