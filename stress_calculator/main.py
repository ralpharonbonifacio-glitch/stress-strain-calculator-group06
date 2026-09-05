"""
Main program for the Stress and Strain Calculator.

This module connects the material, database, tests,
properties, and utility modules.
"""

try:
    from .material import material_management
    from .database import (
        load_materials,
        save_materials,
        get_material_names,
        get_material
    )
    from .tests import StressStrainTest, TestCollection
except ImportError:
    from material import material_management
    from database import (
        load_materials,
        save_materials,
        get_material_names,
        get_material
    )
    from tests import StressStrainTest, TestCollection


def get_number(prompt: str, minimum: float = 0) -> float:
    """Get a valid number from the user."""

    while True:
        try:
            value = float(input(prompt))

            if value < minimum:
                print(f"Error: Value must be at least {minimum}.")
                continue

            return value

        except ValueError:
            print("Error: Please enter a valid number.")


def select_material():
    """Allow the user to select a material from the database."""

    material_names = get_material_names()

    print("\n=== SELECT MATERIAL ===")

    for index, name in enumerate(material_names, start=1):
        print(f"{index}. {name}")

    print(f"{len(material_names) + 1}. Custom Material")

    while True:
        choice = input(
            f"Select a material (1-{len(material_names) + 1}): "
        ).strip()

        try:
            choice_number = int(choice)

            if 1 <= choice_number <= len(material_names):
                return get_material(material_names[choice_number - 1])

            if choice_number == len(material_names) + 1:
                return material_management()

            print("Error: Invalid selection.")

        except ValueError:
            print("Error: Please enter a valid number.")

def perform_calculation(collection: TestCollection) -> None:
    """Perform one stress-strain calculation."""

    material = select_material()

    print("\n=== ENTER TEST DATA ===")

    force = get_number(
        "Enter force (N): ",
        minimum=0
    )

    area = get_number(
        "Enter cross-sectional area (m^2): ",
        minimum=0.0000000001
    )

    original_length = get_number(
        "Enter original length (m): ",
        minimum=0.0000000001
    )

    change_in_length = get_number(
        "Enter change in length (m): ",
        minimum=-float("inf")
    )

    try:
        test = StressStrainTest(
            material=material,
            force=force,
            area=area,
            original_length=original_length,
            change_in_length=change_in_length
        )

        collection.add_test(test)

        test.display_results()

    except ValueError as error:
        print(f"Error: {error}")


def run_random_test(collection: TestCollection) -> None:
    """Generate and run a random stress-strain test."""

    material = select_material()

    try:
        test = StressStrainTest.generate_random_test(material)

        collection.add_test(test)

        print("\n=== RANDOM TEST GENERATED ===")
        test.display_results()

    except ValueError as error:
        print(f"Error: {error}")
