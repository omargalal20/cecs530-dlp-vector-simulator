"""Vector processor simulator for CECS 530 Assignment 4.

Standard library only. Questions are added one at a time:
    Q1 vector operations and strip mining
    Q2 memory bank simulation
    Q3 DAXPY execution time
"""

# Machine parameters (from the assignment and lecture)
MVL = 64

STARTUP = {"load": 12, "mul": 7, "add": 6, "store": 12}

NUM_BANKS = 8
BANK_BUSY = 6
MEMORY_LATENCY = 12

# Test sizes
VECTOR_LENGTHS = [64, 150, 256, 512]
STRIDES = [1, 2, 4, 8, 16]


def main():
    print("Vector simulator: questions will be added step by step.")


if __name__ == "__main__":
    main()
