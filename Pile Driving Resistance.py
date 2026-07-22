import matplotlib.pyplot as plt
import numpy as np

# Simplified Soil & Pile Parameters
depths = np.linspace(0, 36, 100) # 0 to 20 meters
q_c = 5.0 + 1.5 * depths         # Tip resistance increases with depth
friction = 30.0                  # Uniform skin friction (kPa)
pile_perimeter = 0.8             # Meters

# Calculate Soil Resistance to Driving (SRD in kN)
srd = (friction * pile_perimeter * depths) + (q_c * np.pi * (0.5**2))

# Plotting the curve
plt.figure(figsize=(4.5, 1.5))
plt.plot(srd, depths, color='darkorange', linewidth=2, label='Total SRD')
plt.title('Pile Driving Resistance (SRD) Profile')
plt.xlabel('Resistance (kN)')
plt.ylabel('Depth (m)')
plt.gca().invert_yaxis() # Piles go down, so invert the y-axis
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
