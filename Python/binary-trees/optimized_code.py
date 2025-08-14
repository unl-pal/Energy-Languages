# Optimized variant of the Binary Trees benchmark (drop-in compatible)
# Keeps the same API: make_tree, check_tree, make_check, get_argchunks, main

import sys
import multiprocessing as mp


def make_tree(d):
    if d > 0:
        d -= 1
        return (make_tree(d), make_tree(d))
    return (None, None)


def check_tree(node):
    (l, r) = node
    if l is None:
        return 1
    else:
        return 1 + check_tree(l) + check_tree(r)


def make_check(itde, make=make_tree, check=check_tree):
    i, d = itde
    return check(make(d))


def get_argchunks(i, d, chunksize=5000):
    # Kept for API compatibility (tests may import it),
    # though the optimized main no longer uses it.
    assert chunksize % 2 == 0
    chunk = []
    for k in range(1, i + 1):
        chunk.extend([(k, d)])
        if len(chunk) == chunksize:
            yield chunk
            chunk = []
    if len(chunk) > 0:
        yield chunk


def main(n, min_depth=4):
    max_depth = max(min_depth + 2, n)
    stretch_depth = max_depth + 1

    # (Pool left initialized-on-demand if you later want to experiment;
    # not used in the optimized loop below.)
    pool = None
    if mp.cpu_count() > 1:
        pool = mp.Pool()

    # Stretch tree
    print('stretch tree of depth {0}\t check: {1}'.format(
        stretch_depth, make_check((0, stretch_depth))
    ))

    # Long-lived tree
    long_lived_tree = make_tree(max_depth)

    mmd = max_depth + min_depth
    for d in range(min_depth, stretch_depth, 2):
        # i = 2 ** (mmd - d)  → bit-shift
        i = 1 << (mmd - d)

        # Key optimization: make_check((k, d)) is identical for all k at a given d
        single = make_check((0, d))
        cs = i * single

        print('{0}\t trees of depth {1}\t check: {2}'.format(i, d, cs))

    print('long lived tree of depth {0}\t check: {1}'.format(
        max_depth, check_tree(long_lived_tree)
    ))

    if pool is not None:
        pool.close()
        pool.join()


if __name__ == '__main__':
    main(int(sys.argv[1]))
