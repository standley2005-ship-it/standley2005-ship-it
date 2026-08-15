import sys, json, os
import pandas as pd
import numpy as np
import high_confidence_search as hc
import opening_consensus_search as oc
import ensemble_eval as oe

# Multi-strategy research portfolio. Strategy parameters are selected using
# 2019-2025 only. 2026 is evaluated only after one configuration per family
# has been frozen. All fills inherit 1bp adverse slippage and stop-first
# same-bar ambiguity from the existing backtester.

BASE={"slip_bps":1.0,"max_stop_pct":0.012}

def metrics(rows):
    if rows is None or len(rows)==0:
        return {"n":0,"win":None,"avgR":None,"pf":None,"totalR":0.0,"maxddR":None}
    if isinstance(rows,pd.DataFrame): r=rows.R.to_numpy(float)
    else: r=np.array([x['R'] for x in rows],float)
    pos=r[r>0].sum(); neg=-r[r<0].sum(); eq=np.cumsum(r); dd=eq-np.maximum.accumulate(eq)
    return {"n":int(len(r)),"win":float((r>0).mean()),"avgR":float(r.mean()),"pf":float(pos/neg if neg>0 else 999),"totalR":float(r.sum()),"maxddR":float(dd.min())}

def sim(rows,rf=.02):
    if isinstance(rows,pd.DataFrame): rs=rows.R.to_numpy(float) if len(rows) else []
    else: rs=[x['R'] for x in rows]
    b=200.; pk=b; dd=0.
    for r in rs:
        b=max(0,b*(1+rf*r)); pk=max(pk,b); dd=min(dd,b/pk-1)
    return {"end":float(b),"maxdd_pct":float(dd*100)}

def gap_reversal(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day; n=len(o)
    pc=meta.get('pc',np.nan); oi=np.where(m==570)[0]
    if len(oi)==0 or not np.isfinite(pc) or pc<=0:return None
    ix=oi[0]; gap=float(o[ix]/pc-1)
    if abs(gap)<p['gap_min'] or abs(gap)>p['gap_max']:return None
    gapdir=1 if gap>0 else -1
    # Optional prior-trend requirement: only fade gaps that stretch against or
    # beyond the recent trend state.
    trend=0; ma20=meta.get('ma20',np.nan); ret5=meta.get('ret5',np.nan)
    if np.isfinite(ma20): trend=1 if pc>ma20 else -1
    if p['countertrend_only'] and trend==gapdir:return None
    if p['ret5_stretch']>0 and np.isfinite(ret5):
        if abs(ret5)<p['ret5_stretch']: return None
    # Establish opening ATR and require an extension in the gap direction first.
    ci=np.where((m>=570)&(m<=570+p['extension_min']))[0]
    if len(ci)<2:return None
    ar=float(np.nanmedian(atr[ci[:min(len(ci),4)]]))
    if not np.isfinite(ar) or ar<=0:return None
    openpx=float(o[ix]); extreme=openpx; ext_i=None
    for j in ci:
        if gapdir==1:
            extreme=max(extreme,float(h[j]))
            if extreme-openpx>=p['extension_atr']*ar: ext_i=j; break
        else:
            extreme=min(extreme,float(l[j]))
            if openpx-extreme>=p['extension_atr']*ar: ext_i=j; break
    if ext_i is None:return None
    # Reversal direction is opposite the gap. Require reclaim through VWAP/open
    # plus short EMA alignment before entering next bar.
    direction=-gapdir
    inds=np.where((np.arange(n)>ext_i)&(m<=p['entry_cutoff']))[0]
    for j in inds:
        if m[j]<570: continue
        if gapdir==1:
            reclaim=(c[j]<openpx) if p['reclaim']=='open' else (c[j]<vwap[j])
            emaok=(c[j]<e9[j] and e9[j]<e20[j])
        else:
            reclaim=(c[j]>openpx) if p['reclaim']=='open' else (c[j]>vwap[j])
            emaok=(c[j]>e9[j] and e9[j]>e20[j])
        body=abs(c[j]-o[j])/max(h[j]-l[j],1e-9)
        if not reclaim or (p['ema_confirm'] and not emaok) or body<p['body_frac']:continue
        ei=j+1
        if ei>=n:return None
        entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
        # Structural stop beyond the opening extension extreme observed up to reclaim.
        if gapdir==1:
            ex=float(np.max(h[ci[ci<=j]])); stop=ex+p['stop_atr']*ar
        else:
            ex=float(np.min(l[ci[ci<=j]])); stop=ex-p['stop_atr']*ar
        if not hc.valid_risk(entry,stop,p['max_stop_pct']):return None
        risk=abs(entry-stop); target=entry+direction*p['target_R']*risk
        z=hc.exit_trade(day,ei,direction,stop,target,p['slip_bps'],p['time_exit'])
        if z:z['family']='gap_reversal'
        return z
    return None

def trade_family(day,fam,p):
    if fam=='gap_reversal':return gap_reversal(day,p)
    f={'orb_retest':hc.strat_orb_retest,'trend_pullback':hc.strat_trend_pullback}[fam]
    z=f(day,p)
    if z:z['family']=fam
    return z

def bt(days,fam,p,y0,y1):
    out=[]
    for day in days:
        if y0<=day[0].year<=y1:
            z=trade_family(day,fam,p)
            if z:out.append(z)
    return out

def params_for(fam,n,seed):
    rng=np.random.default_rng(seed); out=[]
    for _ in range(n):
        p=BASE.copy(); p['direction']='both'; p['trend_filter']=bool(rng.integers(2));
        p['target_R']=[.50,.60,.75,1.0,1.25][int(rng.integers(5))]
        p['stop_atr']=[0,.1,.2,.3][int(rng.integers(4))]
        p['touch_atr']=[0,.1,.2,.3][int(rng.integers(4))]
        p['entry_cutoff']=[630,660,690,720][int(rng.integers(4))]
        p['ema_confirm']=bool(rng.integers(2))
        if fam=='orb_retest':
            p.update(orb_min=[15,30,45,60][int(rng.integers(4))],
                     max_or_atr=[2,3,4,5][int(rng.integers(4))],
                     break_atr=[0,.1,.2,.3][int(rng.integers(4))],
                     break_cutoff=[630,660,690,720][int(rng.integers(4))],
                     retest_bars=[2,3,4,6,9][int(rng.integers(5))])
        elif fam=='trend_pullback':
            p.update(drive_min=[15,30,45,60][int(rng.integers(4))],
                     drive_atr=[.5,.75,1,1.25,1.5,2][int(rng.integers(6))],
                     body_frac=[.2,.35,.5,.65][int(rng.integers(4))])
        else:
            # Fields unused by gap reversal are harmless.
            p.update(gap_min=[.002,.003,.004,.005,.0075,.01][int(rng.integers(6))],
                     gap_max=[.0125,.015,.02,.03,.05][int(rng.integers(5))],
                     extension_min=[15,30,45,60][int(rng.integers(4))],
                     extension_atr=[.2,.35,.5,.75,1.0][int(rng.integers(5))],
                     reclaim=['vwap','open'][int(rng.integers(2))],
                     countertrend_only=bool(rng.integers(2)),
                     ret5_stretch=[0,.005,.01,.015,.02][int(rng.integers(5))],
                     body_frac=[0,.2,.35,.5][int(rng.integers(4))],
                     time_exit=[780,840,900,955][int(rng.integers(4))])
            if p['gap_min']>=p['gap_max']:continue
        out.append(p)
    return out

def select_family(days,fam,n=4500):
    seed={'orb_retest':2026081511,'trend_pullback':2026081512,'gap_reversal':2026081513}[fam]
    survivors=[]
    for p in params_for(fam,n,seed):
        tr=bt(days,fam,p,2019,2022); tm=metrics(tr)
        if tm['n']<35 or tm['win']<.57 or tm['avgR']<=.03 or tm['pf']<1.12:continue
        a=metrics(bt(days,fam,p,2019,2020)); b=metrics(bt(days,fam,p,2021,2022))
        if a['n']<12 or b['n']<12 or a['avgR']<=0 or b['avgR']<=0:continue
        survivors.append((p,tm,a,b))
    valid=[]
    for p,tm,a,b in survivors:
        vr=bt(days,fam,p,2023,2025); vm=metrics(vr)
        if vm['n']<20 or vm['win']<.60 or vm['avgR']<=.035 or vm['pf']<1.15:continue
        yrs=[metrics(bt(days,fam,p,y,y)) for y in [2023,2024,2025]]
        observed=[x for x in yrs if x['n']>=5]
        if len(observed)<2 or sum(x['avgR']>0 for x in observed)<2:continue
        if any(x['avgR'] is not None and x['avgR']<-.20 for x in observed):continue
        # Stability score emphasizes worst-period win rate and expectancy.
        floorw=min(tm['win'],vm['win']); floore=min(tm['avgR'],vm['avgR']); floorpf=min(tm['pf'],vm['pf'])
        score=5*floorw+2*floore+.25*floorpf+.0005*min(tm['n']+vm['n'],300)+.004*max(tm['maxddR'],vm['maxddR'])
        valid.append((score,p,tm,vm,a,b,yrs))
    valid.sort(key=lambda x:x[0],reverse=True)
    return valid

def df_rows(rows,label):
    if not rows:return pd.DataFrame()
    d=pd.DataFrame(rows).copy();d['model']=label
    return d

def combine_portfolio(frames):
    # Max one trade/day. If strategies conflict, skip the day. Same-direction
    # signals are treated as consensus; earliest entry is used to avoid stacking risk.
    by={}
    for name,df in frames.items():
        if df is None or len(df)==0:continue
        for r in df.itertuples(index=False):
            by.setdefault(str(r.date),[]).append((name,r))
    out=[]
    for d,items in sorted(by.items()):
        dirs={int(r.dir) for _,r in items}
        if len(dirs)>1:continue
        chosen=sorted(items,key=lambda z:str(z[1].entry_ts))[0]
        rec=chosen[1]._asdict(); rec['model']='PORTFOLIO'; rec['sources']='+'.join(sorted(n for n,_ in items)); rec['agreement_count']=len(items);out.append(rec)
    return pd.DataFrame(out)

def yearly_portfolio(days,selected):
    rows=[]
    for y in range(2019,2026):
        la=oe.ledger(days,oe.A,'OCE_A',y,y);lb=oe.ledger(days,oe.B,'OCE_B',y,y);oce=oe.combine(la,lb,'union')
        frames={'OCE':oce}
        for fam,p in selected.items():frames[fam]=df_rows(bt(days,fam,p,y,y),fam)
        pf=combine_portfolio(frames); rows.append({'year':y,**metrics(pf)})
    return rows

def main(train_path,test_path):
    os.makedirs('portfolio_results',exist_ok=True)
    train=hc.prep(hc.load(train_path)); test=hc.prep(hc.load(test_path))
    print('TRAIN_DAYS',len(train),'HOLDOUT_DAYS',len(test),flush=True)
    selected={}; report={}
    for fam in ['orb_retest','gap_reversal','trend_pullback']:
        valid=select_family(train,fam)
        print('FAMILY',fam,'VALID_PRE2026',len(valid),flush=True)
        if not valid:
            report[fam]={'status':'REJECT_NO_PRE2026_CANDIDATE'};continue
        score,p,tm,vm,a,b,yrs=valid[0]
        selected[fam]=p
        h=bt(test,fam,p,2026,2026); hm=metrics(h)
        report[fam]={'status':'FROZEN_AND_TESTED','score':score,'params':p,'train_2019_22':tm,'validation_2023_25':vm,'years_2023_25':yrs,'holdout_2026':hm,'sim200_2pct':sim(h,.02)}
        print('FROZEN',fam,json.dumps(report[fam]),flush=True)
        pd.DataFrame(h).to_csv(f'portfolio_results/{fam}_2026.csv',index=False)

    # Baseline OCE and combined portfolio, with the selected new families.
    def oce_for(days,y0,y1):
        return oe.combine(oe.ledger(days,oe.A,'OCE_A',y0,y1),oe.ledger(days,oe.B,'OCE_B',y0,y1),'union')
    oce_hist=oce_for(train,2019,2025);oce_h=oce_for(test,2026,2026)
    hist_frames={'OCE':oce_hist};h_frames={'OCE':oce_h}
    for fam,p in selected.items():
        hist_frames[fam]=df_rows(bt(train,fam,p,2019,2025),fam)
        h_frames[fam]=df_rows(bt(test,fam,p,2026,2026),fam)
    port_hist=combine_portfolio(hist_frames);port_h=combine_portfolio(h_frames)
    result={'selected':report,'OCE_2019_25':metrics(oce_hist),'PORTFOLIO_2019_25':metrics(port_hist),'portfolio_sim200_2pct':sim(port_hist,.02),'OCE_2026':metrics(oce_h),'PORTFOLIO_2026':metrics(port_h),'portfolio_2026_sim200_2pct':sim(port_h,.02),'yearly_2019_25':yearly_portfolio(train,selected)}
    print('FINAL',json.dumps(result),flush=True)
    if len(port_hist):port_hist.to_csv('portfolio_results/portfolio_2019_25.csv',index=False)
    if len(port_h):port_h.to_csv('portfolio_results/portfolio_2026.csv',index=False)
    json.dump(result,open('portfolio_results/summary.json','w'),indent=2)

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
