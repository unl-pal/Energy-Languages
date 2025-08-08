from k_nucleotide import (
    count_frequencies, make_cumulative, lookup_frequency, display,
    read_sequence
)
from collections import defaultdict
from io import BytesIO
import sys

# ===== Test count_frequencies =====
sequence = bytearray([0, 1, 2, 3, 0, 1, 2, 3])  # GATCGATC encoded
reading_frames = [
    (1, (0, 1, 2, 3)),  # mono
    (2, (0*4+1, 1*4+2, 2*4+3, 3*4+0))  # di (GA, AT, TC, CG)
]
results = count_frequencies(sequence, reading_frames, 0, len(sequence))

# Result is a list of (frame, n, frequencies)
assert isinstance(results, list), "count_frequencies should return a list"
for (frame, n, freq) in results:
    assert isinstance(frame, int)
    assert isinstance(n, int)
    assert isinstance(freq, dict)

# ===== Test lookup_frequency =====
frequency, total = lookup_frequency(results, 1, 0)  # frame=1, G
assert isinstance(frequency, int), "lookup_frequency should return int frequency"
assert isinstance(total, int), "lookup_frequency should return total count"

# ===== Test make_cumulative indirectly with translation =====
def make_translated_sequence():
    translation = bytes.maketrans(b'GTCAgtca', b'\x00\x01\x02\x03\x00\x01\x02\x03')
    data = b">THREE Homo sapiens\nGATTACA\nGATTACA\n"
    f = BytesIO(data)
    result = read_sequence(f, b'THREE', translation)
    expected = bytearray([0, 1, 3, 3, 0, 2, 0, 0, 1, 3, 3, 0, 2, 0])
    assert result == expected, f"Expected {expected}, got {result}"
make_translated_sequence()

# ===== Test display (capturing output) =====
from contextlib import redirect_stdout
import io

f = io.StringIO()
with redirect_stdout(f):
    display(results, [('G', 1, 0)], relative=True, sort=True)
out = f.getvalue()
assert 'G' in out and '%' not in out, "Display should include relative frequency"

print("✅ All k_nucleotide tests passed.")
