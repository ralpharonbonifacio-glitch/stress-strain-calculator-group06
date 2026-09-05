import json
from pathlib import Path

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

DATA_FILE = Path("materials.json")

def save_materials() -> None:
    data = {}

    for name, material in MATERIAL_DATABASE.items():
        data[name] = {
            "density": material.properties.density,
            "yield_strength": material.properties.yield_strength,
            "youngs_modulus": material.properties.typical_youngs_modulus
        }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_materials() -> None:
    if not DATA_FILE.exists():
        return

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    for name, values in data.items():
        properties = MaterialProperties(
            density=values["density"],
            yield_strength=values["yield_strength"],
            typical_youngs_modulus=values["youngs_modulus"]
        )

        MATERIAL_DATABASE[name] = Material(
            name=name,
            properties=properties
        )

def get_all_materials() -> dict:
    """Return all materials in the database."""
    return MATERIAL_DATABASE.copy()

def get_material(name: str) -> Material:
    if name not in MATERIAL_DATABASE:
        raise KeyError(f"Material '{name}' was not found." )
    return MATERIAL_DATABASE[name]

def material_exists(name: str) -> bool:
    return name in MATERIAL_DATABASE
def add_material(material: Material) -> None:
    if material.name in MATERIAL_DATABASE:
        raise ValueError( f"Material '{material.name}' already exists." )
    MATERIAL_DATABASE[material.name] = material
def remove_material(name: str) -> Material:
    if name not in MATERIAL_DATABASE:
        raise KeyError( f"Material '{name}' was not found." )
    return MATERIAL_DATABASE.pop(name)

def get_material_names() -> list[str]:
    return list(MATERIAL_DATABASE.keys())
def get_material_names_tuple() -> tuple[str, ...]:
    return tuple(MATERIAL_DATABASE.keys())

def get_material_categories() -> dict:
    return { "Metal": [ 
        name 
        for name, material in MATERIAL_DATABASE.items() 
        if isinstance(material, Metal) ],
        "Plastic": [ 
            name 
            for name, 
            material in MATERIAL_DATABASE.items() 
            if isinstance(material, Plastic) ],
            "Composite": [ 
                name 
                for name, 
                material in MATERIAL_DATABASE.items() 
                if isinstance(material, Composite) ] }

def get_materials_by_category(category: str) -> list[Material]:
    category = category.lower()
    if category == "metal": 
        material_class = Metal
    elif category == "plastic": 
        material_class = Plastic
    elif category == "composite":
        material_class = Composite
    else:
        raise ValueError( "Invalid category. " "Choose Metal, Plastic, or Composite." )
    return [material for material in MATERIAL_DATABASE.values() 
            if isinstance(material, material_class)]

def create_and_add_custom_material(
        name: str, 
        yield_strength: float, 
        youngs_modulus: float, 
        density: float = 1.0
) -> Material:

    if material_exists(name):
        raise ValueError( f"Material '{name}' already exists." )
    properties = MaterialProperties( 
        density=density, 
        yield_strength=yield_strength, 
        typical_youngs_modulus=youngs_modulus)
    material = Material( 
        name=name, 
        properties=properties)
    add_material(material)
    return material
def display_material_database() -> None:
    print("\n=== MATERIAL DATABASE ===")
    if not MATERIAL_DATABASE:
        print("No materials available.") 
        return
    for material in MATERIAL_DATABASE.values():
        print(f"\nMaterial: {material.name}") 
        material.properties.display()
if __name__ == "__main__":
    print("=== Database Test ===")
    print("\nAvailable materials:")
    for name in get_material_names(): 
        print(f"- {name}")
    print("\nSteel properties:") 
    get_material("Steel").properties.display()
    print("\nMaterial categories:")
    categories = get_material_categories()
    for category, materials in categories.items(): 
        print(f"{category}: {materials}")
