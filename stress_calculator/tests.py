from datetime import datetime
from pathlib import Path
import json
import random
import csv

try:
    from .material import Material
    from .database import get_material
    from .utils import (calculate_stress, convert_stress_to_mpa,
                    calculate_strain, calculate_youngs_modulus,
                    calculate_factor_of_safety, determine_safety_result, 
                    determine_loading_type)  
except ImportError:
    from material import Material
    from .database import get_material
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
            print(f"Timestamp: {test.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Material: {test.material.name}")
            print(f"Force: {test._force:.2f} {units[0]}")
            print(f"Area: {test._area:.2f} {units[1]}")
            print(f"Original Length: {test._original_length:.2f} {units[2]}")
            print(f"Change in Length: {test._change_in_length:.2f} {units[2]}")
            print(f"Stress: {test.stress:.2f} {units[3]}")
            print(f"Stress in MPa: {test.stress_mpa:.2f} {units[4]}")
            print(f"Strain: {test.strain:.6f}")

            modulus = (
                test.material.properties.typical_youngs_modulus
                if test.strain == 0
                else test.youngs_modulus
            )
            print(f"Young's Modulus: {modulus:.2f} {units[5]}")
            print(
                f"Yield Strength: {test.material.properties.yield_strength:.2f} {units[4]}"
            )
            print(f"Factor of Safety: {test.factor_of_safety:.2f}")
            print(f"Safety Result: {test.safety_result}")
            print(f"{test.loading_type}")

        print("\n=== SESSION STATISTICS ===")
        highest_stress_test = max(calculations_history, key=lambda t: t.stress)
        highest_stress_test_in_mpa = max(
            calculations_history, key=lambda t: t.stress_mpa
        )
        lowest_safety_test = min(
            calculations_history, key=lambda t: t.factor_of_safety
        )
        average_strain = sum(t.strain for t in calculations_history) / len(
            calculations_history
        )

        print(
            f"Highest stress: {highest_stress_test.stress:.2f} Pa ({highest_stress_test.material.name})"
        )
        print(
            f"Highest stress in MPa: {highest_stress_test_in_mpa.stress_mpa:.2f} MPa ({highest_stress_test_in_mpa.material.name})"
        )
        print(
            f"Lowest factor of safety: {lowest_safety_test.factor_of_safety:.2f} ({lowest_safety_test.material.name})"
        )
        print(f"Average strain: {average_strain:.6f}")

        material_counts = {}
        for test in calculations_history:
            mat = test.material.name
            material_counts[mat] = material_counts.get(mat, 0) + 1

        print("\nMaterial test counts:")
        for mat, count in material_counts.items():
            print(f"- {mat}: {count}")

        failed_tests = [
            (i, t)
            for i, t in enumerate(calculations_history, 1)
            if t.safety_result != "SAFE"
        ]

        print("\nMaterials that failed or require caution:")
        if failed_tests:
            for i, test in failed_tests:
                print(f"- {test.material.name} (Test #{i}): {test.safety_result}")
        else:
            print("None")
    else:
        print("\nNo calculations were performed.")

    print("\n=== Session Complete ===")

class TestCollection:
    """Manage a collection of stress-strain tests."""

    def __init__(self):
        self._tests = []

    def add_test(self, test):
        """Add a test to the collection."""
        self._tests.append(test)

    def get_tests(self):
        """Return all tests."""
        return self._tests.copy()

    def get_test(self, index):
        """Return a specific test."""
        if index < 0 or index >= len(self._tests):
            raise IndexError("Test index out of range.")
        return self._tests[index]

    def clear(self):
        """Remove all tests."""
        self._tests.clear()

    def __len__(self):
        """Return the number of tests."""
        return len(self._tests)

    def display_history(self):
        """Display all tests in the collection."""
        print("\n=== TEST HISTORY ===")
        if not self._tests:
            print("No tests have been performed.")
            return

        for index, test in enumerate(self._tests, start=1):
            print(f"\nTest #{index}")
            print(f"Timestamp: {test.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Material: {test.material.name}")
            print(f"Stress: {test.stress_mpa:.2f} MPa")
            print(f"Strain: {test.strain:.6f}")
            print(f"Factor of Safety: {test.factor_of_safety:.2f}")
            print(f"Result: {test.safety_result}")

    def unique_materials(self):
        """Return unique material names."""
        return {test.material.name for test in self._tests}

    def material_counts(self):
        """Count how many tests use each material."""
        counts = {}
        for test in self._tests:
            material_name = test.material.name
            counts[material_name] = counts.get(material_name, 0) + 1
        return counts

    def failed_tests(self):
        """Return tests that are likely to fail."""
        return [test for test in self._tests if test.will_fail]

    def caution_tests(self):
        """Return tests with CAUTION result."""
        return [test for test in self._tests if test.safety_result == "CAUTION"]

    def average_strain(self):
        """Calculate the average strain."""
        if not self._tests:
            return 0.0
        return sum(test.strain for test in self._tests) / len(self._tests)

    def maximum_stress(self):
        """Return the maximum stress in MPa."""
        if not self._tests:
            return 0.0
        return max(test.stress_mpa for test in self._tests)

    def minimum_factor_of_safety(self):
        """Return the lowest Factor of Safety."""
        if not self._tests:
            return float("inf")
        return min(test.factor_of_safety for test in self._tests)

    def display_session_summary(self):
        """Display a summary using the collection's tests."""
        display_session_summary(self._tests)

    def save_json (self, filename="test_history.json"):
        """Save test history to a JSON file."""
        path = Path(filename)
        data = [test.to_dict() for test in self._tests]

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Test history saved to: {path}")

    def load_json(self, filename="test_history.json"):
        """Load test history from a JSON file."""

        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self._tests.clear()

        for record in data:
            material = get_material(record["material"])

            test = StressStrainTest(
                material=material,
                force=record["force"],
                area=record["area"],
                original_length=record["original_length"],
                change_in_length=record["change_in_length"]
            )

            self._tests.append(test)

        print(f"Loaded {len(self._tests)} test records.")

    def export_csv(self, filename="test_history.csv"):
        """Export test history to a CSV file."""
        path = Path(filename)
        if not self._tests:
            print("No test data available to export.")
            return

        data = [test.to_dict() for test in self._tests]
        fieldnames = list(data[0].keys())

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"Test data exported to: {path}")
