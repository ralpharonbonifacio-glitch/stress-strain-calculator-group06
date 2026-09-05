# Utility functions for the stress and strain calculator

def calculate_stress(force: float, area: float) -> float:

    return force / area

def convert_stress_to_mpa(stress_pa: float) -> float:

    return stress_pa / 1_000_000

def calculate_strain(change_in_length: float, original_length: float) -> float:

    return change_in_length / original_length

def calculate_youngs_modulus(stress_pa: float, strain: float) -> float:

    if strain == 0:
        return float("inf")
    return (stress_pa / strain) / 1_000_000_000
