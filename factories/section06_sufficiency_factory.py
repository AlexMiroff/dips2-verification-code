"""Section 6: exact finite witnesses for six essential characteristics.

This is a deliberately finite implementation check.  It does not estimate a
population parameter and does not prove the characteristic theorem.
"""
from itertools import product, combinations
import json
from pathlib import Path
from common import check


def projection(state, keep):
    return tuple(state[i] for i in keep)


def conflicts(states, keep):
    seen = {}
    out = []
    for x in states:
        key = projection(x, keep)
        target = x  # declared task: recover the full six-coordinate state
        if key in seen and seen[key][1] != target:
            out.append((seen[key][0], x))
        else:
            seen[key] = (x, target)
    return out


def main():
    states = list(product((0, 1), repeat=6))
    # Every five-coordinate projection has an explicit conflicting pair.
    witness_counts = {}
    for omitted in range(6):
        keep = tuple(i for i in range(6) if i != omitted)
        cs = conflicts(states, keep)
        check(cs, f"missing witness for coordinate {omitted}")
        witness_counts[str(omitted + 1)] = len(cs)
    # The full representation is injective on this declared dictionary.
    check(not conflicts(states, range(6)), "full representation conflicted")
    report = {
        "factory": "section06_sufficiency",
        "state_dictionary": len(states),
        "essential_characteristics": 6,
        "five_coordinate_witness_counts": witness_counts,
        "checked_subsets": sum(1 for _ in combinations(range(6), 5)),
        "result": "PASS",
        "scope": "finite binary witness only"
    }
    p = Path(__file__).with_suffix('.json')
    p.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
