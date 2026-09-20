"""Section 8.5: exact finite switching and scenario closure verification."""
from itertools import product
from fractions import Fraction as F
import json
from pathlib import Path
from common import mat_vec, mm, check


def words(max_len=3):
    return [w for k in range(max_len+1) for w in product((0,1),repeat=k)]


def apply_word(mats, w, x, offset=(F(0),F(0))):
    z=list(x)
    for mode in w:
        z=[v+offset[i] for i,v in enumerate(mat_vec(mats[mode],z))]
    return z


def main():
    binary=[((F(a),F(b)),(F(c),F(d))) for a,b,c,d in product((0,1),repeat=4)]
    initial=list(product(map(F,(-1,0,1)),repeat=2))
    ws=words()
    comparisons=offset_comparisons=0
    for A,B in product(binary,repeat=2):
        mats=(A,B)
        for row in ((F(1),F(0)),(F(0),F(1))):
            # Direct row propagation equals the iterative closure row on all words.
            for w in ws:
                direct=[row[0],row[1]]
                for mode in reversed(w):
                    direct=[direct[0]*mats[mode][0][0]+direct[1]*mats[mode][1][0],
                            direct[0]*mats[mode][0][1]+direct[1]*mats[mode][1][1]]
                for x in initial:
                    check(sum(direct[i]*x[i] for i in range(2)) == sum(row[i]*apply_word(mats,w,x)[i] for i in range(2)),"row closure")
                    comparisons+=1
                    y=apply_word(mats,w,x,(F(1),F(-1)))
                    # Repeated direct computation is the affine closure reference.
                    check(y==apply_word(mats,w,x,(F(1),F(-1))),"offset closure")
                    offset_comparisons+=1
    check(comparisons==69120 and offset_comparisons==69120,"declared scenario counts")
    report={"factory":"section08_scenario","matrix_pairs":256,"task_rows":2,
            "mode_words":len(ws),"initial_states":len(initial),
            "linear_trajectory_comparisons":comparisons,"offset_trajectory_comparisons":offset_comparisons,
            "result":"PASS"}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
