# DLP Vector Processor Simulator

**CECS 530 — Advanced Computer Architecture | CSULB Fall 2026 | Sec 01 | Assignment 4**

A small Python simulator for data-level parallelism. It runs vector operations with strip mining, simulates memory bank conflicts for different strides, and compares vector and scalar execution time for DAXPY.

---

## What It Does

| Question | Task | Result |
|---|---|---|
| 1 | Vector add, multiply, scalar multiply, strip mining, instruction counts | All results match scalar code. n=150 splits into 64 + 64 + 22. Vector add at n=64: 13 instructions vs 513 scalar |
| 2 | Memory bank simulation, strides 1 to 16 | 76, 106, 200, 391, 391 cycles for strides 1, 2, 4, 8, 16 |
| 3 | DAXPY cycles, vector vs scalar | 369 vector vs 514 scalar cycles at n=64 (1.39x) |
| 4 | Performance analysis | See report |

## Background

| Term | Meaning |
|---|---|
| **Vector instruction** | One instruction that works on many elements, such as a whole array add |
| **MVL** | Maximum vector length: the most elements one vector instruction can handle (64 here) |
| **VL** | Vector length: how many elements one instruction handles. VL = min(MVL, elements left) |
| **Strip mining** | Splitting a long vector into strips of at most MVL elements and running one strip at a time |
| **Startup latency** | Cycles before a vector instruction produces its first result. After that, one element per cycle |
| **Memory bank** | An independent part of memory. Element `i` is in bank `i mod 8` |
| **Bank busy time** | Cycles a bank cannot accept a new request after it accepts one |
| **Stride** | The distance between consecutive elements that a vector load reads |
| **Chaining** | Starting a dependent vector instruction before the previous one has finished. Not used in Question 3 |

## Assumptions

Machine values come from the assignment. The rest follow the lecture.

- MVL is 64. One vector lane processes one element per cycle after the startup latency.
- Startup latencies: load 12, multiply 7, add 6, store 12 cycles.
- One vector instruction takes `startup + VL` cycles (lecture: 64 + 6 = 70).
- Question 3 runs the instructions one after another, with no chaining and no bank conflicts.
- Strip mining loop overhead is not given, so it is 0 cycles.
- Scalar code runs one instruction per cycle. The scalar DAXPY loop has 8 instructions plus 2 setup, as in the lecture (258 instructions for 32 elements).
- Instruction counts use the lecture's loops. The vector loop is always the strip-mined loop (11 instructions for DAXPY), so it is slightly longer than the lecture's 8-instruction vector example, which has no loop.
- Memory: requests are issued in order, at most one per cycle, to bank `address mod 8`. A busy bank makes the request, and the ones behind it, wait. Total cycles = 12 + the cycle of the last request (counted from 1).
- Random test vectors use fixed seeds, so every run gives the same output.

## Repository Structure

```
.
├── README.md
├── .gitignore
├── requirements.txt         matplotlib, only used for the graph
├── vector_simulator.py      simulator, Questions 1 to 3
├── plot_results.py          Question 2 graph
└── output/
    ├── program_output.txt   saved output of one run
    └── q2_stride_cycles.png Question 2 graph
```

## Getting Started

The simulator uses only the Python standard library (Python 3.8 or newer). Only the graph needs `matplotlib`.

```bash
git clone https://github.com/omargalal20/cecs530-dlp-vector-simulator.git
cd cecs530-dlp-vector-simulator
python vector_simulator.py
```

On Windows, use `py vector_simulator.py` if `python` is not on your PATH.

To save the output:

```bash
python vector_simulator.py > output/program_output.txt
```

To make the graph:

```bash
pip install -r requirements.txt
python plot_results.py
```

## Code Overview

| Part | Functions |
|---|---|
| Vector operations (Q1a) | `vadd`, `vmul`, `vscalar_mul`, `check_operands`, scalar versions `scalar_add`, `scalar_mul`, `scalar_scalar_mul` |
| Strip mining (Q1b) | `strip_mine`, `run_strip_mined` |
| Instruction counts (Q1c) | `scalar_instruction_count`, `vector_instruction_count` |
| Memory banks (Q2) | `simulate_banks`, `total_cycles`, `banks_visited`, `conflict_expected` |
| DAXPY (Q3) | `daxpy_vector`, `daxpy_scalar`, `strip_timeline`, `daxpy_vector_cycles`, `daxpy_scalar_cycles` |
| Output | `print_question_*` functions print each question |
| Questions | `question_*` functions compute and return results; `main` runs them in order |
| Graph | `draw_stride_chart` in `plot_results.py` |

`question_*` functions only compute and return results. Printing is done afterwards by `print_question_*`.

## Results

**Question 2: memory access cycles (64 elements, 8 banks, busy 6, latency 12)**

| Stride | Banks used | Conflicts | Total cycles | Cycles per element |
|---|---|---|---|---|
| 1 | 8 | 0 | 76 | 1.19 |
| 2 | 4 | 15 | 106 | 1.66 |
| 4 | 2 | 31 | 200 | 3.12 |
| 8 | 1 | 63 | 391 | 6.11 |
| 16 | 1 | 63 | 391 | 6.11 |

**Question 3: DAXPY cycles (no chaining)**

| n | Strips | Vector cycles | Scalar cycles | Speedup |
|---|---|---|---|---|
| 64 | 1 | 369 | 514 | 1.39x |
| 128 | 2 | 738 | 1026 | 1.39x |
| 256 | 4 | 1476 | 2050 | 1.39x |

One strip costs 49 startup cycles + 5 instructions × 64 elements = 369 cycles. MVL stays at 64, so the startup is paid again for every strip and the cost per element stays at 5.77.

## Limitations

- Question 3 follows the simplified model in the assignment: no chaining, no bank conflicts, no strip mining loop overhead.
- The scalar timing is an instruction count at one instruction per cycle. It ignores pipeline stalls and memory latency.
- The bank simulator models one vector load with a fixed stride, not a mix of loads and stores.
- The graph needs `matplotlib`; the simulator itself does not.

## Author

Omar Elhanafy — CECS 530, California State University, Long Beach.
