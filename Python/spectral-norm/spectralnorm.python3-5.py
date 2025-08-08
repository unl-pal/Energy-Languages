# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/

# Contributed by Sebastien Loisel
# Fixed by Isaac Gouy
# Sped up by Josh Goldfoot
# Dirtily sped up by Simon Descarpentries
# Concurrency by Jason Stitt
# 2to3

from multiprocessing import Pool
from math            import sqrt

from sys             import argv

def eval_A (i, j):
    return 1.0 / ((i + j) * (i + j + 1) / 2 + i + 1)

def eval_A_times_u(u, pool):
    args = ((i, u) for i in range(len(u)))
    return pool.map(part_A_times_u, args)

def eval_At_times_u(u, pool):
    args = ((i, u) for i in range(len(u)))
    return pool.map(part_At_times_u, args)

def eval_AtA_times_u(u, pool):
    return eval_At_times_u(eval_A_times_u(u, pool), pool)

def part_A_times_u(xxx_todo_changeme):
    (i,u) = xxx_todo_changeme
    partial_sum = 0
    for j, u_j in enumerate(u):
        partial_sum += eval_A (i, j) * u_j
    return partial_sum

def part_At_times_u(xxx_todo_changeme1):
    (i,u) = xxx_todo_changeme1
    partial_sum = 0
    for j, u_j in enumerate(u):
        partial_sum += eval_A (j, i) * u_j
    return partial_sum

def main():
   with Pool(processes=4) as pool:
    for _ in range(10):
        v = eval_AtA_times_u(u, pool)
        u = eval_AtA_times_u(v, pool)

if __name__ == '__main__':
    pool = Pool(processes=4)
    main()
