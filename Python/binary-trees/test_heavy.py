# Heavy/large test for the binary-trees benchmark script.
# Place this file in the same folder as your 'binarytrees.python3' script.
#
# Usage:
#   HEAVY_N=18 REPEAT=2 python -m pytest -q test_heavy_binary_trees.py
#
# Notes:
# - HEAVY_N sets the 'n' argument passed to the script (default: 18).
# - REPEAT controls how many times to run the heavy test (default: 1).

import os
import re
import sys
import subprocess
import time
import platform
import pathlib
import pytest

# Script filename (adjust if your file is named differently)
SCRIPT = "binarytrees.py"

# Regex to parse lines the program prints
RE_STRETCH = re.compile(r"^stretch tree of depth (\d+)\s+check:\s+(\d+)\s*$")
RE_TREES   = re.compile(r"^(\d+)\s+trees of depth\s+(\d+)\s+check:\s+(\d+)\s*$")
RE_LONG    = re.compile(r"^long lived tree of depth (\d+)\s+check:\s+(\d+)\s*$")

def nodes_in_full_binary_tree(depth: int) -> int:
    # For the implementation provided, check_tree returns total node count:
    # nodes(d) = 2^(d+1) - 1
    return (1 << (depth + 1)) - 1

def run_once(n: int):
    """Run the script in a subprocess with argument n, return (exit, stdout, stderr, elapsed)."""
    py = sys.executable  # current Python
    cmd = [py, SCRIPT, str(n)]
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0
    return proc.returncode, proc.stdout, proc.stderr, elapsed

def parse_and_validate(stdout: str):
    """
    Parse output lines and validate:
      - stretch line: check == nodes(stretch_depth)
      - each 'trees of depth d' line: check == i * nodes(d)
      - long lived line: check == nodes(max_depth)
    Returns dict summary.
    """
    stretch_depth = None
    max_depth = None
    min_depth = None  # inferred later from the set of 'd' encountered
    trees_rows = []

    # Parse
    for line in stdout.splitlines():
        line = line.strip().replace("\t", "    ")
        m = RE_STRETCH.match(line)
        if m:
            d = int(m.group(1))
            chk = int(m.group(2))
            assert chk == nodes_in_full_binary_tree(d), (
                f"Stretch check mismatch: got {chk}, expected {nodes_in_full_binary_tree(d)} (depth={d})"
            )
            stretch_depth = d
            continue

        m = RE_TREES.match(line)
        if m:
            i = int(m.group(1))
            d = int(m.group(2))
            chk = int(m.group(3))
            expected = i * nodes_in_full_binary_tree(d)
            assert chk == expected, (
                f"Trees row mismatch: depth={d}, i={i}, got check={chk}, expected {expected}"
            )
            trees_rows.append((i, d, chk))
            continue

        m = RE_LONG.match(line)
        if m:
            d = int(m.group(1))
            chk = int(m.group(2))
            assert chk == nodes_in_full_binary_tree(d), (
                f"Long-lived check mismatch: got {chk}, expected {nodes_in_full_binary_tree(d)} (depth={d})"
            )
            max_depth = d
            continue

    # Sanity: we should have seen at least one of each block
    assert stretch_depth is not None, "Missing 'stretch tree' line."
    assert max_depth is not None, "Missing 'long lived tree' line."
    assert trees_rows, "No 'trees of depth' lines parsed."

    # Infer min_depth from the trees block
    all_d = sorted({d for _, d, _ in trees_rows})
    min_depth = min(all_d)

    # Additional invariant from the program:
    # stretch_depth == max_depth + 1
    assert stretch_depth == max_depth + 1, (
        f"Expected stretch_depth=max_depth+1, got stretch={stretch_depth}, max={max_depth}"
    )

    # Check that d climbs in steps of 2 from min_depth to max_depth inclusive
    expected_ds = list(range(min_depth, stretch_depth, 2))
    assert all_d == expected_ds, (
        f"Depth sequence mismatch. Got {all_d}, expected {expected_ds}"
    )

    # For each trees row, i == 2^(max_depth + min_depth - d)
    mmd = max_depth + min_depth
    for (i, d, _) in trees_rows:
        expected_i = 1 << (mmd - d)
        assert i == expected_i, (
            f"i mismatch for depth={d}. Got {i}, expected {expected_i}"
        )

    return {
        "stretch_depth": stretch_depth,
        "max_depth": max_depth,
        "min_depth": min_depth,
        "rows": len(trees_rows),
    }

def test_heavy_correctness_and_scaling():
    """
    Heavy run:
      - Uses a large N (default 18; override with HEAVY_N env var).
      - Repeats a few times (REPEAT env var; default 1).
      - Validates mathematical correctness of every printed line.
      - Ensures runtime isn't trivial (basic sanity timing).
    """
    n = int(os.getenv("HEAVY_N", "20"))
    repeat = int(os.getenv("REPEAT", "1"))

    # Make sure the script exists where we expect it
    script_path = pathlib.Path(SCRIPT)
    assert script_path.exists(), f"Script not found: {script_path.resolve()}"

    min_elapsed_any = None
    for r in range(repeat):
        code, out, err, elapsed = run_once(n)
        assert code == 0, f"Process exit {code} != 0\nSTDERR:\n{err}\nSTDOUT:\n{out}"
        summary = parse_and_validate(out)

        # Keep the smallest elapsed to avoid failing slow local boxes
        min_elapsed_any = elapsed if (min_elapsed_any is None or elapsed < min_elapsed_any) else min_elapsed_any

        # Print a small run summary (pytest will show on failure)
        print(f"[Run {r+1}/{repeat}] n={n} "
              f"min_depth={summary['min_depth']} max_depth={summary['max_depth']} "
              f"stretch={summary['stretch_depth']} rows={summary['rows']} elapsed={elapsed:.3f}s")

    # Timing sanity (not a strict perf assertion—just guard against trivially-fast runs):
    # Require that at least one run took >= 0.1s for these heavy params (tune if needed).
    assert min_elapsed_any is not None
    assert min_elapsed_any >= float(os.getenv("MIN_HEAVY_SECONDS", "0.10")), (
        f"Heavy run completed too quickly ({min_elapsed_any:.3f}s). "
        "Increase HEAVY_N or run on a less optimized environment if you need more load."
    )
    
  
