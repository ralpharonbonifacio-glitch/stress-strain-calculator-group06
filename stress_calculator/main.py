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

def show_history(collection: TestCollection) -> None:
    """Display the test history."""

    collection.display_history()


def show_summary(collection: TestCollection) -> None:
    """Display the complete session summary."""

    collection.display_session_summary()

def save_results(collection: TestCollection) -> None:
    """Save test results to JSON and CSV files."""

    if len(collection) == 0:
        print("\nNo test results to save.")
        return

    collection.save_json("test_history.json")
    collection.export_csv("test_history.csv")

def load_results(collection: TestCollection) -> None:
    """Load saved test results from a JSON file."""

    try:
        collection.load_json("test_history.json")
        print("\nTest results loaded successfully.")

    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Error loading test results: {error}")

def main() -> None:
    """Run the main Stress and Strain Calculator."""

    print("=" * 50)
    print("     STRESS AND STRAIN CALCULATOR")
    print("=" * 50)

    try:
        load_materials()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Warning: Could not load materials: {error}")

    collection = TestCollection()

    while True:
        print("\n=== MAIN MENU ===")
        print("1. Perform Stress-Strain Calculation")
        print("2. Generate Random Test")
        print("3. View Test History")
        print("4. View Session Summary")
        print("5. Save Results")
        print("6. Load Results")
        print("7. Save Material Database")
        print("8. Exit")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            perform_calculation(collection)

        elif choice == "2":
            run_random_test(collection)

        elif choice == "3":
            show_history(collection)

        elif choice == "4":
            show_summary(collection)

        elif choice == "5":
            save_results(collection)

        elif choice == "6":
            load_results(collection)

        elif choice == "7":
            try:
                save_materials()
                print("Material database saved successfully.")
            except OSError as error:
                print(f"Error saving material database: {error}")

        elif choice == "8":
            print("\nThank you for using the Stress and Strain Calculator!")
            break

        else:
            print("Error: Please choose a number from 1 to 8.")

if __name__ == "__main__":
    main()
   