## 1. The Makefile (Your Helper Script)

make setup: Installs your Python packages.

make all: Compiles all your C++ executables.

make generate: Runs the dataset generator.

make benchmark: Runs the benchmark script. You can override the algorithms to test like this: make benchmark ALGO_LIST="./monotone_chain ./graham_scan"

make clean: Deletes all executables, output folders, and plots.