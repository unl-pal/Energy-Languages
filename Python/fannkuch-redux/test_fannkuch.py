from fannkuch import permutations, alternating_flips_generator, task

# ===== Test permutations =====
perms = list(permutations(3, 0, 6))
expected = [
    bytearray([0, 1, 2]),
    bytearray([0, 2, 1]),
    bytearray([1, 0, 2]),
    bytearray([1, 2, 0]),
    bytearray([2, 0, 1]),
    bytearray([2, 1, 0])
]
assert perms == expected, f"permutations(3, 0, 6) failed: got {perms}"

# ===== Test alternating_flips_generator =====
gen = alternating_flips_generator(3, 0, 6)
flips = list(gen)
max_flips = flips[-1]
values = flips[:-1]
assert len(values) == 6, f"Expected 6 values, got {len(values)}"
assert isinstance(max_flips, int), f"Max flips should be int, got {type(max_flips)}"
assert all(isinstance(v, int) for v in values), "All flip values should be integers"

# ===== Test task =====
checksum, maximum = task(3, 0, 6)
assert isinstance(checksum, int), "Checksum should be int"
assert isinstance(maximum, int), "Maximum should be int"
assert checksum > 0, "Checksum should be positive"
assert maximum >= 0, "Maximum should be non-negative"

print("✅ All tests passed.")
