# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# contributed by Joerg Baumann
# many thanks to Oleg Mazurov for his helpful description
#
# This version:
# - Numba-accelerated hot path (serial; default when available).
# - Pure-Python fallback improved: one-shot factoradic decode + slice-based nested rotations.
# - Preserves the original contract: same order, same asserts, same output.

from sys import argv
from math import factorial
from multiprocessing import cpu_count, Pool
from itertools import islice, starmap
from functools import lru_cache
import os

# -------------------- Toggles --------------------

# Force pure-Python path even if Numba is installed (for A/B checks).
# You can also set env var: FORCE_PURE_PY=1
FORCE_PURE_PY = bool(int(os.getenv("FORCE_PURE_PY", "0")))

# If Numba is present, we default to single-process (best on Windows).
USE_POOL_WITH_NUMBA = False
# Optional threaded kernel (kept False by default for simplicity).
USE_NUMBA_PARALLEL = False

# -------------------- Optional acceleration detection --------------------

NUMBA_AVAILABLE = False
try:
    import numpy as _np
    from numba import njit
    if USE_NUMBA_PARALLEL:
        from numba import prange, get_num_threads
    NUMBA_AVAILABLE = True
except Exception:
    NUMBA_AVAILABLE = False

# -------------------- Pure-Python helpers --------------------

@lru_cache(maxsize=None)
def _facts(n: int):
    """Factorials 0..n (cached, pure-Python)."""
    f = [1] * (n + 1)
    for i in range(2, n + 1):
        f[i] = f[i - 1] * i
    return tuple(f)

# -------------------- Public API --------------------

def permutations(n, start, size):
    """
    Yield permutations of 0..n-1 starting from global index `start` for `size` items
    in the module's canonical order. Infinite generator; caller limits via islice.
    """
    p = bytearray(range(n))
    count = bytearray(n)
    facts = _facts(n)

    # One-shot factoradic decode: rotate prefix of length v+1 by count[v]
    remainder = start
    for v in range(n - 1, 0, -1):
        c, remainder = divmod(remainder, facts[v])  # 0 <= c <= v
        count[v] = c
        if c:
            # left-rotate p[:v+1] by c (single C-level slice op)
            t = p[:v + 1]
            k = c  # already <= v
            p[:v + 1] = t[k:] + t[:k]

    # Original contract (tests rely on these)
    assert count[1] == 0                    # even start only
    assert size < 2 or (size % 2 == 0)      # multi-perm slices must be even

    if size < 2:
        yield p[:]
        return

    while True:
        # perm #1
        yield p[:]

        # perm #2 (swap first two)
        p[0], p[1] = p[1], p[0]
        yield p[:]

        # advance to next block using nested prefix rotations (v = 1..i)
        i = 2
        while count[i] >= i:
            count[i] = 0
            i += 1
        else:
            count[i] += 1
            # for v in 1..i: rotate p[:v+1] left by 1 (C-level slices)
            for v in range(1, i + 1):
                tmp0 = p[0]
                p[:v] = p[1:v + 1]
                p[v] = tmp0

def alternating_flips_generator(n, start, size):
    """
    Yield exactly `size` signed flip counts for permutations from [start, start+size),
    alternating sign by global index; then yield one trailing value: the max flips.
    """
    maximum_flips = 0
    alternating_factor = 1  # start is guaranteed even by permutations() assert
    for permutation in islice(permutations(n, start, size), size):
        first = permutation[0]
        if first:
            flips_count = 1
            while True:
                permutation[:first + 1] = permutation[first::-1]
                first = permutation[0]
                if not first:
                    break
                flips_count += 1
            if maximum_flips < flips_count:
                maximum_flips = flips_count
            yield flips_count * alternating_factor
        else:
            yield 0
        alternating_factor = -alternating_factor
    yield maximum_flips

# -------------------- Numba kernels (fast path) --------------------

if NUMBA_AVAILABLE:
    @njit(cache=True)
    def _task_numba_serial(n, start, size):
        # factorials 0..n (int64 for divisions)
        facts = _np.empty(n + 1, dtype=_np.int64)
        facts[0] = 1
        for i in range(1, n + 1):
            facts[i] = facts[i - 1] * i

        # decode start -> p (uint8) and count (uint8)
        p = _np.arange(n, dtype=_np.uint8)
        count = _np.zeros(n, dtype=_np.uint8)
        remainder = start
        for v in range(n - 1, 0, -1):
            f = facts[v]
            c = remainder // f
            remainder -= c * f
            count[v] = _np.uint8(c)
            if c != 0:
                k = int(c % (v + 1))
                if k != 0:
                    tmp = _np.empty(v + 1, dtype=_np.uint8)
                    for j in range(v + 1):
                        src = j + k
                        if src >= v + 1:
                            src -= (v + 1)
                        tmp[j] = p[src]
                    for j in range(v + 1):
                        p[j] = tmp[j]

        # temp buffer for flips
        fp = _np.empty(n, dtype=_np.uint8)

        produced = 0
        alt = 1 if (start % 2 == 0) else -1
        checksum = 0
        max_flips = 0

        def flips_of_current():
            for j in range(n):
                fp[j] = p[j]
            flips = 0
            first = int(fp[0])
            if first != 0:
                flips = 1
                while True:
                    i0 = 0
                    j0 = first
                    while i0 < j0:
                        tmpv = fp[i0]
                        fp[i0] = fp[j0]
                        fp[j0] = tmpv
                        i0 += 1
                        j0 -= 1
                    first = int(fp[0])
                    if first == 0:
                        break
                    flips += 1
            return flips

        while produced < size:
            # perm #1
            flips = flips_of_current()
            checksum += alt * flips
            if flips > max_flips:
                max_flips = flips
            alt = -alt
            produced += 1
            if produced >= size:
                break

            # perm #2: swap p[0], p[1]
            t0 = p[0]
            p[0] = p[1]
            p[1] = t0

            flips = flips_of_current()
            checksum += alt * flips
            if flips > max_flips:
                max_flips = flips
            alt = -alt
            produced += 1
            if produced >= size:
                break

            # advance block: nested in-place prefix rotations (v = 1..i)
            i = 2
            while i < n and int(count[i]) >= i:
                count[i] = _np.uint8(0)
                i += 1
            if i < n:
                count[i] = _np.uint8(int(count[i]) + 1)
                for v in range(1, i + 1):
                    tmp0 = p[0]
                    for j in range(v):
                        p[j] = p[j + 1]
                    p[v] = tmp0

        return int(checksum), int(max_flips)

    # Optional threaded kernel (disabled by default)
    if USE_NUMBA_PARALLEL:
        from numba import prange, get_num_threads  # noqa: F401

        @njit(parallel=True, cache=True)
        def _task_numba_parallel(n, start, size):
            facts = _np.empty(n + 1, dtype=_np.int64)
            facts[0] = 1
            for i in range(1, n + 1):
                facts[i] = facts[i - 1] * i

            blocks = 1  # keep simple; you can extend this to split 'size' across threads
            sums = _np.zeros(blocks, dtype=_np.int64)
            maxs = _np.zeros(blocks, dtype=_np.int32)

            for b in prange(blocks):
                p = _np.arange(n, dtype=_np.uint8)
                count = _np.zeros(n, dtype=_np.uint8)
                rem = start
                for v in range(n - 1, 0, -1):
                    f = facts[v]
                    c = rem // f
                    rem -= c * f
                    count[v] = _np.uint8(c)
                    if c != 0:
                        k = int(c % (v + 1))
                        if k != 0:
                            tmp = _np.empty(v + 1, dtype=_np.uint8)
                            for j in range(v + 1):
                                src = j + k
                                if src >= v + 1:
                                    src -= (v + 1)
                                tmp[j] = p[src]
                            for j in range(v + 1):
                                p[j] = tmp[j]

                fp = _np.empty(n, dtype=_np.uint8)
                loc_sum = _np.int64(0)
                loc_max = _np.int32(0)
                alt = 1 if (start % 2 == 0) else -1
                produced = 0

                def flips_of_current():
                    for j in range(n):
                        fp[j] = p[j]
                    flips = 0
                    first = int(fp[0])
                    if first != 0:
                        flips = 1
                        while True:
                            i0 = 0
                            j0 = first
                            while i0 < j0:
                                tmpv = fp[i0]
                                fp[i0] = fp[j0]
                                fp[j0] = tmpv
                                i0 += 1
                                j0 -= 1
                            first = int(fp[0])
                            if first == 0:
                                break
                            flips += 1
                    return flips

                while produced < size:
                    flips = flips_of_current()
                    loc_sum += alt * flips
                    if flips > loc_max:
                        loc_max = flips
                    alt = -alt
                    produced += 1
                    if produced >= size:
                        break

                    t0 = p[0]; p[0] = p[1]; p[1] = t0
                    flips = flips_of_current()
                    loc_sum += alt * flips
                    if flips > loc_max:
                        loc_max = flips
                    alt = -alt
                    produced += 1
                    if produced >= size:
                        break

                    i = 2
                    while i < n and int(count[i]) >= i:
                        count[i] = _np.uint8(0)
                        i += 1
                    if i < n:
                        count[i] = _np.uint8(int(count[i]) + 1)
                        for v in range(1, i + 1):
                            tmp0 = p[0]
                            for j in range(v):
                                p[j] = p[j + 1]
                            p[v] = tmp0

                sums[b] = loc_sum
                maxs[b] = loc_max

            total = _np.int64(0)
            mx = _np.int32(0)
            for b in range(blocks):
                total += sums[b]
                if maxs[b] > mx:
                    mx = maxs[b]
            return int(total), int(mx)

# -------------------- Task selector --------------------

def task(n, start, size):
    """Compute (alternating_sum, max_flips) over the slice [start, start+size) (no truncation)."""
    if size < 1:
        return 0, 0
    if NUMBA_AVAILABLE and not FORCE_PURE_PY:
        if USE_NUMBA_PARALLEL:
            return _task_numba_parallel(n, start, size)
        else:
            return _task_numba_serial(n, start, size)
    # Fallback: generator-based
    alt_gen = alternating_flips_generator(n, start, size)
    return sum(islice(alt_gen, size)), next(alt_gen)

# -------------------- CLI entry --------------------

def fannkuch(n):
    if n < 0:
        m = -n
        total = factorial(m)
        for data in islice(permutations(m, 0, total), total):
            print(''.join(str(x + 1) for x in data))
    else:
        assert n > 0
        total = factorial(n)

        # Prefer single-process when using Numba fast path
        if NUMBA_AVAILABLE and not FORCE_PURE_PY and not USE_POOL_WITH_NUMBA:
            task_count = 1
            task_size = total
        else:
            task_count = cpu_count()
            task_size = (total + task_count - 1) // task_count
            if task_size < 20000:
                task_size = total
                task_count = 1

        assert task_size % 2 == 0

        task_args = [(n, i * task_size, task_size) for i in range(task_count)]

        if task_count > 1:
            with Pool() as pool:
                checksums, maximums = zip(*pool.starmap(task, task_args))
        else:
            checksums, maximums = zip(*starmap(task, task_args))

        checksum, maximum = sum(checksums), max(maximums)
        print(f"{checksum}\nPfannkuchen({n}) = {maximum}")

if __name__ == "__main__":
    fannkuch(int(argv[1]))
