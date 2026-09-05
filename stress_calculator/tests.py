class StressStrainTest:
    """A single stress-strain test."""
    def __init__(
        self,
        material: Material,
        force: float,
        area: float,
        original_length: float,
        change_in_length: float,
    ):
        self.material = material
        self._force = force
        self._area = area
        self._original_length = original_length
        self._change_in_length = change_in_length

        if force < 0:
            raise ValueError("Force cannot be negative")
        if area <= 0:
            raise ValueError("Area must be positive")
        if original_length <= 0:
            raise ValueError("Original length must be positive")

    @property
    def stress(self) -> float:
        """Calculate stress in Pa."""
        return self._force / self._area

    @property
    def stress_mpa(self) -> float:
        """Convert stress from Pascals to Megapascals."""
        return self.stress / 1_000_000  

    @property
    def strain(self) -> float:
        """Calculate strain (dimensionless)."""
        return self._change_in_length / self._original_length

    @property
    def youngs_modulus(self) -> float:
        """Calculate actual Young's modulus in GPa based on the test parameters."""
        if self.strain == 0:
            return float("inf")
        # Stress in Pa / Strain / 1e9 to get GPa
        return (self.stress / self.strain) / 1_000_000_000

    @property
    def factor_of_safety(self) -> float:
        """Calculate Factor of Safety (Yield Strength / Stress)."""
        if self.stress_mpa > 0:
            return self.material.properties.yield_strength / self.stress_mpa
        return float("inf")

    @property
    def safety_result(self) -> str:
        """Return safety evaluation label based on safety factor."""
        fos = self.factor_of_safety
        if fos > 1.2:
            return "SAFE"
        elif fos >= 1.0:
            return "CAUTION"
        else:
            return "WARNING"

    @property
    def loading_type(self) -> str:
        """Determine if load is tension, compression, or static."""
        if self._change_in_length > 0:
            return "Loading is in tension."
        elif self._change_in_length < 0:
            return "Loading is in compression."
        else:
            return "No change in length."

    def will_fail(self) -> bool:
        """Determine if the material is likely to fail under this test."""
        return not self.material.can_withstand_stress(self.stress_mpa)

