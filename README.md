# DLP Vector Processor Simulator

**CECS 530 — Advanced Computer Architecture | CSULB Fall 2026 | Sec 01 | Assignment 4**

A small Python simulator for data-level parallelism. It runs vector operations with strip mining, simulates memory bank conflicts for different strides, and compares vector and scalar execution time for DAXPY.

---

## What It Does

| Question | Task | Result |
|---|---|---|
| 1 | Vector add, multiply, scalar multiply, strip mining | TBD |
| 2 | Memory bank simulation, strides 1 to 16 | TBD |
| 3 | DAXPY cycles, vector vs scalar | TBD |
| 4 | Performance analysis | See report |

## Repository Structure

```
.
├── README.md
├── .gitignore
├── requirements.txt         matplotlib, only used for the graph
├── vector_simulator.py      simulator, Questions 1 to 3
├── plot_results.py          Question 2 graph
└── output/
    └── program_output.txt   saved output of one run
```

## Getting Started

The simulator uses only the Python standard library (Python 3.8 or newer). Only the graph needs `matplotlib`.

```bash
git clone https://github.com/omargalal20/cecs530-dlp-vector-simulator.git
cd cecs530-dlp-vector-simulator
python vector_simulator.py
```

To make the graph:

```bash
pip install -r requirements.txt
python plot_results.py
```

## Author

Omar Elhanafy — CECS 530, California State University, Long Beach.
