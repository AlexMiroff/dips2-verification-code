"""Section 12.6: exact convolution, composition and shared-path checks."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from common import det, eye, add, scale, check


def recurrence(a, x):
    y=[]; state=F(0)
    for v in x:
        state = a*state+v; y.append(state)
    return y


def convolution(a, x):
    return [sum((a**(t-k)*x[k] for k in range(t+1)), F(0)) for t in range(len(x))]


def main():
    checks={"memory_recursion":0,"series_parallel":0,"feedback":0,"shared_path":0}
    for i in range(32):
        a=F((i%7)-3, 10); x=[F((i+t)%5-2, 7) for t in range(8)]
        check(recurrence(a,x)==convolution(a,x), "memory convolution")
        checks["memory_recursion"]+=1
    for i in range(40):
        a,b=F(i%5,9),F((2*i)%5,11); x=[F(t+1,13) for t in range(9)]
        serial=recurrence(b,recurrence(a,x))
        direct=[sum((b**(t-j)*a**(j-k)*x[k]
                     for j in range(t+1) for k in range(j+1)), F(0))
                for t in range(9)]
        check(serial==direct,"series composition")
        checks["series_parallel"]+=1
    for i in range(40):
        a=F(i%4,10); x=[F((2*t+i)%7-3,11) for t in range(10)]
        y=recurrence(a,x)
        check(all(y[t] == (a*y[t-1] if t else 0)+x[t] for t in range(10)),"feedback recurrence")
        checks["feedback"]+=1
    determinant_evaluations=0
    for gates in product(range(9), repeat=2):
        weight=1 + gates[0] + gates[1]
        # Two common paths agree whether evaluated as route sum or return kernel.
        route=sum(F(g*weight,17) for g in gates)
        kernel=F(weight,17)*sum(gates)
        check(route==kernel,"shared path")
        for z in (F(-2),F(-1),F(0),F(1),F(2),F(3),F(5),F(7)):
            a=[[F(0),route],[F(0),F(0)]]
            check(det(add(scale(z,eye(2)),scale(F(-1),a)))==z*z,"shared-path determinant")
            determinant_evaluations+=1
        checks["shared_path"]+=1
    report={"factory":"section12_channel_path", **checks,
            "exact_determinant_evaluations":determinant_evaluations, "result":"PASS"}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
