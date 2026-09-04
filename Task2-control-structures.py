# Part 1: Basic Stress and Strain Calculator Template

def main():
    """Main function for the stress and strain calculator."""

    print("=== Stress and Strain Calculator ===")
    print()


    while True:

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

        while True:
            print()
            print("===Material Properties===")
            print("1. Steel")
            print("2. Aluminum")
            print("3. Titanium")
            print("4. Custom Material")

            material_choice = input("Select a material (1-4): ")

            if material_choice == '1':
                material = "Steel"
                yield_strength = 250
                youngs_modulus = 200
                break

            elif material_choice == '2':
                material = "Aluminum"
                yield_strength = 95
                youngs_modulus = 69
                break

            elif material_choice == '3':
                material = "Titanium"
                yield_strength = 880
                youngs_modulus = 114
                break

            elif material_choice == '4':
                material = input("Enter custom material name: ").strip()

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
                        youngs_modulus = float(input("Enter Young's modulus (GPa): "))
                        if youngs_modulus <= 0:
                            print("Error: Young's modulus must be greater than zero.")
                        else:
                            break
                    except ValueError:
                        print("Error: Please enter a valid number for Young's modulus.")
                break

            else:
                print("Error: Invalid selection. Please choose a number between 1 and 4.")


    
        stress = force / area
        strain = change_in_length / original_length


        print()
        print("=== RESULTS ===")
        print(f"Applied Force: {force:.2f} N")
        print(f"Cross-sectional Area: {area:.2f} m^2")
        print(f"Original Length: {original_length:.2f} m")
        print(f"Change in Length: {change_in_length:.2f} m")

        print()
        print(f"Stress: {stress:.2f} Pa")
        print(f"Strain: {strain:.6f}")


        print()

        stress_mpa = stress / 1_000_000
        print(f"Stress: {stress_mpa:.2f} MPa")

        if stress_mpa > 0:
            factor_of_safety = yield_strength / stress_mpa
        else:
            factor_of_safety = float('inf')

        if change_in_length > 0:
            print("Loading is in tension.")
        elif change_in_length < 0:
            print("Loading is in compression.")
        else:
            print("No change in length.")

        print()
        print("=== SAFETY ANALYSIS ===")

        if factor_of_safety > 1.2:
            print(f"SAFE - Factor of Safety: {factor_of_safety:.2f}")

        elif factor_of_safety >= 1.0:
            print(f"CAUTION - Factor of Safety: {factor_of_safety:.2f}")
            print("Stress is approaching the yield strength. Consider redesigning or using a stronger material.")

        else:
            print(f"WARNING - Factor of Safety: {factor_of_safety:.2f}")
            print("Stress exceeds the yield strength. The material is likely to fail under this load.")

        print()
        print("=== Analysis Complete ===")

        while True:
            repeat = input("Would you like to perform another calculation? (y/n): ").strip().lower()
            if repeat == 'y':
                print("\nStarting a new calculation...\n")
                break
            elif repeat == 'n':
                print("Exiting the calculator. Goodbye!")
                return
            else:
                print("Error: Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()
