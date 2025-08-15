import os, sys, time
sys.setrecursionlimit(10000)

# Change this to "binarytrees" or "optimized_code"
MODULE_NAME = "optimized_code"

M = __import__(MODULE_NAME)

BT_N = 20
BT_REPEAT =  1
def nodes(d: int) -> int:
    return (1 << (d + 1)) - 1

def test_small_correctness():
    make_tree = getattr(M, "make_tree")
    check_tree = getattr(M, "check_tree")
    for d in [0, 1, 2, 5, 10]:
        t = make_tree(d)
        assert check_tree(t) == nodes(d)
        assert check_tree(make_tree(d)) == nodes(d)

def test_get_argchunks_structure():
    get_argchunks = getattr(M, "get_argchunks", None)
    if get_argchunks is None:
        import pytest; pytest.skip(f"{MODULE_NAME}.get_argchunks not found")
    i, d, chunk = 10, 3, 4
    chunks = list(get_argchunks(i, d, chunksize=chunk))
    assert sum(len(c) for c in chunks) == i
    assert all(isinstance(c, list) for c in chunks)
    assert all(all(isinstance(p, tuple) and len(p) == 2 for p in c) for c in chunks)

def test_end_to_end():
    assert hasattr(M, "main"), f"{MODULE_NAME} must define main(N:int)"
    best = None
    for _ in range(BT_REPEAT):
        t0 = time.perf_counter()
        M.main(BT_N)
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    print(f"[end-to-end] module={M.__name__} N={BT_N} best={best:.3f}s")
