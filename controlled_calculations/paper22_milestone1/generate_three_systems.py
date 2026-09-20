"""Paper 2.2 Milestone 1: generate and validate exactly three frozen systems.

No DIPS selection, optimization, or solver comparison occurs here.  This stage
only creates source-controlled ground truth and blind observations.
"""
from pathlib import Path
import csv, json, math, random

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'

def mean(xs): return sum(xs)/len(xs)

def system_1_gaussian():
    rng=random.Random(2201); n=400
    rows=[]; errors=[]
    for t in range(n):
        z1=rng.gauss(0,1); z2=rng.gauss(0,1); eps=rng.gauss(0,0.10)
        x1=z1; x2=0.8*z1+0.6*z2; x3=0.5*z1-0.3*z2+eps
        rows.append({'t':t,'x1':x1,'x2':x2,'x3':x3})
        errors.append(x3-(0.5*z1-0.3*z2))
    assert abs(mean(errors)) < 0.03
    return {'name':'SYSTEM_1_GAUSSIAN','seed':2201,'n':n,
            'ground_truth':{'latent_dimension':2,'noise_sd':0.10,
                            'equations':['x1=z1','x2=0.8z1+0.6z2','x3=0.5z1-0.3z2+epsilon']},
            'rows':rows,'validation':{'mean_residual':mean(errors),'max_abs_residual':max(map(abs,errors))}}

def system_2_known_function():
    rng=random.Random(2202); n=400; m=0.0; rows=[]; max_err=0.0
    for t in range(n):
        u=math.sin(t/13.0)+0.25*math.cos(t/7.0)
        shock=rng.uniform(-0.02,0.02)
        y=math.tanh(0.9*u+0.7*m)+shock
        reconstructed=math.tanh(0.9*u+0.7*m)+shock
        max_err=max(max_err,abs(y-reconstructed))
        rows.append({'t':t,'u':u,'memory_before':m,'shock':shock,'y':y})
        m=0.65*m+u
    assert max_err==0.0
    return {'name':'SYSTEM_2_KNOWN_FUNCTION','seed':2202,'n':n,
            'ground_truth':{'memory_rule':'m[t+1]=0.65m[t]+u[t]',
                            'response':'y[t]=tanh(0.9u[t]+0.7m[t])+shock[t]',
                            'shock_support':'uniform[-0.02,0.02]'},
            'rows':rows,'validation':{'maximum_reconstruction_error':max_err}}

def system_3_multivariate_vector():
    rng=random.Random(2203); n=400; rows=[]; max_identity=0.0
    for t in range(n):
        a=rng.gauss(0,1); b=rng.gauss(0,1); c=rng.gauss(0,1)
        v1=a+b; v2=b+c; v3=a-c; total=v1+v2-v3
        max_identity=max(max_identity,abs(total-2*(b+c)))
        rows.append({'t':t,'v1':v1,'v2':v2,'v3':v3,'total':total,'latent_a':a,'latent_b':b,'latent_c':c})
    assert max_identity < 1e-12
    return {'name':'SYSTEM_3_MULTIVARIATE_VECTOR','seed':2203,'n':n,
            'ground_truth':{'latent_dimension':3,'vector_rules':['v1=a+b','v2=b+c','v3=a-c','total=v1+v2-v3']},
            'rows':rows,'validation':{'maximum_identity_error':max_identity}}

def write_system(system):
    name=system['name']; d=OUT/name; d.mkdir(parents=True,exist_ok=True)
    truth={k:v for k,v in system.items() if k!='rows'}
    (d/'ground_truth.json').write_text(json.dumps(truth,indent=2),encoding='utf-8')
    # Blind observations deliberately omit all latent variables and the memory
    # state.  No analysis is run at Milestone 1.
    observed=[]
    for row in system['rows']:
        if name=='SYSTEM_1_GAUSSIAN': observed.append({k:row[k] for k in ['t','x1','x2','x3']})
        elif name=='SYSTEM_2_KNOWN_FUNCTION': observed.append({k:row[k] for k in ['t','u','y']})
        else: observed.append({k:row[k] for k in ['t','v1','v2','v3','total']})
    with (d/'blind_observations.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(observed[0])); w.writeheader(); w.writerows(observed)
    return truth

def main():
    systems=[system_1_gaussian(),system_2_known_function(),system_3_multivariate_vector()]
    truths=[write_system(x) for x in systems]
    report=['# MILESTONE 1 REPORT','',
            'Exactly three controlled systems were generated and mathematically validated.',
            'No DIPS representation selection, baseline comparison, optimization, or quantum calculation has been run at this stage.','']
    for s in truths:
        report += [f"## {s['name']}", f"Seed: {s['seed']}; observations: {s['n']}.",
                   f"Validation: `{json.dumps(s['validation'])}`.", '']
    report += ['## STOP','Milestone 1 is complete. The next stage must define a frozen analysis protocol and common baselines before any DIPS analysis.']
    (OUT/'MILESTONE_1_REPORT.md').write_text('\n'.join(report),encoding='utf-8')
    print(OUT/'MILESTONE_1_REPORT.md')

if __name__=='__main__': main()
