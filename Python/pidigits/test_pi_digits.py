from pi_digits import compute_pi_digits

# ===== Test basic digit output =====
out = compute_pi_digits(10)
lines = out.strip().splitlines()

# Check number of lines
assert len(lines) == 1, f"Expected 1 line, got {len(lines)}"

# Check digit content
digits, label = lines[0].split('\t')
assert digits.isdigit(), "Output should contain only digits"
assert len(digits) == 10, "Should output 10 digits"
assert label.strip() == ":10", "Should label line with correct count"

# ===== Test with non-multiple-of-10 count =====
out = compute_pi_digits(13)
lines = out.strip().splitlines()

assert len(lines) == 2, f"Expected 2 lines, got {len(lines)}"
assert lines[1].endswith(":13"), "Last line label should end with :13"
all_digits = ''.join(line.split('\t')[0].strip() for line in lines)
assert all_digits.isdigit() and len(all_digits) == 13, "Should contain 13 digits total"

print("✅ All pi_digits tests passed.")
