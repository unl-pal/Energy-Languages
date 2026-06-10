# GreenRepo Microbenchmark Suite

This repository contains the microbenchmark suite used in the GreenRepo evaluation. It is based on the Energy-Languages benchmark from the Green Software Lab, which provides 10 benchmark programs from the Computer Language Benchmark Game across multiple programming languages.

For GreenRepo, we use only the Python and Java versions of the 10 benchmark programs. We modified the benchmark setup to support GreenRepo's optimization and validation workflow.

## What is included

This repository contains:

```text
Python/     # Python implementations of the 10 microbenchmarks
Java/       # Java implementations of the 10 microbenchmarks
gen-input.sh
```

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

## Repository structure

The relevant folder structure is:

```text
Python/
  binary-trees/
  fannkuch-redux/
  fasta/
  k-nucleotide/
  mandelbrot/
  n-body/
  pidigits/
  regex-redux/
  reverse-complement/
  spectral-norm/

Java/
  binary-trees/
  fannkuch-redux/
  fasta/
  k-nucleotide/
  mandelbrot/
  n-body/
  pidigits/
  regex-redux/
  reverse-complement/
  spectral-norm/

gen-input.sh
```

Each benchmark directory contains the benchmark source code, a Makefile, and the test files needed by GreenRepo.

## Generating benchmark inputs

Some benchmarks require input files. Generate them by running:

```bash
./gen-input.sh
```

This creates the input files used by benchmarks such as:

```text
k-nucleotide
regex-redux
reverse-complement
```

## Running a benchmark manually

Each benchmark directory contains a Makefile. To run a benchmark manually, go to the benchmark directory and run:

```bash
make run
```

For example:

```bash
cd Python/binary-trees
make run
```

or:

```bash
cd Java/binary-trees
make run
```

## Running benchmark tests

The benchmark tests are used by GreenRepo to check whether an optimized version still preserves the expected behavior.

To run the test target manually:

```bash
make test
```

For example:

```bash
cd Python/fasta
make test
```

or:

```bash
cd Java/fasta
make test
```

A benchmark is considered valid for GreenRepo only if its test target passes before optimization.

## Use with GreenRepo

GreenRepo uses this repository as the microbenchmark dataset. For each benchmark, GreenRepo:

1. Starts from the original benchmark implementation.
2. Sends source files to the selected LLM for optimization.
3. Runs the benchmark's test workload to validate correctness.
4. Keeps only optimized code that passes validation.
5. Measures the energy consumption of the original version and the optimized version using `perf stat`.
6. Computes the energy improvement from the mean of five measurements for each version.

The energy improvement is computed as:

```text
Improvement =
(Energy_original - Energy_optimized) / Energy_original * 100
```

A positive value means that the optimized version consumed less energy than the original version.

## Notes

This repository is not intended to reproduce the full Energy-Languages study across all 28 languages. Instead, it contains the Python and Java microbenchmarks adapted for GreenRepo's evaluation workflow.

The original Energy-Languages repository and benchmark framework are available from the Green Software Lab:

```text
https://github.com/greensoftwarelab/Energy-Languages
```

## Acknowledgment

This benchmark suite is based on the Energy-Languages benchmark from the Green Software Lab, which uses programs from the Computer Language Benchmark Game.
