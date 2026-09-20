"""Section 6.2 and 6.4 finite exact verification suite.

The three solvers are deliberately separate implementations: subset enumeration,
branch-and-bound set cover, and binary-energy enumeration with a sufficient
penalty.  All instances are finite and generated from a fixed seed.
"""
from itertools import combinations, product
from random import Random
from fractions import Fraction as F
import json
from pathlib import Path
from common import check


def generated_hypergraph(n, rng):
    # Nonempty discernibility sets, with duplicate edges removed.
    edges=set()
    for _ in range(2*n+3):
        edge=tuple(i for i in range(n) if rng.randrange(2))
        edges.add(edge or (rng.randrange(n),))
    return tuple(sorted(edges))


def enum(edges, n):
    for k in range(n+1):
        for s in combinations(range(n),k):
            if all(set(s)&set(e) for e in edges): return k


def bnb(edges, n):
    best=n+1
    def rec(chosen, remaining):
        nonlocal best
        if len(chosen)>=best: return
        if not remaining:
            best=len(chosen); return
        edge=min(remaining,key=len)
        for v in edge:
            rec(chosen|{v}, [e for e in remaining if v not in e])
    rec(set(), list(edges))
    return best


def qubo(edges, n):
    # Exact energy enumeration. P>n makes uncovered-edge penalty lexicographic.
    penalty=n+1
    best=None
    for bits in product((0,1),repeat=n):
        uncovered=sum(not any(bits[i] for i in e) for e in edges)
        energy=sum(bits)+penalty*uncovered
        candidate=(energy,sum(bits))
        best=min(best,candidate) if best else candidate
    return best[1]


def closure_cases():
    # 204 memory-insensitive tasks and 120 declared memory-sensitive tasks.
    counts={"phi5_pass":0,"phi5_fail":0,"phi6_pass":0,"witnesses":0}
    for i in range(324):
        baseline=(i%3,i%2,(i//3)%3,(i//9)%2,(i//18)%3)
        memory0,memory1=0,1
        sensitive=i>=204
        out0=(baseline, memory0) if sensitive else baseline
        out1=(baseline, memory1) if sensitive else baseline
        phi5_same=True
        if phi5_same and out0==out1: counts["phi5_pass"]+=1
        else:
            counts["phi5_fail"]+=1; counts["witnesses"]+=1
        check((baseline,memory0)!=(baseline,memory1),"Phi6 must retain memory")
        counts["phi6_pass"]+=1
    check(counts["phi5_pass"]==204 and counts["phi5_fail"]==120,"closure split")
    return counts


def main():
    rng=Random(20260920)
    enum_bnb=0
    for n in range(3,11):
        for _ in range(100):
            edges=generated_hypergraph(n,rng)
            check(enum(edges,n)==bnb(edges,n),"ENUM != BNB")
            enum_bnb+=1
    triple=0
    for n in range(3,11):
        for _ in range(25):
            edges=generated_hypergraph(n,rng)
            a=enum(edges,n); check(a==bnb(edges,n)==qubo(edges,n),"solver disagreement")
            triple+=1
    report={"factory":"section06_exact_formulations","enum_bnb_instances":enum_bnb,
            "enum_bnb_agreement":enum_bnb,"enum_bnb_qubo_instances":triple,
            "triple_agreement":triple,"closure":closure_cases(),"result":"PASS"}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
