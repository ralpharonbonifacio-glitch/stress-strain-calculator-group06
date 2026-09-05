"""
Material classes for the Stress and Strain Calculator.

This module contains the base Material class and
specialized material classes.
"""

try:
    from .properties import MaterialProperties
except ImportError:
    from properties import MaterialProperties

class Material:
    """Base class for all materials."""

    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    def __str__(self) -> str:
        return (
            f"{self.name} "
            f"(Yield Strength: {self.properties.yield_strength} MPa)"
        )

    def can_withstand_stress(self, stress_mpa: float) -> bool:
        """Check if the material can withstand the given stress."""
        return stress_mpa < self.properties.yield_strength

class Metal(Material):
    """Material class for metal materials."""

    def __str__(self) -> str:
        return (
            f"{self.name} - Metal "
            f"(Yield Strength: "
            f"{self.properties.yield_strength} MPa)"
        )

class Plastic(Material):
    """Material class for plastic materials."""

    def __str__(self) -> str:
        return (
            f"{self.name} - Plastic "
            f"(Yield Strength: "
            f"{self.properties.yield_strength} MPa)"
        )

class Composite(Material):
    """Material class for composite materials."""

    def __str__(self) -> str:
        return (
            f"{self.name} - Composite "
            f"(Yield Strength: "
            f"{self.properties.yield_strength} MPa)"
        )

def create_steel() -> Material:
    """Create a standard steel material."""

    properties = MaterialProperties(
        density=7850,
        yield_strength=250,
        typical_youngs_modulus=200
    )

    return Metal(
        name="Steel",
        properties=properties
    )

def create_aluminum() -> Material:
    """Create a standard aluminum material."""

    properties = MaterialProperties(
        density=2700,
        yield_strength=95,
        typical_youngs_modulus=70
    )

    return Metal(
        name="Aluminum",
        properties=properties
    )

def create_titanium() -> Material:
    """Create a standard titanium material."""

    properties = MaterialProperties(
        density=4500,
        yield_strength=880,
        typical_youngs_modulus=114
    )

    return Metal(
        name="Titanium",
        properties=properties
    )


def create_custom_material(
    name: str,
    yield_strength: float,
    youngs_modulus: float,
    density: float = 1.0
) -> Material:
    """
    Create a custom material.

    Density defaults to 1.0 because the original Task 5
    program did not ask the user for density.
    """

    properties = MaterialProperties(
        density=density,
        yield_strength=yield_strength,
        typical_youngs_modulus=youngs_modulus
    )

    return Material(
        name=name,
        properties=properties
    )

def material_management() -> Material:
    """Prompt the user to select a preset or custom material."""

    presets = {
        "1": create_steel(),
        "2": create_aluminum(),
        "3": create_titanium()
    }

    while True:
        print("\n=== Material Properties ===")
        print("1. Steel")
        print("2. Aluminum")
        print("3. Titanium")
        print("4. Custom Material")

        material_choice = input("Select a material (1-4): ").strip()

        if material_choice in presets:
            return presets[material_choice]

        elif material_choice == "4":
            name = input("Enter custom material name: ").strip()

            while not name:
                print("Error: Material name cannot be empty.")
                name = input("Enter custom material name: ").strip()

            while True:
                try:
                    yield_strength = float(
                        input("Enter yield strength (MPa): ")
                    )

                    if yield_strength <= 0:
                        print(
                            "Error: Yield strength must be "
                            "greater than zero."
                        )
                    else:
                        break

                except ValueError:
                    print(
                        "Error: Please enter a valid number "
                        "for yield strength."
                    )

            while True:
                try:
                    modulus = float(
                        input("Enter expected Young's modulus (GPa): ")
                    )

                    if modulus <= 0:
                        print(
                            "Error: Young's modulus must be "
                            "greater than zero."
                        )
                    else:
                        break

                except ValueError:
                    print(
                        "Error: Please enter a valid number "
                        "for Young's modulus."
                    )

            return create_custom_material(
                name=name,
                yield_strength=yield_strength,
                youngs_modulus=modulus
            )

        else:
            print(
                "Error: Invalid selection. "
                "Please choose a number between 1 and 4."
            )

if __name__ == "__main__":
    print("=== Material Module Test ===")

    steel = create_steel()
    aluminum = create_aluminum()
    titanium = create_titanium()

    print(steel)
    print(aluminum)
    print(titanium)

    print("\nSteel properties:")
    print(f"Density: {steel.properties.density} kg/m^3")
    print(
        f"Yield Strength: "
        f"{steel.properties.yield_strength} MPa"
    )
    print(
        f"Young's Modulus: "
        f"{steel.properties.typical_youngs_modulus} GPa"
    )