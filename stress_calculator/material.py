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