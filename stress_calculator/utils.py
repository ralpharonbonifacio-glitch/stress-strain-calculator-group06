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

def calculate_factor_of_safety(yield_strength_mpa: float,stress_mpa: float) -> float:

    if stress_mpa > 0:
         return yield_strength_mpa / stress_mpa

    return float("inf")

def determine_safety_result(factor_of_safety: float) -> str:

    if factor_of_safety > 1.2:
        return "SAFE"
    elif factor_of_safety >= 1.0:
        return "CAUTION"
    else:
        return "WARNING"

def validate_force(force: float) -> None:

    if force < 0:
        raise ValueError("Force cannot be negative")

def validate_area(area: float) -> None:

    if area <= 0:
        raise ValueError("Area must be positive")

def validate_original_length(original_length: float) -> None:

    if original_length <= 0:
        raise ValueError("Original length must be positive")

def determine_loading_type(change_in_length: float) -> str:

    if change_in_length > 0:
        return "Loading is in tension."
    elif change_in_length < 0:
        return "Loading is in compression."
    else:
        return "No change in length."

def validate_change_in_length(change_in_length: float) -> None:
    return None