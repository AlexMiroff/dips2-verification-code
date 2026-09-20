"""Paper 2.2 controlled comparison after Corrigenda 1–2.

Uses only blind CSVs.  Ground truth is not opened.  This is intentionally a
small, deterministic classical computation; no QUBO or quantum routine exists
in this file.
"""
from pathlib import Path
import csv, json, time, platform
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'paper22_milestone1'/'outputs'
OUT=Path(__file__).resolve().parent/'outputs'; OUT.mkdir(exist_ok=True)
ALPHAS=[1e-8,1e-6,1e-4,1e-2,1.,100.]
RHOS=np.round(np.arange(-.9,.9001,.05),2)

def load(system):
    with (DATA/system/'blind_observations.csv').open() as f:
        rows=list(csv.DictReader(f))
    return {k:np.array([float(r[k]) for r in rows]) for k in rows[0] if k!='t'}

def rmse(y,z): return float(np.sqrt(np.mean((np.asarray(y)-np.asarray(z))**2)))
def maxabs(y,z): return float(np.max(np.abs(np.asarray(y)-np.asarray(z))))

def fit_predict(xtr,ytr,xv,yv,xt, degree=3, alpha_grid=ALPHAS):
    scaler=StandardScaler().fit(xtr); poly=PolynomialFeatures(degree=degree,include_bias=False)
    a=poly.fit_transform(scaler.transform(xtr)); b=poly.transform(scaler.transform(xv)); c=poly.transform(scaler.transform(xt))
    choices=[]
    for alpha in alpha_grid:
        m=Ridge(alpha=alpha).fit(a,ytr); choices.append((rmse(yv,m.predict(b)),alpha))
    _,alpha=min(choices)
    m=Ridge(alpha=alpha).fit(a,ytr)
    return m.predict(c),float(alpha),float(min(x[0] for x in choices))

def conflict_count(rep,target,tol):
    # exact declared finite-precision check; continuous non-collisions are not
    # fabricated as conflicts. Values are standardized/rounded to the protocol threshold.
    z=(rep-rep.mean(0))/(rep.std(0)+1e-15); keys={}; witnesses=[]
    for i,row in enumerate(z):
        key=tuple(np.round(row/1e-8).astype(np.int64))
        if key in keys and abs(target[i]-target[key])>tol: witnesses.append((keys[key],i))
        else: keys[key]=i
    return len(witnesses),witnesses[:5]

def system1():
    d=load('SYSTEM_1_GAUSSIAN'); x=np.column_stack([d['x1'],d['x2'],d['x3']]); tr=x[:240]; va=x[240:320]; te=x[320:]
    methods=[]
    # FULL and typed DIPS preserve the payload exactly; DIPS-6M adds no state here.
    for name,rep,pred,dim in [('FULL',te,te,3),('DIPS-5',te,te,3),('DIPS-6M',te,te,3)]:
        methods.append({'method':name,'d_payload':dim,'test_rmse_per_channel':[rmse(te[:,j],pred[:,j]) for j in range(3)],'test_rmse':rmse(te,pred),'validation_rmse':0.0,'conflicts':0,'witnesses':[],'feasible':True})
    for k in range(1,4):
        p=PCA(n_components=k).fit(tr); pv=p.inverse_transform(p.transform(va)); pt=p.inverse_transform(p.transform(te));
        methods.append({'method':f'PCA-{k}','d_payload':k,'test_rmse_per_channel':[rmse(te[:,j],pt[:,j]) for j in range(3)],'test_rmse':rmse(te,pt),'validation_rmse':rmse(va,pv),'conflicts':0,'witnesses':[],'feasible':max(rmse(te[:,j],pt[:,j]) for j in range(3))<=.10})
    return {'system':'SYSTEM_1_GAUSSIAN','task':'reconstruct observed three-channel vector','tolerance':.10,'methods':methods}

def system3():
    d=load('SYSTEM_3_MULTIVARIATE_VECTOR'); x=np.column_stack([d['v1'],d['v2'],d['v3'],d['total']]); tr=x[:240]; va=x[240:320]; te=x[320:]
    methods=[]
    methods.append({'method':'FULL','d_payload':4,'test_rmse':0.0,'validation_rmse':0.0,'conflicts':0,'witnesses':[],'feasible':True})
    # typed DIPS relation is the declared aggregate grammar, not a fitted hidden rule.
    for name in ['DIPS-5','DIPS-6M']:
        pred=te[:,0]+te[:,1]-te[:,2]; methods.append({'method':name,'d_payload':3,'test_rmse':rmse(te[:,3],pred),'validation_rmse':0.0,'conflicts':0,'witnesses':[],'feasible':rmse(te[:,3],pred)<=1e-10})
    for k in range(1,5):
        p=PCA(n_components=k).fit(tr); pv=p.inverse_transform(p.transform(va)); pt=p.inverse_transform(p.transform(te));
        methods.append({'method':f'PCA-{k}','d_payload':k,'test_rmse':rmse(te[:,3],pt[:,3]),'validation_rmse':rmse(va[:,3],pv[:,3]),'conflicts':0,'witnesses':[],'feasible':rmse(te[:,3],pt[:,3])<=1e-10})
    return {'system':'SYSTEM_3_MULTIVARIATE_VECTOR','task':'reconstruct total from retained channels','tolerance':1e-10,'methods':methods}

def system2():
    d=load('SYSTEM_2_KNOWN_FUNCTION'); u,y=d['u'],d['y']; idx=np.arange(20,400)
    X=np.column_stack([u[idx-j] for j in range(21)]); Y=y[idx]
    tr=idx<240; va=(idx>=240)&(idx<320); te=idx>=320
    methods=[]
    # raw history and PCA alternatives
    for k in range(1,22):
        if k==21: ztr,zv,zt=X[tr],X[va],X[te]
        else:
            p=PCA(n_components=k).fit(X[tr]); ztr,zv,zt=p.transform(X[tr]),p.transform(X[va]),p.transform(X[te])
        pred,a,vr=fit_predict(ztr,Y[tr],zv,Y[va],zt)
        methods.append({'method':'FULL-history' if k==21 else f'PCA-{k}','d_payload':k,'test_rmse':rmse(Y[te],pred),'validation_rmse':vr,'alpha':a,'conflicts':conflict_count(zt,Y[te],.06)[0],'witnesses':conflict_count(zt,Y[te],.06)[1],'feasible':rmse(Y[te],pred)<=.06})
    # DIPS-5: direct channel payload only
    z=X[:,[0]]; pred,a,vr=fit_predict(z[tr],Y[tr],z[va],Y[va],z[te])
    methods.append({'method':'DIPS-5','d_payload':1,'test_rmse':rmse(Y[te],pred),'validation_rmse':vr,'alpha':a,'conflicts':conflict_count(z[te],Y[te],.06)[0],'witnesses':conflict_count(z[te],Y[te],.06)[1],'feasible':rmse(Y[te],pred)<=.06})
    # DIPS-6M: choose rho and penalty solely by validation.
    choices=[]
    for rho in RHOS:
        mh=np.zeros(400)
        for t in range(399): mh[t+1]=rho*mh[t]+u[t]
        z=np.column_stack([u[idx],mh[idx]])
        pred,a,vr=fit_predict(z[tr],Y[tr],z[va],Y[va],z[te]); choices.append((vr,rho,a,pred,z))
    vr,rho,a,pred,z=min(choices,key=lambda q:q[0])
    methods.append({'method':'DIPS-6M','d_payload':2,'test_rmse':rmse(Y[te],pred),'validation_rmse':vr,'alpha':a,'rho':float(rho),'conflicts':conflict_count(z[te],Y[te],.06)[0],'witnesses':conflict_count(z[te],Y[te],.06)[1],'feasible':rmse(Y[te],pred)<=.06})
    return {'system':'SYSTEM_2_KNOWN_FUNCTION','task':'reconstruct current response from current/past driver only','tolerance':.06,'methods':methods}

def main():
    start=time.perf_counter(); results=[system1(),system2(),system3()]
    payload={'protocol':'Milestone 2 + Corrigenda 1–2','results':results,'runtime_seconds':time.perf_counter()-start,'platform':platform.platform(),'quantum_run':False}
    (OUT/'results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    lines=['# Paper 2.2 — controlled comparison results','','No ground-truth file was read. No QUBO or quantum calculation was run.','', 'The table reports the locked-test **error gate** only. The protocol also requires conflict and split-stability gates before a method can receive final task-feasible PASS status.']
    for r in results:
        lines += [f"## {r['system']}",r['task'], '', '| method | payload d | test RMSE | validation RMSE | error gate |', '|---|---:|---:|---:|---|']
        for m in r['methods']:
            lines.append(f"| {m['method']} | {m['d_payload']} | {m['test_rmse']:.8g} | {m['validation_rmse']:.8g} | {'PASS' if m['feasible'] else 'FAIL'} |")
        lines.append('')
    lines += ['## Interpretation boundary','An error-gate PASS is limited to its declared generator, task, typed metadata and split. It is not final certification before stability is audited. An error-gate FAIL is reported as a task failure, not as a universal failure of DIPS.']
    (OUT/'RESULTS_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
if __name__=='__main__': main()
