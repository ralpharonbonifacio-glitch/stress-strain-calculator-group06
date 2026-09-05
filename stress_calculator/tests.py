from datetime import datetime
from pathlib import Path
import json
import random
import csv


from material import Material
from utils import (calculate_stress, convert_stress_to_mpa,
                   calculate_strain, calculate_youngs_modulus,
                   calculate_factor_of_safety, determine_safety_result, 
                   determine_loading_type)

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
        self._timestamp = datetime.now()

    @property
    def timestamp(self):
        """Return the date and time when the test was recorded."""
        return self._timestamp

    @property
    def force(self):
        """Return applied force in Newtons."""
        return self._force

    @property
    def area(self):
        """Return cross-sectional area in square meters."""
        return self._area

    @property
    def original_length(self):
        """Return original length in meters."""
        return self._original_length

    @property
    def change_in_length(self):
        """Return change in length in meters."""
        return self._change_in_length

    @property
    def stress(self):
        """Calculate stress in Pa."""
        return calculate_stress(self._force, self._area)

    @property
    def stress_mpa(self):
        """Convert stress from Pascals to Megapascals."""
        return convert_stress_to_mpa(self.stress)

    @property
    def strain(self):
        """Calculate strain (dimensionless)."""
        return calculate_strain(self._change_in_length, self._original_length)

    @property
    def youngs_modulus(self):
        """Calculate actual Young's modulus in GPa based on test parameters."""
        return calculate_youngs_modulus(self.stress, self.strain)

    @property
    def factor_of_safety(self):
        """Calculate Factor of Safety (Yield Strength / Stress)."""
        return calculate_factor_of_safety(
            self.material.properties.yield_strength, self.stress_mpa
        )

    @property
    def safety_result(self):
        """Return safety evaluation label based on safety factor."""
        return determine_safety_result(self.factor_of_safety)

    @property
    def loading_type(self):
        """Determine if load is tension, compression, or static."""
        return determine_loading_type(self._change_in_length)

    @property
    def will_fail(self):
        """Determine if the material is likely to fail under this test."""
        return not self.material.can_withstand_stress(self.stress_mpa)

    @classmethod
    def generate_random_test(cls, material):
        """Generate a randomized test instance for simulation and testing."""
        force = random.uniform(1000.0, 50000.0)
        area = random.uniform(0.0001, 0.005)
        original_length = random.uniform(0.1, 1.0)
        change_in_length = random.uniform(-0.005, 0.005)

        return cls(material, force, area, original_length, change_in_length)

    def display_results(self) -> None:
        """Print formatted calculation results to the console."""
        display_results(self)

    def to_dict(self) -> dict:
        """Return the test results as a dictionary."""
        modulus = self.material.properties.typical_youngs_modulus if self.strain == 0 else self.youngs_modulus
        return {
            "material": self.material.name,
            "force": self._force,
            "area": self._area,
            "original_length": self._original_length,
            "change_in_length": self._change_in_length,
            "stress": self.stress,
            "stress_mpa": self.stress_mpa,
            "strain": self.strain,
            "youngs_modulus": self.youngs_modulus,
            "factor_of_safety": self.factor_of_safety,
            "safety_result": self.safety_result,
            "loading_type": self.loading_type
        }

def display_results(test: StressStrainTest):
    """Print formatted calculation results to the console."""

    units = ("N", "m^2", "m", "Pa", "MPa", "GPa")

    print("\n=== RESULTS ===")
    print(f"Stress: {test.stress:.2f} {units[3]}")
    print(f"Stress in MPa: {test.stress_mpa:.2f} {units[4]}")
    print(f"Strain: {test.strain:.6f}")

    display_modulus = test.material.properties.typical_youngs_modulus if test.strain == 0 else test.youngs_modulus
    print(f"Young's Modulus: {display_modulus:.2f} {units[5]}")
    print()
    print(f"{test.loading_type}")

    print("\n=== SAFETY ANALYSIS===")
    if test.safety_result == "SAFE":
        print(f"SAFE - Factor of Safety: {test.factor_of_safety:.2f}")
    elif test.safety_result == "CAUTION":
        print(f"CAUTION - Factor of Safety: {test.factor_of_safety:.2f}")
        print(
            "Stress is approaching the yield strength. "
            "Consider redesigning or using a stronger material."
        )
    else:
        print(f"WARNING - Factor of Safety: {test.factor_of_safety:.2f}")
        print(
            "Stress exceeds the yield strength. "
            "The material is likely to fail under this load."
        )
        
    print("\n=== ANALYSIS COMPLETE ===")


def display_session_summary(calculations_history):
    """Print final session summary using the history of test objects."""
    units = ("N", "m^2", "m", "Pa", "MPa", "GPa")

    print("\n" + "=" * 50)
    print("SESSION SUMMARY")
    print("=" * 50)

    print(f"Total calculations: {len(calculations_history)}")

    unique_materials = {test.material.name for test in calculations_history}
    if unique_materials:
        print(f"Unique materials tested: {', '.join(sorted(unique_materials))}")
        print(f"Number of unique materials: {len(unique_materials)}")
    else:
        print("Unique materials tested: None")

    if calculations_history:
        print("\n=== CALCULATION HISTORY ===")
        for i, test in enumerate(calculations_history, 1):
            print(f"\nTest #{i}")
            print(f"Material: {test.material.name}")
            print(f"Force: {test._force:.2f} {units[0]}")
            print(f"Area: {test._area:.2f} {units[1]}")
            print(f"Original Length: {test._original_length:.2f} {units[2]}")
            print(f"Change in Length: {test._change_in_length:.2f} {units[2]}")
            print(f"Stress: {test.stress:.2f} {units[3]}")
            print(f"Stress in MPa: {test.stress_mpa:.2f} {units[4]}")
            print(f"Strain: {test.strain:.6f}")
            
            modulus = test.material.properties.typical_youngs_modulus if test.strain == 0 else test.youngs_modulus
            print(f"Young's Modulus: {modulus:.2f} {units[5]}")
            print(f"Yield Strength: {test.material.properties.yield_strength:.2f} {units[4]}")
            print(f"Factor of Safety: {test.factor_of_safety:.2f}")
            print(f"Safety Result: {test.safety_result}")
            print(f"{test.loading_type}")

        print("\n=== SESSION STATISTICS ===")
        highest_stress_test = max(calculations_history, key=lambda t: t.stress)
        highest_stress_test_in_mpa = max(calculations_history, key=lambda t: t.stress_mpa)
        lowest_safety_test = min(calculations_history, key=lambda t: t.factor_of_safety)
        average_strain = sum(t.strain for t in calculations_history) / len(calculations_history)

        print(f"Highest stress: {highest_stress_test.stress:.2f} Pa ({highest_stress_test.material.name})")
        print(f"Highest stress in MPa: {highest_stress_test.stress_mpa:.2f} MPa ({highest_stress_test_in_mpa.material.name})")
        print(f"Lowest factor of safety: {lowest_safety_test.factor_of_safety:.2f} ({lowest_safety_test.material.name})")
        print(f"Average strain: {average_strain:.6f}")

        material_counts = {}
        for test in calculations_history:
            mat = test.material.name
            material_counts[mat] = material_counts.get(mat, 0) + 1

        print("\nMaterial test counts:")
        for mat, count in material_counts.items():
            print(f"- {mat}: {count}")

        failed_tests = [(i, t) for i, t in enumerate(calculations_history, 1) if t.safety_result != "SAFE"]

        print("\nMaterials that failed or require caution:")
        if failed_tests:
            for i, test in failed_tests:
                print(f"- {test.material.name} (Test #{i}): {test.safety_result}")
        else:
            print("None")
    else:
        print("\nNo calculations were performed.")

    print("\n=== Session Complete ===")
