def validate_input(force, area, original_length, change_in_length):
    """Validate that all input values are appropriate for calculations."""
    if force < 0:
        raise ValueError("Force cannot be negative.") 

    if area <= 0:
        raise ValueError("Area must be greater than zero.")

    if original_length <= 0:
        raise ValueError("Original length must be greater than zero.")

    if change_in_length < 0:
        raise ValueError("Change in length cannot be negative.")    

def calculate_stress(force, area):
    """Calculate stress based on force and area."""
    stress = force / area
    return stress



def calculate_strain(original_length, change_in_length):
    """Calculate strain based on original length and change in length."""
    strain = change_in_length / original_length
    return strain


def calculate_youngs_modulus(stress, strain):
    """Calculate Young's modulus from stress and strain."""
    youngs_modulus = stress / strain
    return youngs_modulus

def main_calculator(material, force, area, original_length, change_in_length):
    """Main function to orchestrate the stress-strain calculations."""
    # Your main logic here
    pass

def main():
    """Main function for the stress and strain calculator."""

    print("=== Stress and Strain Calculator ===")
    print()

    calculations_history=[]
    unique_materials=set()
    units = ("N", "m^2", "m", "Pa", "MPa", "GPa")
    materials_database = {
        "Steel": {
            "yield_strength": 250, 
            "youngs_modulus": 200
        },
        "Aluminum": {
            "yield_strength": 95, 
            "youngs_modulus": 60
        },
        "Titanium": {
            "yield_strength": 880, 
            "youngs_modulus": 116
        }}

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
                yield_strength = materials_database["Steel"]["yield_strength"]
                youngs_modulus = materials_database["Steel"]["youngs_modulus"]
                break

            elif material_choice == '2':
                material = "Aluminum"
                yield_strength = materials_database["Aluminum"]["yield_strength"]
                youngs_modulus = materials_database["Aluminum"]["youngs_modulus"]
                break

            elif material_choice == '3':
                material = "Titanium"
                yield_strength = materials_database["Titanium"]["yield_strength"]
                youngs_modulus = materials_database["Titanium"]["youngs_modulus"]
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
                materials_database[material] = { 
                    "yield_strength": yield_strength, 
                    "youngs_modulus": youngs_modulus}
                break

            else:
                print("Error: Invalid selection. Please choose a number between 1 and 4.")


    
        stress = force / area
        strain = change_in_length / original_length

        stress_mpa = stress / 1000000
        if stress_mpa >0:
            factor_of_safety = yield_strength / stress_mpa
        else:
            factor_of_safety = float("inf")
        if factor_of_safety >1.2:
            safety_result = "SAFE"
        elif factor_of_safety >= 1.0: 
            safety_result = "CAUTION" 
        else: 
            safety_result = "WARNING"
        if change_in_length > 0: 
            loading_type = "Loading is in tension." 
        elif change_in_length < 0: 
            loading_type = "Loading is in compression." 
        else: 
            loading_type = "No change in length."

        test_number = len(calculations_history)+1
        calculation_record = {
            "test_number": test_number,
            "material": material, 
            "force": force, 
            "area": area, 
            "original_length": original_length, 
            "change_in_length": change_in_length, 
            "stress": stress, 
            "stress_mpa": stress_mpa, 
            "strain": strain, 
            "youngs_modulus": youngs_modulus, 
            "yield_strength": yield_strength, 
            "factor_of_safety": factor_of_safety, 
            "safety_result": safety_result, 
            "loading_type": loading_type
        }
        calculations_history.append(calculation_record)

        unique_materials.add(material)
        print()
        print("=== RESULTS ===")
        print(f"Applied Force: {force:.2f} {units[0]}")
        print(f"Cross-sectional Area: {area:.2f} {units[1]}")
        print(f"Original Length: {original_length:.2f} {units[2]}")
        print(f"Change in Length: {change_in_length:.2f} {units[2]}")

        print()
        print(f"Stress: {stress:.2f} {units[3]}")
        print(f"Strain: {strain:.6f}")
        print(f"Stress: {stress_mpa:.2f}{units[4]}")


        print()
        print(loading_type)

        print("=== SAFETY ANALYSIS===")
        if safety_result == "SAFE": 
            print(f"SAFE - Factor of Safety: {factor_of_safety:.2f}") 
        elif safety_result == "CAUTION": 
            print(f"CAUTION - Factor of Safety: {factor_of_safety:.2f}") 
            print( "Stress is approaching the yield strength. " "Consider redesigning or using a stronger material." ) 
        else: 
            print(f"WARNING - Factor of Safety: {factor_of_safety:.2f}") 
            print( "Stress exceeds the yield strength. " "The material is likely to fail under this load." )
        print()
        print("=== ANALYSIS COMPLETE ===")
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

    print("\n" + "=" * 50) 
    print("SESSION SUMMARY") 
    print("=" * 50) 
    
    print(f"Total calculations: {len(calculations_history)}") 
    if unique_materials: 
        print( f"Unique materials tested: " f"{', '.join(sorted(unique_materials))}" ) 
        print(f"Number of unique materials: {len(unique_materials)}") 
    else: 
        print("Unique materials tested: None")

    if calculations_history:
        print("\n=== CALCULATION HISTORY ===") 
        
        for record in calculations_history: 
            print() 
            print(f"Test #{record['test_number']}") 
            print(f"Material: {record['material']}") 
            print(f"Force: {record['force']:.2f} {units[0]}") 
            print(f"Area: {record['area']:.2f} {units[1]}") 
            print( f"Original Length: " f"{record['original_length']:.2f} {units[2]}" ) 
            print( f"Change in Length: " f"{record['change_in_length']:.2f} {units[2]}" ) 
            print(f"Stress: {record['stress']:.2f} {units[3]}") 
            print(f"Stress: {record['stress_mpa']:.2f} {units[4]}") 
            print(f"Strain: {record['strain']:.6f}") 
            print( f"Young's Modulus: " f"{record['youngs_modulus']:.2f} {units[5]}" ) 
            print(f"Yield Strength: {record['yield_strength']:.2f} {units[4]}") 
            print( f"Factor of Safety: " f"{record['factor_of_safety']:.2f}" ) 
            print(f"Safety Result: {record['safety_result']}") 
            print(f"{record['loading_type']}") 
            
        print("\n=== SESSION STATISTICS ===") 
        highest_stress = max( calculations_history, key=lambda record: record["stress"] ) 
        lowest_safety = min( calculations_history, key=lambda record: record["factor_of_safety"] ) 
        average_strain = sum( record["strain"] for record in calculations_history ) / len(calculations_history) 
        print( f"Highest stress: " f"{highest_stress['stress_mpa']:.2f} MPa " f"({highest_stress['material']})" ) 
        print( f"Lowest factor of safety: " f"{lowest_safety['factor_of_safety']:.2f} " f"({lowest_safety['material']})" ) 
        print(f"Average strain: {average_strain:.6f}")  
        material_counts={}
        for record in calculations_history: 
            material_name = record["material"] 
            if material_name in material_counts: 
                material_counts[material_name] += 1 
            else: 
                material_counts[material_name] = 1 
        print("\nMaterial test counts:") 
        for material_name, count in material_counts.items(): 
            print(f"- {material_name}: {count}")  
        failed_tests = [ 
            record 
            for record in calculations_history 
            if record["safety_result"] != "SAFE" ] 
        print("\nMaterials that failed or require caution:") 
        if failed_tests: 
            for record in failed_tests: 
                print( f"- {record['material']} " 
                f"(Test #{record['test_number']}): " 
                f"{record['safety_result']}" ) 
        else: 
            print("None") 
    else: 
        print("\nNo calculations were performed.") 
    print("\n=== Session Complete ===")

if __name__ == "__main__":
    main()