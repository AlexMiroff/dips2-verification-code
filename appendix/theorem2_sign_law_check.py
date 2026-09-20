from decimal import Decimal as D, localcontext
 
with localcontext() as ctx:
    ctx.prec = 180
    xs = list(map(D, ["1e-12", ".001", ".1", ".5",
                      ".9", ".999", ".999999999999"]))
    ps = list(map(D, [".01", ".1", ".5", ".999999",
                      "1.000001", "2", "10"]))
    failures = []
    sign = lambda a: (a > 0) - (a < 0)
    for x in xs:
        for q in ps:
            for r in ps:
                def log_m(u):
                    return (1-(r*(1-u).ln()).exp()).ln()
                gap = q*log_m(x)-log_m((q*x.ln()).exp())
                if sign(gap) != sign((q-1)*(r-1)):
                    failures.append((x, q, r))
    print(len(xs)*len(ps)**2, len(failures))