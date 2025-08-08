# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/

# Contributed by Sebastien Loisel
# Fixed by Isaac Gouy
# Sped up by Josh Goldfoot
# Dirtily sped up by Simon Descarpentries
# Concurrency by Jason Stitt
# 2to3

from multiprocessing import Pool
from math import sqrt
from sys import argv

def eval_A(i, j):
    return 1.0 / ((i + j) * (i + j + 1) / 2 + i + 1)

def eval_A_times_u(u, pool):
    args = ((i, u) for i in range(len(u)))
    return pool.map(part_A_times_u, args)

def eval_At_times_u(u, pool):
    args = ((i, u) for i in range(len(u)))
    return pool.map(part_At_times_u, args)

def eval_AtA_times_u(u, pool):
    return eval_At_times_u(eval_A_times_u(u, pool), pool)

def part_A_times_u(args):
    i, u = args
    return sum(eval_A(i, j) * u_j for j, u_j in enumerate(u))

def part_At_times_u(args):
    i, u = args
    return sum(eval_A(j, i) * u_j for j, u_j in enumerate(u))

def main():
    n = int(argv[1])
    u = [1.0] * n

    with Pool(processes=4) as pool:
        for _ in range(10):
            v = eval_AtA_times_u(u, pool)
            u = eval_AtA_times_u(v, pool)

        vBv = sum(ue * ve for ue, ve in zip(u, v))
        vv  = sum(ve * ve for ve in v)

    print("%.9f" % sqrt(vBv / vv))

if __name__ == '__main__':
    main()
