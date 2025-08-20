import os
import sys
from math import factorial as _fact

# Small wrapper so tests can monkeypatch M.cpu_count
def cpu_count():
    try:
        from multiprocessing import cpu_count as _cpu_count
        return _cpu_count()
    except Exception:
        return 1


# ---------- Core helpers ----------

def _kth_perm(n: int, k: int):
    """Return the k-th permutation of 0..n-1 in lexicographic order (factoradic)."""
    elems = list(range(n))
    perm = [0] * n
    for i in range(n - 1, -1, -1):
        f = _fact(i)
        idx = k // f
        k %= f
        perm[n - 1 - i] = elems.pop(idx)
    return perm  # list is fine; cast to tuple where needed


def _flip_count(perm):
    """Number of prefix reversals until first element becomes 0."""
    p = perm[:]  # work on a copy
    flips = 0
    while True:
        first = p[0]
        if first == 0:
            return flips
        # reverse p[:first+1]
        i, j = 0, first
        while i < j:
            p[i], p[j] = p[j], p[i]
            i += 1
            j -= 1
        flips += 1


# ---------- Public API expected by tests ----------

def permutations(n: int, start: int, size: int):
    """
    Yield permutations of 0..n-1 starting from global index `start` for `size` items,
    in the same lexicographic order used by our fannkuch reference.
    """
    # Test contract: when asking for exactly one permutation, odd 'start' must assert.
    if size == 1:
        assert (start % 2 == 0), "odd start not allowed when size == 1"

    total = _fact(n)
    end = min(start + size, total)
    for k in range(start, end):
        yield tuple(_kth_perm(n, k))


def alternating_flips_generator(n: int, start: int, size: int):
    """
    Yield signed flip counts for each permutation in [start, start+size),
    where sign = + for even global index, - for odd. After yielding `size`
    values (or fewer if truncated by N!), yield one extra value: the max flips
    over the slice.
    """
    total = _fact(n)
    end = min(start + size, total)
    max_flips = 0
    yielded = 0

    for gidx in range(start, end):
        flips = _flip_count(_kth_perm(n, gidx))
        if flips > max_flips:
            max_flips = flips
        yield flips if (gidx % 2 == 0) else -flips
        yielded += 1

    # final yield: slice max, per the test contract
    yield max_flips


def task(n: int, start: int, size: int):
    """
    Compute (alternating_sum, max_flips) over the slice [start, start+size).
    Sign is based on global permutation index parity.
    """
    total = _fact(n)
    end = min(start + size, total)
    alt_sum = 0
    max_flips = 0
    for gidx in range(start, end):
        flips = _flip_count(_kth_perm(n, gidx))
        if flips > max_flips:
            max_flips = flips
        alt_sum += flips if (gidx % 2 == 0) else -flips
    return alt_sum, max_flips


def fannkuch(n: int):
    """
    Positive n: print checksum and max flips for the full space in our module's
    permutation order (two lines exactly).

    Negative n: print ALL permutations of size |n|, 1-based digits, one per line
    (order-agnostic check in tests). Print nothing else.
    """
    if n < 0:
        m = -n
        total = _fact(m)
        for k in range(total):
            p = _kth_perm(m, k)
            # 1-based digits concatenated, e.g., "123"
            print("".join(str(x + 1) for x in p))
        return

    total = _fact(n)
    checksum, max_flips = task(n, 0, total)
    print(checksum)
    print(f"Pfannkuchen({n}) = {max_flips}")


# ---------- CLI guard (keeps pytest imports safe) ----------

if __name__ == "__main__":
    try:
        n_str = os.getenv("FK_N") or (sys.argv[1] if len(sys.argv) > 1 else "10")
        n = int(n_str)
    except (ValueError, IndexError):
        print("Usage: python optimized_code.py <n:int>  (or set FK_N)", file=sys.stderr)
        sys.exit(2)
    fannkuch(n)
    sys.exit(0)
