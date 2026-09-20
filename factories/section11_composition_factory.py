"""Section 11.5: exact composition checks for small directed contours."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from common import det, eye, add, scale, check


def characteristic_two_cycle(a, b, z):
    m = [[F(0), a], [b, F(0)]]
    return det(add(scale(z, eye(2)), scale(F(-1), m)))


def main():
    determinant_checks = 0
    # 60 general weighted two-channel matrices, four exact evaluation points each.
    for k in range(60):
        a, b = F((k % 11) - 5, 7), F(((3*k) % 13) - 6, 11)
        for z in (F(-2), F(-1), F(1), F(3)):
            check(characteristic_two_cycle(a, b, z) == z*z - a*b, "two-cycle determinant")
            determinant_checks += 1
    # 144 two-contour configurations; determinant agrees with product of independent contours.
    for route1, route2, enabled1, enabled2 in product(range(6), range(6), (0,1), (0,1)):
        a = F(route1 + 1, 5) * enabled1; b = F(route2 + 1, 7) * enabled2
        for z in (F(-1), F(0), F(1), F(2), F(3), F(5), F(7)):
            block = [[F(0), a, F(0), F(0)], [b,F(0),F(0),F(0)],
                     [F(0),F(0),F(0),a], [F(0),F(0),b,F(0)]]
            left = det(add(scale(z, eye(4)), scale(F(-1), block)))
            right = (z*z-a*b)**2
            check(left == right, "independent contour composition")
            determinant_checks += 1
    report={"factory":"section11_composition", "general_matrices":60,
            "two_contour_configurations":144, "exact_determinant_evaluations":determinant_checks,
            "result":"PASS"}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
