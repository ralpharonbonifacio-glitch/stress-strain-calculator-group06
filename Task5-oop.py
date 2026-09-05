from dataclasses import dataclass
from typing import List

@dataclass
class MaterialProperties:
    """Properties of a material."""
    density: float # kg/m^3
    yield_stength = float #MPa
    typical_youngs_modulus: float #GPa

    def __post_init__(self):
        """Validate properties."""
        if self.density <- 0:
            raise ValueError("Density must be positive")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be positive")
        if self.typical_youngs_modulus <= 0:
            raise ValueError("Young's modulus must be positive")

class Material:
    """Base class for all materials."""
    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    def __str__(self) -> str:
        return f"{self.name} (Yield Strength: {self.properties.yield_strength} MPa)"

    def can_withstand_stress(self, stress_mpa: float) -> bool:
        """Check if the material can withstand the given stress."""
        return stress_mpa < self.properties.yield_strength

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

        # Validate inputs based on user constraints
        if force < 0:
            raise ValueError("Force cannot be negative")
        if area <= 0:
            raise ValueError("Area must be positive")
        if original_length <= 0:
            raise ValueError("Original length must be positive")
        # Change in length can be negative (compression)

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
    
def calculate_stress(force, area):
    """Calculate stress (Force / Area)."""  
    return force / area

def calculate_strain(original_length, change_in_length):
    """Calculate strain (ΔL / L)."""
    return change_in_length / original_length

def calculate_youngs_modulus(stress, strain):
    """Calculate Young's Modulus (Stress / Strain)."""
    if strain == 0:
        return float("inf") 
    return stress / strain

def calculate_stress_mpa(stress):
    """Convert stress from Pascals to Megapascals."""
    return stress / 1000000

def calculate_factor_of_safety(yield_strength, stress_mpa):
    """Calculate Factor of Safety (Yield Strength / Stress)."""
    if stress_mpa > 0:
        factor_of_safety = yield_strength / stress_mpa
    else:
        factor_of_safety = float("inf")

    return factor_of_safety

def safety_result(factor_of_safety):
    """Return safety evaluation label based on safety factor."""
    if factor_of_safety > 1.2:
        safety_result = "SAFE"
    elif factor_of_safety >= 1.0:
        safety_result = "CAUTION"
    else:
        safety_result = "WARNING"

    return safety_result

def loading_type(change_in_length):
    """Determine if load is tension, compression, or static."""
    if change_in_length > 0: 
        return "Loading is in tension." 
    elif change_in_length < 0: 
        return "Loading is in compression." 
    else: 
        return "No change in length."

def material_management() -> Material:
    """Prompt user to select a preset or custom material."""
    presets = {
        "Steel": Material("Steel", MaterialProperties(density=7850, yield_strength=250, typical_youngs_modulus=200)),
        "Aluminum": Material("Aluminum", MaterialProperties(density=2700, yield_strength=95, typical_youngs_modulus=69)),
        "Titanium": Material("Titanium", MaterialProperties(density=4500, yield_strength=880, typical_youngs_modulus=114))
    }
    
    while True:
        print("\n===Material Properties===")
        print("1. Steel")
        print("2. Aluminum")
        print("3. Titanium")
        print("4. Custom Material")

        material_choice = input("Select a material (1-4): ")

        if material_choice == '1':
            return presets["Steel"]
        elif material_choice == '2':
            return presets["Aluminum"]
        elif material_choice == '3':
            return presets["Titanium"]
        elif material_choice == '4':
            name = input("Enter custom material name: ").strip()
            
            while True:
                try:
                    yield_strength = float(input("Enter yield strength (MPa): "))
                    if yield_strength <= 0:
                        print("Error: Yield strength must be greater than zero.")
                    else:
                        break
                except ValueError:
                    print("Error: Please enter a valid number for yield strength.")
            
            while True:
                try:
                    modulus = float(input("Enter expected Young's modulus (GPa): "))
                    if modulus <= 0:
                        print("Error: Young's modulus must be greater than zero.")
                    else:
                        break
                except ValueError:
                    print("Error: Please enter a valid number for Young's modulus.")
            
            # Density is required by the base class, using 1.0 as a placeholder if not asking the user for it
            custom_props = MaterialProperties(density=1.0, yield_strength=yield_strength, typical_youngs_modulus=modulus)
            return Material(name, custom_props)
        else:
            print("Error: Invalid selection. Please choose a number between 1 and 4.")

def validate_input() -> tuple[float, float, float, float, Material]:
    """Prompt user and validate numeric inputs for the test."""
    while True:
        try:
            force = float(input("Enter applied force (N): "))
            if force < 0:
                print("Error: Force cannot be negative.")
            else:
                break
        except ValueError:
            print("Error: Please enter a valid number for force.")

    while True:
        try:
            area = float(input("Enter cross-sectional area (m^2): "))
            if area <= 0:
                print("Error: Area must be greater than zero.")
            else:
                break
        except ValueError:
            print("Error: Please enter a valid number for area.")

    while True:
        try:
            original_length = float(input("Enter original length (m): "))
            if original_length <= 0:
                print("Error: Original length must be greater than zero.")
            else:
                break
        except ValueError:
            print("Error: Please enter a valid number for original length.")

    while True:
        try:
            change_in_length = float(input("Enter change in length (m): "))
            break
        except ValueError:
            print("Error: Please enter a valid number for change in length.")

    material = material_management()
    return force, area, original_length, change_in_length, material

def display_session_summary(calculations_history: List[StressStrainTest]):
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
            print(f"Stress: {test.stress_mpa:.2f} {units[4]}")
            print(f"Strain: {test.strain:.6f}")
            
            modulus = test.material.properties.typical_youngs_modulus if test.strain == 0 else test.youngs_modulus
            print(f"Young's Modulus: {modulus:.2f} {units[5]}")
            print(f"Yield Strength: {test.material.properties.yield_strength:.2f} {units[4]}")
            print(f"Factor of Safety: {test.factor_of_safety:.2f}")
            print(f"Safety Result: {test.safety_result}")
            print(f"{test.loading_type}")

        print("\n=== SESSION STATISTICS ===")
        highest_stress_test = max(calculations_history, key=lambda t: t.stress_mpa)
        lowest_safety_test = min(calculations_history, key=lambda t: t.factor_of_safety)
        average_strain = sum(t.strain for t in calculations_history) / len(calculations_history)

        print(f"Highest stress: {highest_stress_test.stress_mpa:.2f} MPa ({highest_stress_test.material.name})")
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

def display_results(test: StressStrainTest):
    """Print formatted calculation results to the console."""

    units = ("N", "m^2", "m", "Pa", "MPa", "GPa")

    print("\n=== RESULTS ===")
    print(f"Stress: {test.stress:.2f} {units[3]}")
    print(f"Strain: {test.strain:.6f}")
    print(f"Stress: {test.stress_mpa:.2f} {units[4]}")

    display_modulus = test.material.properties.typical_youngs_modulus if test.strain == 0 else test.youngs_modulus
    print(f"Young's Modulus: {display_modulus:.2f} {units[5]}")
    print()
    print(f"\n{test.loading_type}")

    print("=== SAFETY ANALYSIS===")
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
        
    print("=== ANALYSIS COMPLETE ===")

def main():
    """Main function for the stress and strain calculator."""

    print("=== Stress and Strain Calculator ===")
    print()

    calculations_history = []
    unique_materials = set()
    units = ("N", "m^2", "m", "Pa", "MPa", "GPa")

    while True:

        force, area, original_length, change_in_length, material, yield_strength, preset_modulus = validate_input()
        stress = calculate_stress(force, area)
        strain = calculate_strain(original_length, change_in_length)
        stress_mpa = calculate_stress_mpa(stress)
        if preset_modulus is None:
            youngs_modulus_pa = calculate_youngs_modulus(stress, strain)
            youngs_modulus = youngs_modulus_pa / 1e9 if youngs_modulus_pa != float("inf") else float("inf")
        else:
            youngs_modulus = preset_modulus 
        factor_of_safety = calculate_factor_of_safety(yield_strength, stress_mpa)
        safety_val = safety_result(factor_of_safety)
        loading_val= loading_type(change_in_length)

        record_calculation(
                calculations_history,
                material=material,
                force=force,
                area=area,
                original_length=original_length,
                change_in_length=change_in_length,
                stress=stress,
                stress_mpa=stress_mpa,
                strain=strain,
                youngs_modulus=youngs_modulus,
                yield_strength=yield_strength,
                factor_of_safety=factor_of_safety,
                safety_val=safety_val,
                loading_val=loading_val,
        )
        unique_materials.add(material)

        display_results(stress, strain, youngs_modulus, units, stress_mpa, factor_of_safety, safety_val, loading_val)


        while True:
            repeat = input("Would you like to perform another calculation? (y/n): ").strip().lower()
            if repeat =="y":
                print("\nStarting a new calculation...\n")
                break
            elif repeat == "n": 
                break 
            else: 
                print("Error: Please enter 'y' for yes or 'n' for no.")
        if repeat == "n":

            break

    record_calculation(calculations_history, unique_materials=unique_materials, units=units, summary=True)


if __name__ == "__main__":
    main()