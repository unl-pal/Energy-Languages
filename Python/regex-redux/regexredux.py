# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# regex-dna program contributed by Dominique Wahli
# 2to3
# mp by Ahmad Syukri
# modified by Justin Peel
# converted from regex-dna program

from sys import stdin
from re import sub, findall
from multiprocessing import Pool

def init(arg):
    global seq
    seq = arg

def var_find(f):
    return len(findall(f, seq))

def main():
    seq = stdin.read()
    ilen = len(seq)

    seq = sub('>.*\n|\n', '', seq)
    clen = len(seq)

    pool = Pool(initializer = init, initargs = (seq,))

    variants = (
          'agggtaaa|tttaccct',
          '[cgt]gggtaaa|tttaccc[acg]',
          'a[act]ggtaaa|tttacc[agt]t',
          'ag[act]gtaaa|tttac[agt]ct',
          'agg[act]taaa|ttta[agt]cct',
          'aggg[acg]aaa|ttt[cgt]ccct',
          'agggt[cgt]aa|tt[acg]accct',
          'agggta[cgt]a|t[acg]taccct',
          'agggtaa[cgt]|[acg]ttaccct')
    for f in zip(variants, pool.imap(var_find, variants)):
        print(f[0], f[1])

    subst = {
          'tHa[Nt]' : '<4>', 'aND|caN|Ha[DS]|WaS' : '<3>', 'a[NSt]|BY' : '<2>',
          '<[^>]*>' : '|', '\\|[^|][^|]*\\|' : '-'}
    for f, r in list(subst.items()):
        seq = sub(f, r, seq)

    print()
    print(ilen)
    print(clen)
    print(len(seq))

variants = (
    'agggtaaa|tttaccct',
    '[cgt]gggtaaa|tttaccc[acg]',
    'a[act]ggtaaa|tttacc[agt]t',
    'ag[act]gtaaa|tttac[agt]ct',
    'agg[act]taaa|ttta[agt]cct',
    'aggg[acg]aaa|ttt[cgt]ccct',
    'agggt[cgt]aa|tt[acg]accct',
    'agggta[cgt]a|t[acg]taccct',
    'agggtaa[cgt]|[acg]ttaccct'
)

subst = {
    'tHa[Nt]' : '<4>', 'aND|caN|Ha[DS]|WaS' : '<3>', 'a[NSt]|BY' : '<2>',
    '<[^>]*>' : '|', '\\|[^|][^|]*\\|' : '-'
}

def run_regex_dna(seq):
    original_length = len(seq)
    cleaned = sub('>.*\n|\n', '', seq)
    cleaned_length = len(cleaned)

    variant_counts = [(v, len(findall(v, cleaned))) for v in variants]

    for f, r in subst.items():
        cleaned = sub(f, r, cleaned)

    final_length = len(cleaned)
    return {
        "original_length": original_length,
        "cleaned_length": cleaned_length,
        "final_length": final_length,
        "variant_counts": variant_counts
    }

def main():
    seq = stdin.read()
    results = run_regex_dna(seq)
    for v, count in results["variant_counts"]:
        print(v, count)
    print()
    print(results["original_length"])
    print(results["cleaned_length"])
    print(results["final_length"])


if __name__=="__main__":
    main()
