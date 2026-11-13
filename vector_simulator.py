"""Vector processor simulator for CECS 530 Assignment 4.

Standard library only. Questions are added one at a time:
    Q1 vector operations and strip mining
    Q2 memory bank simulation
    Q3 DAXPY execution time
"""

import random

# Machine parameters (from the assignment and lecture)
MVL = 64

STARTUP = {"load": 12, "mul": 7, "add": 6, "store": 12}

NUM_BANKS = 8
BANK_BUSY = 6
MEMORY_LATENCY = 12

# Test sizes
VECTOR_LENGTHS = [64, 150, 256, 512]
STRIDES = [1, 2, 4, 8, 16]

RANDOM_SEED = 530


# ---------------------------------------------------------------------------
# Question 1a: vector operations
# ---------------------------------------------------------------------------

def check_operands(*vectors):
    """Check that all vectors have the same length and fit in one vector."""
    lengths = {len(v) for v in vectors}
    if len(lengths) != 1:
        raise ValueError(f"vector lengths differ: {sorted(lengths)}")
    length = lengths.pop()
    if length > MVL:
        raise ValueError(f"length {length} is larger than MVL {MVL}; use strip mining")


def vadd(a, b):
    """Vector add: c[i] = a[i] + b[i]."""
    check_operands(a, b)
    return [x + y for x, y in zip(a, b)]


def vmul(a, b):
    """Vector multiply: c[i] = a[i] * b[i]."""
    check_operands(a, b)
    return [x * y for x, y in zip(a, b)]


def vscalar_mul(s, a):
    """Vector-scalar multiply: c[i] = s * a[i]."""
    check_operands(a)
    return [s * x for x in a]


# Scalar versions: one element per loop step. Used as the expected answer.

def scalar_add(a, b):
    result = []
    for i in range(len(a)):
        result.append(a[i] + b[i])
    return result


def scalar_mul(a, b):
    result = []
    for i in range(len(a)):
        result.append(a[i] * b[i])
    return result


def scalar_scalar_mul(s, a):
    result = []
    for i in range(len(a)):
        result.append(s * a[i])
    return result


def make_vector(length, seed):
    """Random whole-number vector. Same seed gives the same vector."""
    rng = random.Random(seed)
    return [float(rng.randint(-100, 100)) for _ in range(length)]


def run_case(name, a, b, s):
    """Run the three vector operations on one input and compare with scalar code."""
    add = vadd(a, b)
    mul = vmul(a, b)
    smul = vscalar_mul(s, a)
    passed = (
        add == scalar_add(a, b)
        and mul == scalar_mul(a, b)
        and smul == scalar_scalar_mul(s, a)
    )
    return {"name": name, "a": a, "b": b, "s": s,
            "add": add, "mul": mul, "smul": smul, "passed": passed}


def too_long_message():
    """Try a vector longer than MVL and return the error message."""
    try:
        vadd([0] * (MVL + 1), [0] * (MVL + 1))
    except ValueError as error:
        return str(error)
    return "no error raised"


def question_1a():
    """Test the vector operations on different inputs."""
    cases = [
        ("Hand-checkable", [1, 2, 3, 4], [10, 20, 30, 40], 3),
        ("Negatives and zeros", [-5, 0, 7, -2], [3, 0, -7, 4], -2),
        ("Fractions", [0.5, 1.5, 2.5], [2.0, 4.0, 8.0], 0.25),
        ("Random, 64 elements (seeds 1, 2)", make_vector(64, 1), make_vector(64, 2), 5),
        ("Random, 64 elements (seeds 3, 4)", make_vector(64, 3), make_vector(64, 4), -7),
    ]
    return [run_case(*case) for case in cases], too_long_message()


def format_vector(v, limit=6):
    """Show a vector; long vectors are cut after `limit` elements."""
    if len(v) <= limit:
        return str(v)
    shown = ", ".join(str(x) for x in v[:limit])
    return f"[{shown}, ...] ({len(v)} elements)"


def print_question_1a(results, too_long):
    print("=" * 60)
    print("Question 1a: vector operations")
    print("=" * 60)
    for number, r in enumerate(results, start=1):
        print(f"\nCase {number}: {r['name']}")
        print(f"  A            = {format_vector(r['a'])}")
        print(f"  B            = {format_vector(r['b'])}")
        print(f"  s            = {r['s']}")
        print(f"  vadd         = {format_vector(r['add'])}")
        print(f"  vmul         = {format_vector(r['mul'])}")
        print(f"  vscalar_mul  = {format_vector(r['smul'])}")
        print(f"  Matches scalar code: {'yes' if r['passed'] else 'NO'}")
    print(f"\nVector longer than MVL is rejected: {too_long}")
    all_passed = all(r["passed"] for r in results)
    print(f"All cases correct: {'yes' if all_passed else 'NO'}")


def main():
    results, too_long = question_1a()
    print_question_1a(results, too_long)


if __name__ == "__main__":
    main()
