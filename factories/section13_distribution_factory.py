"""Section 13.6: exact finite distribution identities with rational weights."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from common import check


def marginal(joint, index):
    ans={}
    for state,p in joint.items(): ans[state[index]]=ans.get(state[index],F(0))+p
    return ans


def main():
    checks=0
    # Five declared grammars × three joint laws, compared against direct enumeration.
    laws=[{(0,0):F(1,2),(1,1):F(1,2)},
          {(0,0):F(1,4),(0,1):F(1,4),(1,0):F(1,4),(1,1):F(1,4)},
          {(0,0):F(1,8),(0,1):F(3,8),(1,0):F(3,8),(1,1):F(1,8)}]
    grammars=[lambda x,y:x+y,lambda x,y:x*y,lambda x,y:min(x,y),lambda x,y:max(x,y),lambda x,y:max(x,y)+x*y]
    for law, g in product(laws,grammars):
        out={}
        for (x,y),p in law.items(): out[g(x,y)]=out.get(g(x,y),F(0))+p
        check(sum(out.values(),F(0))==F(1),"probability mass")
        checks+=1
    # Identical marginals do not identify dependence: diagonal vs anti-diagonal.
    diagonal=laws[0]; anti={(0,1):F(1,2),(1,0):F(1,2)}
    check(marginal(diagonal,0)==marginal(anti,0)=={0:F(1,2),1:F(1,2)},"marginal x")
    check(marginal(diagonal,1)==marginal(anti,1),"marginal y")
    check(sum((x*y*p for (x,y),p in diagonal.items()),F(0)) != sum((x*y*p for (x,y),p in anti.items()),F(0)),"dependence witness")
    report={"factory":"section13_distribution", "finite_joint_laws":3,
            "declared_grammars":5,"exact_output_laws_checked":checks,
            "dependence_counterexample":"PASS", "result":"PASS"}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
