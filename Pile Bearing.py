import numpy as np
import matplotlib.pyplot as plt

# --- 1. INPUT PARAMETERS ---
depth_max = 25.0       # Maximum pile depth (meters)
diameter = 0.6         # Pile diameter (meters)
cu = 40.0              # Undrained shear strength of clay (kPa)
alpha = 0.55           # Adhesion factor for skin friction
gamma = 18.0           # Unit weight of soil (kN/m^3)
phi = 30.0             # Friction angle (degrees) for deep layers
Nc = 9.0               # Bearing capacity factor for deep clay

# --- 2. DERIVED GEOMETRY ---
area_tip = np.pi * (diameter / 2) ** 2
perimeter = np.pi * diameter

# --- 3. CALCULATIONS PROFILE ---
depths = np.linspace(0, depth_max, 100)

# Skin Friction Profile: Q_s = alpha * cu * Perimeter * Depth
q_s_profile = alpha * cu * perimeter * depths

# End Bearing Profile: Q_b = Nc * cu * Area_tip (simplified constant for clay)
# Note: In reality, tip resistance applies fully only when the tip reaches that depth
q_b_profile = np.full_like(depths, Nc * cu * area_tip)

# Total Ultimate Capacity
q_u_profile = q_s_profile + q_b_profile

# Allowable Capacity (Factor of Safety = 2.5)
fos = 2.5
q_a_profile = q_u_profile / fos

# Print final design values at the bottom tip
print(f"--- RESULTS AT DEPTH {depth_max}m ---")
print(f"Skin Friction (Qs): {q_s_profile[-1]:.2f} kN")
print(f"End Bearing (Qb):   {q_b_profile[-1]:.2f} kN")
print(f"Total Ultimate (Qu): {q_u_profile[-1]:.2f} kN")
print(f"Allowable Load (Qa): {q_a_profile[-1]:.2f} kN (FoS = {fos})")

# --- 4. VISUALIZATION ---
plt.figure(figsize=(7, 9))
plt.plot(q_s_profile, depths, 'g--', label='Skin Friction ($Q_s$)')
plt.plot(q_b_profile, depths, 'b--', label='End Bearing ($Q_b$)')
plt.plot(q_u_profile, depths, 'r-', linewidth=2.5, label='Total Ultimate ($Q_u$)')
plt.plot(q_a_profile, depths, 'k-', linewidth=2, label='Allowable Capacity ($Q_a$)')

plt.title('Pile Bearing Capacity vs. Depth Profile', fontsize=12, fontweight='bold')
plt.xlabel('Capacity (kN)', fontsize=10)
plt.ylabel('Depth below Ground Level (m)', fontsize=10)
plt.gca().invert_yaxis()  # Invert y-axis to simulate going underground
plt.grid(True, which='both', linestyle=':', alpha=0.5)
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()
