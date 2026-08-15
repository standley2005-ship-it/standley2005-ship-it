import sys,json,os
import pandas as pd
import numpy as np
import high_confidence_search as hc
import ensemble_eval as oe
import second_wave_core as sw

GAP={"slip_bps":1.0,"max_stop_pct":0.012,"direction":"both","trend_filter":True,"target_R":0.6,"stop_atr":0,"touch_atr":0.3,"entry_cutoff":660,"ema_confirm":True,"gap_min":0.005,"gap_max":0.02,"confirm_min":45,"open_confirm":0.003}

def metrics(df):
    if df is None or len(df)==0:return {'n':0,'win':None,'avgR':None,'pf':None,'totalR':0.,'maxddR':None}
    r=df.R.to_numpy(float);pos=r[r>0].sum();neg=-r[r<0].sum();eq=np.cumsum(r);dd=eq-np.maximum.accumulate(eq)
    return {'n':int(len(r)),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pos/neg if neg>0 else 999),'totalR':float(r.sum()),'maxddR':float(dd.min())}

def sim(df,rf=.02):
    b=200.;pk=b;dd=0.
    for r in (df.R.to_numpy(float) if len(df) else []):b=max(0,b*(1+rf*r));pk=max(pk,b);dd=min(dd,b/pk-1)
    return {'end':float(b),'maxdd_pct':float(dd*100)}

def oce(days,y0,y1):return oe.combine(oe.ledger(days,oe.A,'A',y0,y1),oe.ledger(days,oe.B,'B',y0,y1),'union')
def gap(days,y0,y1):
    rows=sw.bt(days,'gap_pullback',GAP,y0,y1)
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=['date','R','dir','entry_ts','exit_ts'])

def combine(o,g):
    by={}
    for name,df in [('OCE',o),('GAP',g)]:
        if df is None or not len(df):continue
        for r in df.itertuples(index=False):by.setdefault(str(r.date),[]).append((name,r))
    out=[];conflicts=0;agreements=0;gap_only=0;oce_only=0
    for d,items in sorted(by.items()):
        dirs={int(r.dir) for _,r in items}
        if len(dirs)>1: conflicts+=1;continue
        names={n for n,_ in items}
        if names=={'OCE','GAP'}:agreements+=1
        elif names=={'GAP'}:gap_only+=1
        else:oce_only+=1
        # Use earliest valid setup if both agree; one position/day.
        n,r=sorted(items,key=lambda x:str(x[1].entry_ts))[0]
        z=r._asdict();z['sources']='+'.join(sorted(names));out.append(z)
    return pd.DataFrame(out),{'conflict_days_skipped':conflicts,'agreement_days':agreements,'gap_only_days':gap_only,'oce_only_days':oce_only}

def evaluate(days,y0,y1):
    o=oce(days,y0,y1);g=gap(days,y0,y1);p,counts=combine(o,g)
    return o,g,p,counts

def main(train_path,test_path):
    train=hc.prep(hc.load(train_path));test=hc.prep(hc.load(test_path));os.makedirs('final_portfolio_results',exist_ok=True)
    o,g,p,c=evaluate(train,2019,2025)
    o26,g26,p26,c26=evaluate(test,2026,2026)
    years=[]
    for y in range(2019,2026):
        yo,yg,yp,yc=evaluate(train,y,y);years.append({'year':y,'OCE':metrics(yo),'GAP':metrics(yg),'PORT':metrics(yp),**yc})
    # incremental unique opportunity measure
    result={
      'OCE_2019_25':metrics(o),'GAP_2019_25':metrics(g),'PORT_2019_25':metrics(p),'PORT_200_2pct':sim(p,.02),'counts_2019_25':c,
      'incremental_portfolio_trades_vs_OCE':int(len(p)-len(o)),
      'OCE_2026':metrics(o26),'GAP_2026':metrics(g26),'PORT_2026':metrics(p26),'PORT_2026_200_2pct':sim(p26,.02),'counts_2026':c26,
      'years':years,'gap_params':GAP
    }
    json.dump(result,open('final_portfolio_results/summary.json','w'),indent=2)
    p.to_csv('final_portfolio_results/portfolio_2019_25.csv',index=False);p26.to_csv('final_portfolio_results/portfolio_2026.csv',index=False)
    print('FINAL_PORTFOLIO',json.dumps(result),flush=True)

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
