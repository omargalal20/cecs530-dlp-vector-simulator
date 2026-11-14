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


# ---------------------------------------------------------------------------
# Question 1b: strip mining
# ---------------------------------------------------------------------------

def strip_mine(n, mvl=MVL):
    """Split n elements into strips of at most mvl: a list of (start, length).

    Same rule as the lecture's setvl: VL = min(MVL, remaining elements).
    Full strips come first and the short strip comes last.
    """
    strips = []
    start = 0
    while start < n:
        length = min(mvl, n - start)
        strips.append((start, length))
        start += length
    return strips


def run_strip_mined(operation, *vectors, mvl=MVL):
    """Run a vector operation on vectors of any length, one strip at a time."""
    result = []
    for start, length in strip_mine(len(vectors[0]), mvl):
        pieces = [v[start:start + length] for v in vectors]
        result.extend(operation(*pieces))
    return result


def question_1b():
    """Strip mine each required length and check the results."""
    rows = []
    for n in VECTOR_LENGTHS:
        a = make_vector(n, 10 + n)
        b = make_vector(n, 20 + n)
        s = 3
        add_ok = run_strip_mined(vadd, a, b) == scalar_add(a, b)
        mul_ok = run_strip_mined(vmul, a, b) == scalar_mul(a, b)
        smul_ok = (run_strip_mined(lambda x: vscalar_mul(s, x), a)
                   == scalar_scalar_mul(s, a))
        rows.append({"n": n, "strips": strip_mine(n),
                     "passed": add_ok and mul_ok and smul_ok})
    return rows


def print_question_1b(rows):
    print("=" * 60)
    print(f"Question 1b: strip mining (MVL = {MVL})")
    print("=" * 60)
    for r in rows:
        print(f"\nn = {r['n']}: {len(r['strips'])} strip(s)")
        for number, (start, length) in enumerate(r["strips"], start=1):
            print(f"  strip {number}: elements {start}-{start + length - 1}  (VL = {length})")
        print(f"  vadd, vmul, vscalar_mul match scalar code: {'yes' if r['passed'] else 'NO'}")

    print("\nSummary")
    print(f"  {'n':>4}  {'strips':>6}  VL of each strip")
    for r in rows:
        lengths = " + ".join(str(length) for _, length in r["strips"])
        print(f"  {r['n']:>4}  {len(r['strips']):>6}  {lengths}")


# ---------------------------------------------------------------------------
# Question 1c: scalar vs vector instruction count
# ---------------------------------------------------------------------------
# Loop bodies follow the lecture's DAXPY code (RV64G scalar loop, RV64V
# strip-mined loop). "Setup" instructions run once, outside the loop.

SCALAR_SETUP = {
    "add": ["addi"],
    "mul": ["addi"],
    "scalar_mul": ["fld", "addi"],
    "daxpy": ["fld", "addi"],
}

SCALAR_LOOP = {
    "add": ["fld", "fld", "fadd.d", "fsd", "addi", "addi", "addi", "bne"],
    "mul": ["fld", "fld", "fmul.d", "fsd", "addi", "addi", "addi", "bne"],
    "scalar_mul": ["fld", "fmul.d", "fsd", "addi", "addi", "bne"],
    "daxpy": ["fld", "fmul.d", "fld", "fadd.d", "fsd", "addi", "addi", "bne"],
}

VECTOR_SETUP = {
    "add": ["vsetdcfg", "vdisable"],
    "mul": ["vsetdcfg", "vdisable"],
    "scalar_mul": ["vsetdcfg", "fld", "vdisable"],
    "daxpy": ["vsetdcfg", "fld", "vdisable"],
}

VECTOR_LOOP = {
    "add": ["setvl", "vld", "vld", "vadd", "vst", "slli", "add", "add", "add", "sub", "bnez"],
    "mul": ["setvl", "vld", "vld", "vmul", "vst", "slli", "add", "add", "add", "sub", "bnez"],
    "scalar_mul": ["setvl", "vld", "vmul", "vst", "slli", "add", "add", "sub", "bnez"],
    "daxpy": ["setvl", "vld", "slli", "add", "vmul", "vld", "vadd", "sub", "vst", "add", "bnez"],
}

OPERATIONS = ["add", "mul", "scalar_mul"]


def scalar_instruction_count(op, n):
    """Setup instructions plus the loop body once per element."""
    return len(SCALAR_SETUP[op]) + len(SCALAR_LOOP[op]) * n


def vector_instruction_count(op, n, mvl=MVL):
    """Setup instructions plus the loop body once per strip."""
    strips = len(strip_mine(n, mvl))
    return len(VECTOR_SETUP[op]) + len(VECTOR_LOOP[op]) * strips


def question_1c():
    """Count instructions for each operation and vector length."""
    rows = []
    for op in OPERATIONS:
        for n in VECTOR_LENGTHS:
            scalar = scalar_instruction_count(op, n)
            vector = vector_instruction_count(op, n)
            rows.append({"op": op, "n": n, "strips": len(strip_mine(n)),
                         "scalar": scalar, "vector": vector,
                         "ratio": scalar / vector})
    return rows


def print_question_1c(rows):
    print("=" * 60)
    print("Question 1c: scalar vs vector instruction count")
    print("=" * 60)
    print("\nInstructions counted (taken from the lecture's DAXPY code):")
    for op in OPERATIONS:
        print(f"  {op}")
        print(f"    scalar: {len(SCALAR_SETUP[op])} setup + {len(SCALAR_LOOP[op])} per element")
        print(f"    vector: {len(VECTOR_SETUP[op])} setup + {len(VECTOR_LOOP[op])} per strip")
    print("\n  Scalar count = setup + per-element x n")
    print("  Vector count = setup + per-strip x number of strips")

    print(f"\n  {'operation':<11}{'n':>5}{'strips':>8}{'scalar':>9}{'vector':>8}{'scalar/vector':>15}")
    for r in rows:
        print(f"  {r['op']:<11}{r['n']:>5}{r['strips']:>8}{r['scalar']:>9}"
              f"{r['vector']:>8}{r['ratio']:>14.1f}x")


def main():
    results, too_long = question_1a()
    print_question_1a(results, too_long)
    print()
    print_question_1b(question_1b())
    print()
    print_question_1c(question_1c())


if __name__ == "__main__":
    main()
