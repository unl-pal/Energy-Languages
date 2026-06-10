# GreenRepo Microbenchmark Suite

This repository contains the microbenchmark suite used in the GreenRepo evaluation. It is based on the Energy-Languages benchmark from the Green Software Lab, which provides 10 benchmark programs from the Computer Language Benchmark Game across multiple programming languages.

For GreenRepo, we use only the Python and Java versions of the 10 benchmark programs. We modified the benchmark setup to support GreenRepo's optimization and validation workflow.

The 10 benchmark programs are:

```text
binary-trees
fannkuch-redux
fasta
k-nucleotide
mandelbrot
n-body
pidigits
regex-redux
reverse-complement
spectral-norm
```

## Changes made for GreenRepo

Compared with the original Energy-Languages repository, this version was adapted for GreenRepo in the following ways:

1. We focus only on the Python and Java implementations, since these are the two languages currently supported by GreenRepo.
2. We updated the Makefiles used by the Python and Java benchmarks.
3. We added test files for the microbenchmarks so that GreenRepo can validate functional correctness after optimization.
4. The Makefiles are used to run the benchmark workload for both the original version and the optimized version during GreenRepo evaluation.

The goal of these changes is to make the microbenchmarks usable as a controlled evaluation dataset for LLM-based energy optimization.


## Running benchmark tests

The benchmark tests are used by GreenRepo to check whether an optimized version still preserves the expected behavior.

To run the test target manually:

```bash
make test
```
## Notes

This repository is not intended to reproduce the full Energy-Languages study across all 28 languages. Instead, it contains the Python and Java microbenchmarks adapted for GreenRepo's evaluation workflow.

The original Energy-Languages repository and benchmark framework are available from the Green Software Lab:

```text
https://github.com/greensoftwarelab/Energy-Languages
```
