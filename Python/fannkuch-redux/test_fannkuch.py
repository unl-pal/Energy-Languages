
import os
import time
import importlib
from math import factorial
from itertools import islice, permutations as py_perms

import pytest

# ---------------------------------------------------------------------------
# Module-under-test selection: switch by environment variable
#   MODULE_NAME=optimized_code  or  MODULE_NAME=fannkuchredux
# ---------------------------------------------------------------------------
MODULE_NAME = os.getenv("MODULE_NAME", "optimized_code")
M = importlib.import_module(MODULE_NAME)

# Register a 'perf' marker to avoid PytestUnknownMarkWarning
def pytest_configure(config):
    config.addinivalue_line("markers", "perf: performance/timing checks")

# ---------------------------------------------------------------------------
# Helpers for correctness checks
# ---------------------------------------------------------------------------
def count_prefix_flips_one_perm(perm):
    """Return fannkuch flip count for a single permutation."""
    p = list(perm)  # copy
    flips = 0
    first = p[0]
    while first:
        i, j = 0, first
        while i < j:
            p[i], p[j] = p[j], p[i]
            i += 1
            j -= 1
        flips += 1
        first = p[0]
    return flips

def altern_sum_and_max_for_slice_via_module_perms(n, start, size):
    """
    Reference for alternating sum & max on a slice, computed by:
      1) using the module's permutations(), then
      2) recomputing flips locally for each permutation,
      3) alternating signs starting with +1.
    This avoids any assumption about permutation *order*.
    """
    total = 0
    alt = 1
    max_flips = 0
    for perm in islice(M.permutations(n, start, size), size):
        flips = count_prefix_flips_one_perm(perm)
        max_flips = max(max_flips, flips)
        total += alt * flips
        alt = -alt
    return total, max_flips

# ---------------------------------------------------------------------------
# Correctness & edge cases
# ---------------------------------------------------------------------------

def test_permutations_even_start_required_and_yields_for_size1():
    """Odd 'start' must raise (module keeps assert count[1]==0); even starts work."""
    n = 5
    # odd starts should trip the algorithm's internal assert
    for start in [1, 3, 5]:
        with pytest.raises(AssertionError):
            _ = next(M.permutations(n, start, 1))
    # a couple of even starts should succeed and yield exactly one permutation
    for start in [0, 2, 4]:
        got = list(islice(M.permutations(n, start, 1), 1))
        assert len(got) == 1
        assert isinstance(got[0], (list, tuple, bytearray))

def test_full_enumeration_matches_set_of_all_perms_n5():
    """Order may differ, but the *set* of permutations must match all permutations of 0..n-1."""
    n = 5
    total = factorial(n)
    mod_perms = list(islice(M.permutations(n, 0, total), total))
    got = sorted("".join(str(x) for x in p) for p in mod_perms)
    ref = sorted("".join(str(x) for x in p) for p in py_perms(range(n)))
    assert got == ref

def test_alternating_flips_generator_matches_reference_small():
    """Compare module's alternating_flips_generator against local reference on a small slice."""
    n, start, size = 5, 6, 20  # size even, start even
    # module:
    it = M.alternating_flips_generator(n, start, size)
    module_sum = sum(islice(it, size))
    module_max = next(it)
    # reference computed from module permutations (order-agnostic correctness)
    ref_sum, ref_max = altern_sum_and_max_for_slice_via_module_perms(n, start, size)
    assert module_sum == ref_sum
    assert module_max == ref_max

def test_task_matches_reference_on_slices():
    """task(n, start, size) should match the local reference for several slices."""
    n = 5
    # try a few scattered slices; make size even
    for start, size in [(0, 10), (10, 10), (40, 20)]:
        size += (size % 2)
        mod_sum, mod_max = M.task(n, start, size)
        ref_sum, ref_max = altern_sum_and_max_for_slice_via_module_perms(n, start, size)
        assert mod_sum == ref_sum
        assert mod_max == ref_max

def test_fannkuch_singleprocess_output_and_values(monkeypatch, capsys):
    """
    Force single-process path (cpu_count->1). Verify printed format and values for a small n.
    Values are computed via our local reference built on module permutations.
    """
    n = 6  # fast
    monkeypatch.setattr(M, "cpu_count", lambda: 1)
    # run
    M.fannkuch(n)
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2
    checksum_line, pf_line = out
    checksum = int(checksum_line)
    assert pf_line.startswith(f"Pfannkuchen({n}) = ")
    max_flips = int(pf_line.split(" = ")[1])
    # compute reference over full space using module permutations
    total = factorial(n)
    ref_sum, ref_max = altern_sum_and_max_for_slice_via_module_perms(n, 0, total)
    assert checksum == ref_sum
    assert max_flips == ref_max

def test_negative_n_prints_all_permutations_order_agnostic(capsys):
    """For n < 0 it prints all permutations (1-based). Order differs; check set."""
    n = -3
    M.fannkuch(n)
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == factorial(-n)
    got = sorted(out)
    ref = sorted("".join(str(x + 1) for x in p) for p in py_perms(range(-n)))
    assert got == ref

# ---------------------------------------------------------------------------
# End-to-end timing (execution time only; extendable via env)
# ---------------------------------------------------------------------------

@pytest.mark.perf
def test_perf_small_progression():
    """
    End-to-end timing across several n. Prints median/mean/stdev per n.
    Extend via env:
      PERF_NS="8,9,10,11"  PERF_REPEATS=5  MODULE_NAME=optimized_code  python -m pytest -q -s test.py
    """
    ns_env = os.getenv("PERF_NS", "8,9,10,11")
    repeats = int(os.getenv("PERF_REPEATS", "1"))
    ns = [int(x.strip()) for x in ns_env.split(",") if x.strip()]
  

    for n in ns:
        times = []
        for r in range(1, repeats + 1):
            t0 = time.perf_counter()
            M.fannkuch(n)
            dt = time.perf_counter() - t0
            times.append(dt)
            print(f"[perf] n={n} run={r}/{repeats} time={dt:.3f}s")
        # simple stats
        times_sorted = sorted(times)
        m = sum(times) / len(times)
        mid = len(times)//2
        median = (times_sorted[mid] if len(times)%2==1 else 0.5*(times_sorted[mid-1]+times_sorted[mid]))
        # stdev
        if len(times) > 1:
            var = sum((x - m) ** 2 for x in times) / (len(times) - 1)
            sd = var ** 0.5
        else:
            sd = 0.0
        print(f"[perf] n={n} median={median:.3f}s mean={m:.3f}s stdev={sd:.3f}s")

def test_multiprocess_vs_singleprocess_parity(monkeypatch):
    import importlib as _imp
    import optimized_code as M

    # single-process
    monkeypatch.setattr(M, "cpu_count", lambda: 1)
    from io import StringIO
    import sys
    buf1 = StringIO()
    old = sys.stdout; sys.stdout = buf1
    M.fannkuch(8)
    sys.stdout = old
    out1 = buf1.getvalue()

    # multiprocess (force >1 cores)
    monkeypatch.setattr(M, "cpu_count", lambda: 4)
    buf2 = StringIO()
    sys.stdout = buf2
    M.fannkuch(8)
    sys.stdout = old
    out2 = buf2.getvalue()

    assert out1 == out2

def test_tail_truncation_slice():
    import optimized_code as M
    from math import factorial
    from itertools import islice

    n = 7
    total = factorial(n)
    remaining = 6
    start = total - remaining     # even start
    size = remaining              # <= n! - start

    s1, m1 = M.task(n, start, size)

    perms = list(islice(M.permutations(n, start, size), size))
    alt = 1  # start is even
    ref_sum = ref_max = 0
    for p in perms:
        q = list(p); flips = 0
        while q[0] != 0:
            q[:q[0]+1] = q[q[0]::-1]
            flips += 1
        ref_sum += alt * flips
        ref_max = max(ref_max, flips)
        alt = -alt

    assert (s1, m1) == (ref_sum, ref_max)
