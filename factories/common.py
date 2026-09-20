"""Small exact-arithmetic helpers used by the DIPS II verification factories."""
from fractions import Fraction as F
from itertools import permutations


def det(a):
    """Exact determinant by permutation expansion; intended for small matrices."""
    n = len(a)
    total = F(0)
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inv % 2 else 1)
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def mat_vec(a, x):
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0)) for i in range(len(a))]


def check(condition, message):
    if not condition:
        raise AssertionError(message)
