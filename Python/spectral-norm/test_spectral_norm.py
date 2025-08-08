from spectral_norm import eval_A, part_A_times_u, part_At_times_u, eval_AtA_times_u
from multiprocessing import Pool
import math

# ===== Test eval_A(i,j) values =====
assert eval_A(0, 0) == 1.0 / (0*1/2 + 0 + 1), "eval_A(0,0) incorrect"
assert round(eval_A(1, 1), 6) == round(1.0 / ((2)*(3)/2 + 1 + 1), 6), "eval_A(1,1) incorrect"

# ===== Test part_A_times_u for known input =====
u = [1, 1, 1]
row0 = part_A_times_u((0, u))  # Should be sum of A[0][j] for j=0..2
manual = sum(eval_A(0, j) for j in range(3))
assert abs(row0 - manual) < 1e-12, "part_A_times_u incorrect"

# ===== Test part_At_times_u for known input =====
col0 = part_At_times_u((0, u))  # Should be sum of A[j][0] for j=0..2
manual = sum(eval_A(j, 0) for j in range(3))
assert abs(col0 - manual) < 1e-12, "part_At_times_u incorrect"

# ===== Test eval_AtA_times_u on small input =====
with Pool(processes=2) as pool:
    u = [1, 1, 1]
    result = eval_AtA_times_u(u, pool)
    assert isinstance(result, list), "Result should be a list"
    assert len(result) == len(u), "Output vector should match input size"
    assert all(isinstance(x, float) for x in result), "All entries should be floats"

    # Check magnitude isn't exploding
    norm = math.sqrt(sum(x*x for x in result))
    assert norm > 0, "Vector norm should be positive"
    assert norm < 10, "Unexpectedly large value"

print("✅ All spectral_norm tests passed.")
