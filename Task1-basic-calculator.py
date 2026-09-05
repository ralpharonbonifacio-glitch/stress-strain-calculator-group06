# Part 1: Basic Stress and Strain Calculator Template

def main():
    """Main function for the stress and strain calculator."""

    print("=== Stress and Strain Calculator ===")
    print()

    force = float(input("Enter applied force (N): "))
    area = float(input("Enter cross-sectional area (m^2): "))
    original_length = float(input("Enter original length (m): "))
    change_in_length = float(input("Enter change in length (m): "))

    
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

    if change_in_length > 0:
        print("Loading is in tension.")
    elif change_in_length < 0:
        print("Loading is in compression.")
    else:
        print("No change in length.")

    print()
    print("=== Analysis Complete ===")

if __name__ == "__main__":
    main()
