from dataclasses import dataclass
@dataclass
class MaterialProperties:
    """ Store the physical properties of a material."""

    density: float
    yield_strength: float
    typical_youngs_modulus: float

    def __post_init__(self):
        """Validate material properties"""

        if self.density <= 0:
            raise ValueError("Density must be positive")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be positive")
        if self.typical_youngs_modulus <= 0:
            raise ValueError("Young's modulus must be positive")