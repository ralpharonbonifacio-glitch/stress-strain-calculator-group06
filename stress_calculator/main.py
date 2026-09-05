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
