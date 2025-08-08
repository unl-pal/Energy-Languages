import io
import sys
from fasta import repeat_fasta, random_fasta, make_cumulative, alu, iub, homosapiens

# Helper to capture binary stdout
class BinaryStdoutCapture:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self.buffer = io.BytesIO()
        sys.stdout = io.TextIOWrapper(self.buffer, encoding='utf-8')
        return self.buffer
    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout

# ===== Test make_cumulative =====
P, C = make_cumulative([('a', 0.5), ('b', 0.3), ('c', 0.2)])
assert len(P) == 3 and len(C) == 3, "make_cumulative should return cumulative probs and char ords"
assert round(P[-1], 5) == 1.0, "Cumulative probabilities should sum to 1.0"
assert C == [ord('a'), ord('b'), ord('c')], "Characters should be converted to ASCII"

# ===== Test repeat_fasta output (check formatting) =====
with BinaryStdoutCapture() as buffer:
    repeat_fasta("ACGT", 100)  # Will print 100 characters
output = buffer.getvalue().decode('utf-8')
lines = output.strip().split('\n')
assert all(len(line) <= 60 for line in lines), "Each line should be <= 60 characters"
total_chars = sum(len(line) for line in lines)
assert total_chars == 100, f"Expected 100 characters, got {total_chars}"

# ===== Test random_fasta output (check reproducibility and formatting) =====
with BinaryStdoutCapture() as buffer:
    seed = random_fasta(iub, 120, seed=42.0)
output = buffer.getvalue().decode('utf-8')
lines = output.strip().split('\n')
assert all(len(line) <= 60 for line in lines), "Random lines must be ≤ 60 characters"
assert sum(len(line) for line in lines) == 120, "Should output exactly 120 characters"

# ===== Check that random_fasta returns a float seed =====
assert isinstance(seed, float), "random_fasta should return a float seed"

print("✅ All fasta tests passed.")
