from mandelbrot import pixels, compute_row, compute_rows
import types

# ===== Test pixels generator =====
gen = pixels(0, 8, abs)
first_byte = next(gen)
assert isinstance(first_byte, int), "pixels() should yield integers"
assert 0 <= first_byte <= 255, "Each pixel byte should be a valid 8-bit value"

# ===== Test compute_row =====
y, n = 0, 8
row_y, row_data = compute_row((y, n))
assert row_y == 0, "compute_row should return correct y-coordinate"
assert isinstance(row_data, bytearray), "Row data should be a bytearray"
assert len(row_data) == 1, "For n=8, expect 1 byte in output"

# ===== Test compute_rows with serial fallback =====
rows = list(compute_rows(4, compute_row))  # Avoid triggering multiprocessing
assert len(rows) == 4, "Expected 4 rows"
for y, row in rows:
    assert isinstance(row, bytearray), "Each row should be a bytearray"
    assert len(row) == 1, "Each row should be one byte for n=8"

print("✅ All mandelbrot tests passed.")
