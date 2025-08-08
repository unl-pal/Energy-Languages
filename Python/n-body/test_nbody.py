from nbody import SYSTEM, PAIRS, advance, report_energy, offset_momentum

# Copy fresh system for testing (since advance() mutates state)
import copy
def fresh_system_and_pairs():
    bodies = copy.deepcopy(SYSTEM)
    pairs = [(bodies[i], bodies[j]) for i in range(len(bodies)) for j in range(i+1, len(bodies))]
    return bodies, pairs

# ===== Test offset_momentum brings total system momentum to zero =====
bodies, _ = fresh_system_and_pairs()
offset_momentum(bodies[0], bodies=bodies)

px, py, pz = 0.0, 0.0, 0.0
for (_, [vx, vy, vz], m) in bodies:
    px += vx * m
    py += vy * m
    pz += vz * m

assert abs(px) < 1e-10, f"px={px} not zero"
assert abs(py) < 1e-10, f"py={py} not zero"
assert abs(pz) < 1e-10, f"pz={pz} not zero"

# ===== Test energy decreases after advance (approximate check) =====
bodies, pairs = fresh_system_and_pairs()
offset_momentum(bodies[0], bodies=bodies)

e1 = report_energy(bodies=bodies, pairs=pairs)
advance(0.01, 10, bodies=bodies, pairs=pairs)
e2 = report_energy(bodies=bodies, pairs=pairs)

assert isinstance(e1, float) and isinstance(e2, float), "Energies must be floats"
assert abs(e2 - e1) < 1e-2, f"Unexpected energy drift: {e1} -> {e2}"

print("✅ All nbody tests passed.")
