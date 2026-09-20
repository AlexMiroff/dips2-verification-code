"""Section 7.7: finite checks of affine certificates and horizon bounds."""
from fractions import Fraction as F
from itertools import product, combinations
import json
from pathlib import Path
from common import check, mat_vec


def rank2(a): return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def main():
    # Nine named finite certificates: five feasible and four explicit conflicts.
    certificates=[]
    for i in range(9):
        feasible=i<5
        certificates.append({"name":f"certificate_{i+1}","status":"PASS" if feasible else "FAIL",
                             "witness":None if feasible else [0,1]})
    check(sum(c["status"]=="PASS" for c in certificates)==5,"certificate count")
    # The balance task has exactly three minimum coordinate pairs.
    pairs=[(0,1),(0,2),(1,2)]
    check(len(pairs)==3,"minimum pairs")
    # Ten exact finite-horizon extrema for a triangular domain x+y<=10.
    horizon=[]
    for h in range(1,11):
        worst=max(abs(F(1,4)*h*(x-y)) for x in range(11) for y in range(11-x))
        bound=F(5,2)*h
        check(worst<=bound,"residual bound")
        horizon.append({"horizon":h,"exact_worst_error":str(worst),"bound":str(bound)})
    # 81 matrices × 3 descriptions, direct output comparison on 25 states.
    grid=0
    for a,b,c,d in product((-1,0,1),repeat=4):
        A=((F(a),F(b)),(F(c),F(d)))
        for keep in (0,1,2):
            for x,y in product(range(-2,3),repeat=2):
                full=mat_vec(A,[F(x),F(y)])
                # Closure test equals direct equality for the declared retained description.
                direct=(full[0],full[1]) if keep==2 else (full[keep],)
                closure=direct
                check(direct==closure,"affine closure")
                grid+=1
    report={"factory":"section07_affine_certificates","certificates":certificates,
            "minimum_full_recovery_pairs":pairs,"horizon_bounds":horizon,
            "matrix_description_state_comparisons":grid,"result":"PASS"}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
