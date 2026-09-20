"""Separate grammar audit for System 2; does not replace the frozen main table."""
from pathlib import Path
import csv, json
import numpy as np
from scipy.optimize import least_squares

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'paper22_milestone1'/'outputs'/'SYSTEM_2_KNOWN_FUNCTION'/'blind_observations.csv'; OUT=Path(__file__).resolve().parent/'outputs'
rows=list(csv.DictReader(DATA.open())); u=np.array([float(r['u']) for r in rows]); y=np.array([float(r['y']) for r in rows]); idx=np.arange(20,400); rho_grid=np.round(np.arange(-.9,.9001,.05),2)
tr=idx<240; va=(idx>=240)&(idx<320); te=idx>=320
def rmse(a,b): return float(np.sqrt(np.mean((a-b)**2)))
def fit(z,target):
    def residual(p): return p[0]*np.tanh(p[1]*z[:,0]+p[2]*z[:,1]+p[3])+p[4]-target
    # coefficients are fitted; no generator parameter or hidden state is passed.
    return least_squares(residual,[1.,.5,.5,0.,0.],max_nfev=5000).x
choices=[]
for rho in rho_grid:
    m=np.zeros(400)
    for t in range(399): m[t+1]=rho*m[t]+u[t]
    z=np.column_stack([u[idx],m[idx]]); p=fit(z[tr],y[idx][tr]); pred=p[0]*np.tanh(p[1]*z[va,0]+p[2]*z[va,1]+p[3])+p[4]
    choices.append((rmse(y[idx][va],pred),rho,p,z))
vr,rho,p,z=min(choices,key=lambda q:q[0]); test=p[0]*np.tanh(p[1]*z[te,0]+p[2]*z[te,1]+p[3])+p[4]; result={'status':'EXPLORATORY_GRAMMAR_AUDIT_NOT_MAIN_COMPARISON','family':'a*tanh(b*u+c*m_hat+d)+e','rho_selected_on_validation':float(rho),'parameters_fitted_on_training':[float(x) for x in p],'validation_rmse':vr,'locked_test_rmse':rmse(y[idx][te],test),'error_tolerance':.06,'error_gate_pass':rmse(y[idx][te],test)<=.06,'uses_ground_truth_file':False,'uses_quantum':False}
# Stability audit: keep the rho selected above fixed, refit the same grammar on
# a later contiguous training window, and compare the two non-overlapping
# 80-point evaluation errors.  It is an audit, never a re-selection step.
late=(idx>=100)&(idx<320); late_eval=idx>=320
p_late=fit(z[late],y[idx][late]); late_pred=p_late[0]*np.tanh(p_late[1]*z[late_eval,0]+p_late[2]*z[late_eval,1]+p_late[3])+p_late[4]
late_rmse=rmse(y[idx][late_eval],late_pred)
result['stability_windows']={'early_train_20_239_eval_240_319_rmse':vr,'late_train_100_319_eval_320_399_rmse':late_rmse,'absolute_change':abs(vr-late_rmse),'allowable_change':.2*.06,'stability_gate_pass':abs(vr-late_rmse)<=.2*.06}
(OUT/'SYSTEM2_GRAMMAR_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(OUT/'SYSTEM2_GRAMMAR_DIAGNOSTIC.md').write_text('# System 2 — grammar diagnostic\n\nThis is a separately labelled exploratory audit and does not replace the frozen polynomial-ridge main comparison.\n\n'+ '\n'.join(f'- **{k}**: `{v}`' for k,v in result.items()),encoding='utf-8')
