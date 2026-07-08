import math

# Inputs
D = 0.8  # Pile diameter in meters
L = 36.0  # Total pile length in meters
t = 0.00813  # Wall thickness in meters (8 mm)

# Geometric properties
A_g = (math.pi * D ** 2) / 4.0  # Gross base area
D_i = D - 2 * t  # Internal diameter
A_t = A_g - ((math.pi * D_i ** 2) / 4.0)  # Steel annulus cross-section area
A_s_ext = math.pi * D * L  # Total external shaft surface area
A_s_int = math.pi * D_i * L  # Total internal shaft surface area

# Stratigraphy and Unit Values
# Zone 1: 0 - 15m (Loose/Silty - Liquefiable, skin friction ignored)
L1 = 15.0
f_s1 = 0.0

# Zone 2: 15 - 30m (Medium Stable Stratum)
L2 = 15.0
f_s2 = 40.0  # kPa

# Zone 3: 30 - 36m (Dense Pliocene Clay / Anchor Zone)
L3 = 6.0
f_s3 = 75.0  # kPa
q_b = 10000.0  # kPa (10 MPa) Unit tip resistance for clay basement

# 1. External Shaft Friction (Qs_ext)
Q_s_ext = (f_s1 * math.pi * D * L1) + (f_s2 * math.pi * D * L2) + (f_s3 * math.pi * D * L3)

# 2. End Bearing Scenarios
# Mode A: Fully Plugged (Gross base area)
Q_b_plugged = q_b * A_g

# Mode B: Unplugged (Steel wall annulus + Internal plug friction)
# The internal plug friction is generated in the dense lower layer where soil column locks up.
# Let's assume inner shaft friction matches or is slightly lower than outer (say 80%).
# However, usually it is bounded by the total plug block resistance. Let's compute f_s_int for Layer 3.
f_s3_int = 0.8 * f_s3
Q_s_int = (0.0 * math.pi * D_i * L1) + (f_s2 * 0.8 * math.pi * D_i * L2) + (f_s3_int * math.pi * D_i * L3)
Q_b_unplugged = (q_b * A_t) + Q_s_int

# Total Ultimate Capacities (Characteristic values)
Q_u_plugged = Q_s_ext + Q_b_plugged
Q_u_unplugged = Q_s_ext + Q_b_unplugged

# Design Capacity according to Eurocode 7 (DA1 Combination 1 / Design Approach 1)
# Standard partial safety factors for driven piles (EC7/UK or general template):
# gamma_s = 1.3 (shaft), gamma_b = 1.3 (base)
# Let's apply standard Eurocode model factor or correlation factors if 1 CPT is assumed (xi = 1.4)
xi = 1.4
R_k_plugged_shaft = Q_s_ext / xi
R_k_plugged_base = Q_b_plugged / xi

gamma_s = 1.3
gamma_b = 1.3

R_d_plugged = (R_k_plugged_shaft / gamma_s) + (R_k_plugged_base / gamma_b)

print(f"A_g: {A_g:.3f} m2, A_t: {A_t:.3f} m2, A_s_ext: {A_s_ext:.2f} m2")
print(f"Q_s_ext: {Q_s_ext:.2f} kN")
print(f"Q_b_plugged: {Q_b_plugged:.2f} kN, Total Ultimate Plugged: {Q_u_plugged:.2f} kN")
print(
    f"Q_b_unplugged (Annulus + Int Friction): {Q_b_unplugged:.2f} kN, Total Ultimate Unplugged: {Q_u_unplugged:.2f} kN")
print(f"Design Capacity Eurocode 7 (Plugged Mode): {R_d_plugged:.2f} kN")
# Use code with caution.2 sitesEurocode 7 – second generation – piled foundations - ISSMGEThe representative values of the pile resistance in axial compression 𝑅c, rep resp.of the base and shaft resistance 𝑅b, rep and...International Society for Soil Mechanics and Geotechnical EngineeringPile design to Eurocode 7 and the UK National Annex.Part 1For pile foundations, Combination I applies partial factors significantly.greater than unity to unfavourable.actions and only sm...
