import sys, json, os
import pandas as pd
import numpy as np
import high_confidence_search as hc
import opening_consensus_search as oc

# These two configurations are frozen from the prior robustness search.
# No parameters are chosen using the labels in this script.
A={"slip_bps":1.0,"max_stop_pct":0.012,"confirm_min":60,"drive_atr":0.2,"vwap_dist_atr":0,"ema_dist_atr":0,"gap_min":0,"pm_start":420,"pm_min":0.002,"daily_dist":0,"min_active":6,"vote_margin":5,"agreement":0.75,"direction":"both","entry_mode":"next","wait_bars":6,"pullback_ref":"ema9","touch_atr":0,"entry_cutoff":690,"stop_mode":"opening","stop_atr":1.25,"buffer_atr":0.2,"swing_bars":3,"target_R":0.75,"time_exit":840}
B={"slip_bps":1.0,"max_stop_pct":0.012,"confirm_min":45,"drive_atr":0.8,"vwap_dist_atr":0.2,"ema_dist_atr":0.2,"gap_min":0.0025,"pm_start":480,"pm_min":0.002,"daily_dist":0,"min_active":5,"vote_margin":5,"agreement":0.75,"direction":"both","entry_mode":"next","wait_bars":6,"pullback_ref":"ema9","touch_atr":0.3,"entry_cutoff":690,"stop_mode":"opening","stop_atr":1.5,"buffer_atr":0,"swing_bars":3,"target_R":0.75,"time_exit":840}

def ledger(days,p,label,y0,y1):
    rows=[]
    for day in days:
        if y0<=day[0].year<=y1:
            x=oc.trade(day,p)
            if x:
                x=dict(x);x['model']=label;rows.append(x)
    return pd.DataFrame(rows)

def metrics(df):
    if df is None or len(df)==0:return {'n':0,'win':None,'avgR':None,'pf':None,'totalR':0,'maxddR':None}
    r=df.R.to_numpy(float); pos=r[r>0].sum();neg=-r[r<0].sum();eq=np.cumsum(r);dd=eq-np.maximum.accumulate(eq)
    return {'n':int(len(r)),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pos/neg if neg>0 else 999),'totalR':float(r.sum()),'maxddR':float(dd.min())}

def combine(la,lb,mode):
    # One trade per date. Same-direction overlap can be required or prioritized.
    if len(la)==0 and len(lb)==0:return pd.DataFrame()
    aa={str(r.date):r for r in la.itertuples(index=False)};bb={str(r.date):r for r in lb.itertuples(index=False)}
    out=[]
    for d in sorted(set(aa)|set(bb)):
        a=aa.get(d);b=bb.get(d)
        if mode=='overlap':
            if a is None or b is None or a.dir!=b.dir:continue
            chosen=a
            rec=chosen._asdict();rec['model']='A+B_overlap';rec['R']=(a.R+b.R)/2
            out.append(rec);continue
        if a is not None and b is not None:
            if a.dir!=b.dir:continue # conflicting evidence -> no trade
            # If both fire same direction, use the earlier signal's realized trade (or A on tie).
            chosen=a if str(a.entry_ts)<=str(b.entry_ts) else b
            rec=chosen._asdict();rec['model']='A+B_union_agree';rec['agreement_count']=2;out.append(rec)
        else:
            chosen=a if a is not None else b
            rec=chosen._asdict();rec['model']='A+B_union';rec['agreement_count']=1;out.append(rec)
    return pd.DataFrame(out)

def sim(df,rf):
    b=200.;pk=b;dd=0.
    for r in (df.R if len(df) else []):
        b=max(0,b*(1+rf*r));pk=max(pk,b);dd=min(dd,b/pk-1)
    return {'end':b,'maxdd_pct':dd*100}

def run(path,y0,y1,prefix):
    days=hc.prep(hc.load(path));la=ledger(days,A,'A',y0,y1);lb=ledger(days,B,'B',y0,y1)
    u=combine(la,lb,'union');ov=combine(la,lb,'overlap')
    print(prefix,'A',json.dumps(metrics(la)));print(prefix,'B',json.dumps(metrics(lb)))
    print(prefix,'UNION',json.dumps(metrics(u)),json.dumps(sim(u,.02)))
    print(prefix,'OVERLAP',json.dumps(metrics(ov)),json.dumps(sim(ov,.02)))
    if prefix=='HOLDOUT_2026':
        os.makedirs('ensemble_results',exist_ok=True);la.to_csv('ensemble_results/A_2026.csv',index=False);lb.to_csv('ensemble_results/B_2026.csv',index=False);u.to_csv('ensemble_results/union_2026.csv',index=False);ov.to_csv('ensemble_results/overlap_2026.csv',index=False)
        if len(u):
            print('UNION_TRADES',json.dumps(u[['date','R','dir','model','entry_ts','exit_ts']].astype(str).to_dict('records')))
        if len(ov): print('OVERLAP_TRADES',json.dumps(ov[['date','R','dir','model','entry_ts','exit_ts']].astype(str).to_dict('records')))
    return days

def yearly(path):
    days=hc.prep(hc.load(path))
    for y in range(2019,2026):
        la=ledger(days,A,'A',y,y);lb=ledger(days,B,'B',y,y);u=combine(la,lb,'union');ov=combine(la,lb,'overlap')
        print('YEAR',y,'UNION',json.dumps(metrics(u)),'OVERLAP',json.dumps(metrics(ov)))

if __name__=='__main__':
    yearly(sys.argv[1]);run(sys.argv[1],2019,2025,'FULL_2019_25');run(sys.argv[2],2026,2026,'HOLDOUT_2026')