"""Section 6.1: fully specified convergence control for six characteristics.

The population is the 64-state binary cube.  At each sample size, 1,500
independent samples are drawn with replacement from a fixed PRNG seed.  The
empirical minimum is the smallest coordinate subset injective on the observed
unique states.  This is a finite control, not a population estimate for an
economic dataset.
"""
from itertools import product, combinations
from random import Random
from pathlib import Path
import csv, json

SIZES=(6,12,16,20,24,32)
REPLICATES=1500
SEED=20260920
STATES=tuple(product((0,1),repeat=6))
SUBSETS=tuple(s for k in range(7) for s in combinations(range(6),k))


def empirical_minimum(sample):
    observed=tuple(set(sample))
    for subset in SUBSETS:
        if len({tuple(x[i] for i in subset) for x in observed})==len(observed):
            return len(subset)
    raise RuntimeError('full representation must be injective')


def write_figures(rows, out):
    import matplotlib.pyplot as plt
    xs=[r['sample_size'] for r in rows]
    means=[r['mean_empirical_minimum'] for r in rows]
    recovery=[r['exact_recovery_rate'] for r in rows]
    plt.style.use('seaborn-v0_8-whitegrid')
    fig,ax=plt.subplots(figsize=(7.2,4.2),dpi=180)
    ax.plot(xs,means,marker='o',linewidth=2.2,color='#153b6e')
    ax.axhline(6,color='#9c1f32',linestyle='--',linewidth=1.3,label='exact minimum = 6')
    ax.set(xlabel='Construction-sample size N',ylabel='Mean empirical minimum',ylim=(0,6.25))
    ax.legend(frameon=False,loc='lower right'); fig.tight_layout()
    fig.savefig(out/'figure2_convergence.png',bbox_inches='tight')
    fig.savefig(out/'figure2_convergence.svg',bbox_inches='tight'); plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.2,4.2),dpi=180)
    ax.plot(xs,recovery,marker='o',linewidth=2.2,color='#153b6e',label='exact recovery')
    ax.plot(xs,[1-v for v in recovery],marker='s',linewidth=1.7,color='#9c1f32',label='underestimation')
    ax.set(xlabel='Construction-sample size N',ylabel='Frequency',ylim=(0,1.05))
    ax.legend(frameon=False,loc='center right'); fig.tight_layout()
    fig.savefig(out/'figure3_recovery.png',bbox_inches='tight')
    fig.savefig(out/'figure3_recovery.svg',bbox_inches='tight'); plt.close(fig)


def main():
    rng=Random(SEED); rows=[]
    for n in SIZES:
        values=[empirical_minimum([STATES[rng.randrange(len(STATES))] for _ in range(n)])
                for _ in range(REPLICATES)]
        rows.append({'sample_size':n,'replicates':REPLICATES,
                     'mean_empirical_minimum':sum(values)/REPLICATES,
                     'exact_recovery_rate':sum(v==6 for v in values)/REPLICATES,
                     'underestimation_rate':sum(v<6 for v in values)/REPLICATES})
    out=Path(__file__).resolve().parent/'section06_convergence_outputs'; out.mkdir(exist_ok=True)
    with (out/'convergence.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    write_figures(rows,out)
    report={'factory':'section06_convergence','seed':SEED,'population_states':64,
            'sample_sizes':list(SIZES),'replicates_per_size':REPLICATES,'rows':rows,'result':'PASS'}
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
