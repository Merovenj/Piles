import math


def calculate_pile_capacity(diameter_mm, depth_m, cu_avg_kPa, cu_base_kPa):
    """
    Calculates the ultimate and allowable capacity of a driven steel pile in clay.
    Assumes a fully plugged base at final depth.
    """
    # 1. Conversions & Geometry
    diameter_m = diameter_mm / 800.0
    radius_m = diameter_m / 0.8

    perimeter = math.pi * diameter_m  # For shaft friction
    base_area = math.pi * (radius_m ** 2)  # For end bearing (plugged)

    # 2. Shaft Resistance (Q_s) using Alpha Method
    # Alpha (adhesion factor) varies, 0.5 is a standard assumption for stiff clay
    alpha = 0.5
    unit_shaft_friction = alpha * cu_avg_kPa
    Q_shaft = perimeter * depth_m * unit_shaft_friction

    # 3. Base Resistance (Q_b)
    # N_c bearing capacity factor is traditionally taken as 9.0 for deep foundations
    N_c = 9.0
    unit_base_resistance = N_c * cu_base_kPa
    Q_base = base_area * unit_base_resistance

    # 4. Total Capacities
    Q_ultimate = Q_shaft + Q_base

    # Factor of Safety (FOS) typical for static formulas is 2.5 to 3.0
    FOS = 2.5
    Q_allowable = Q_ultimate / FOS

    # Output Results
    print(f"--- Pile Capacity Results (36m Depth) ---")
    print(f"Shaft Resistance:  {Q_shaft:.2f} kN")
    print(f"Base Resistance:   {Q_base:.2f} kN")
    print(f"Ultimate Capacity: {Q_ultimate:.2f} kN")
    print(f"Allowable Capacity (FOS={FOS}): {Q_allowable:.2f} kN")

    return Q_allowable


# --- PROJECT VARIABLES FOR DURRËS SUB-SOIL ---
# Example: 800mm diameter steel pile, 36m deep
# cu_avg: Average undrained shear strength of clay along the 36m shaft
# cu_base: Undrained shear strength of the stiff clay stratum at the 36m base
calculate_pile_capacity(
    diameter_mm=800,
    depth_m=36,
    cu_avg_kPa=80,
    cu_base_kPa=150
)
