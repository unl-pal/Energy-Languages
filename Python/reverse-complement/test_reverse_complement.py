from reverse_complement import reverse_complement, read_sequences, reverse_translation
from io import BytesIO

# ===== Test reverse_translation mapping =====
test_seq = b'ACGTacgt'
expected_rc = b'ACGTACGT'[::-1]  # Complement and reverse
result = test_seq.translate(reverse_translation)
assert result == expected_rc[::-1], f"Expected {expected_rc}, got {result}"

# ===== Test reverse_complement (basic case) =====
header = b'>seq1\n'
seq = b'ACGTACGT\n'
h_out, rc_out = reverse_complement(header, seq)
assert h_out == header, "Header should be unchanged"
# Output is bytearray starting with newline, each line ≤ 60 chars
rc_lines = rc_out.strip().split(b'\n')
assert all(len(line) <= 60 for line in rc_lines), "Each output line must be ≤ 60 chars"

# Reversing manually:
expected = b'ACGTACGT'.translate(reverse_translation)[::-1]
reconstructed = b''.join(rc_lines)
assert reconstructed == expected, "Reverse complement mismatch"

# ===== Test read_sequences (FASTA mock) =====
fasta = b""">SEQ1
ACGTACGT
ACGT
>SEQ2
TTTTCCCC
"""
f = BytesIO(fasta)
seqs = list(read_sequences(f))
assert len(seqs) == 2, "Should read two sequences"
assert seqs[0][0].startswith(b'>'), "First header must start with >"
assert seqs[0][1] == b'ACGTACGT\nACGT\n', "First sequence should match raw body"
assert seqs[1][0].startswith(b'>SEQ2'), "Second header match"
assert seqs[1][1] == b'TTTTCCCC\n', "Second sequence content match"

print("✅ All reverse_complement tests passed.")
