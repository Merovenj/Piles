import numpy as np
import matplotlib.pyplot as plt

# --- 1. INPUT PARAMETERS (SILTY CLAY PROPERTY BIAS) ---
depth_max = 20.0       # Maximum pile depth (meters)
diameter = 0.5         # Pile diameter (meters)
gamma_bulk = 19.0      # Unit weight of silty clay (kN/m^3)
water_depth = 2.0      # Water table depth below surface (meters)

# Undrained parameters (Short-term)
cu = 35.0              # Undrained shear strength (kPa)
alpha = 0.65           # Adhesion factor for intermediate/silty clay
Nc = 9.0               # End bearing factor

# Drained parameters (Long-term)
phi_prime = 24.0       # Effective friction angle (degrees)
c_prime = 5.0          # Effective cohesion (kPa)
K_earth = 0.7          # Lateral earth pressure coefficient
delta = 20.0           # Pile-soil friction angle (degrees)

# --- 2. GEOMETRY & DERIVED VARIABLES ---
area_tip = np.pi * (diameter / 2) ** 2
perimeter = np.pi * diameter
gamma_water = 9.81

# --- 3. LAYER DEPTH ARRAY & EFFECTIVE STRESS ---
depths = np.linspace(0, depth_max, 100)

# Calculate Effective Overburden Pressure (sigma_v_prime)
sigma_v_prime = []
for z in depths:
    if z <= water_depth:
        stress = gamma_bulk * z
    else:
        stress = (gamma_bulk * water_depth) + ((gamma_bulk - gamma_water) * (z - water_depth))
    sigma_v_prime.append(stress)
sigma_v_prime = np.array(sigma_v_prime)

# --- 4. BEARING CAPACITY CALCULATIONS ---

# A. Short-Term / Undrained Profile
qs_undrained = alpha * cu * perimeter * depths
qb_undrained = np.full_like(depths, Nc * cu * area_tip)
qu_undrained = qs_undrained + qb_undrained

# B. Long-Term / Drained Profile (Beta Method Variation)
# Skin friction: f_s = c' + sigma_v_prime * K * tan(delta)
# Integrating over depth step-by-step
fs_drained = c_prime + (sigma_v_prime * K_earth * np.tan(np.radians(delta)))
qs_drained = np.zeros_like(depths)
for i in range(1, len(depths)):
    # Numerical integration of friction along shaft segments
    dz = depths[i] - depths[i-1]
    avg_fs = (fs_drained[i] + fs_drained[i-1]) / 2
    qs_drained[i] = qs_drained[i-1] + (avg_fs * perimeter * dz)

# Terzaghi/Meyerhof End Bearing for c-phi soils: q_b = c'Nc + sigma_v_prime*Nq
# Simplified Nq estimation for phi=24 degrees
Nq_drained = 10.0
Nc_drained = 20.0
qb_drained = (c_prime * Nc_drained + sigma_v_prime * Nq_drained) * area_tip
qu_drained = qs_drained + qb_drained

# --- 5. VISUALIZATION ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8), sharey=True)

# Plot Undrained (Short-Term)
ax1.plot(qs_undrained, depths, 'g--', label='Skin Friction ($Q_s$)')
ax1.plot(qb_undrained, depths, 'b--', label='End Bearing ($Q_b$)')
ax1.plot(qu_undrained, depths, 'r-', linewidth=2, label='Total Ultimate ($Q_u$)')
ax1.set_title('Undrained Capacity (Short-Term)')
ax1.set_xlabel('Capacity (kN)')
ax1.set_ylabel('Depth (m)')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='lower left')

# Plot Drained (Long-Term)
ax2.plot(qs_drained, depths, 'g--', label='Skin Friction ($Q_s$)')
ax2.plot(qb_drained, depths, 'b--', label='End Bearing ($Q_b$)')
ax2.plot(qu_drained, depths, 'r-', linewidth=2, label='Total Ultimate ($Q_u$)')
ax2.set_title('Drained Capacity (Long-Term)')
ax2.set_xlabel('Capacity (kN)')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='lower left')

plt.gca().invert_yaxis()
plt.suptitle('Silty Clay Driven Pile Profiler', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
