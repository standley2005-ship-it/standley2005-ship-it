import json, os
import numpy as np
import pandas as pd
import high_confidence_search as hc

BASE={'slip_bps':1.0,'max_stop_pct':.012}

def metrics(rows):
    if not rows:return {'n':0,'win':None,'avgR':None,'pf':None,'totalR':0.0,'maxddR':None}
    r=np.array([x['R'] for x in rows],float);pos=r[r>0].sum();neg=-r[r<0].sum();eq=np.cumsum(r);dd=eq-np.maximum.accumulate(eq)
    return {'n':int(len(r)),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pos/neg if neg>0 else 999),'totalR':float(r.sum()),'maxddR':float(dd.min())}

def sim(rows,rf=.02):
    b=200.;pk=b;dd=0.
    for x in rows:b=max(0,b*(1+rf*x['R']));pk=max(pk,b);dd=min(dd,b/pk-1)
    return {'end':float(b),'maxdd_pct':float(dd*100)}

def vwap_reversion(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day;n=len(o)
    oi=np.where(m==570)[0]; ci=np.where((m>=570)&(m<570+p['observe_min']))[0]
    if len(oi)==0 or len(ci)<3:return None
    ix=oi[0]; ar=float(np.nanmedian(atr[ci[-3:]]))
    if not np.isfinite(ar) or ar<=0:return None
    move=(float(c[ci[-1]])-float(o[ix]))/ar
    if abs(move)<p['drive_atr']:return None
    drive=1 if move>0 else -1
    # Only fade if price is materially stretched from VWAP.
    dist=(float(c[ci[-1]])-float(vwap[ci[-1]]))/ar
    if abs(dist)<p['vwap_dist_atr'] or np.sign(dist)!=drive:return None
    pc=meta.get('pc',np.nan);ma20=meta.get('ma20',np.nan);trend=0
    if np.isfinite(pc) and np.isfinite(ma20):trend=1 if pc>ma20 else -1
    if p['avoid_trend'] and trend==drive:return None
    direction=-drive
    inds=np.where((m>=570+p['observe_min'])&(m<=p['entry_cutoff']))[0]
    extreme=float(np.max(h[ci]) if drive==1 else np.min(l[ci]))
    for j in inds:
        # Require momentum to turn toward VWAP and a close through EMA9.
        if drive==1:
            turned=(c[j]<e9[j]) and (c[j]<o[j] if p['body_confirm'] else True)
            extreme=max(extreme,float(h[j]))
        else:
            turned=(c[j]>e9[j]) and (c[j]>o[j] if p['body_confirm'] else True)
            extreme=min(extreme,float(l[j]))
        if not turned:continue
        ei=j+1
        if ei>=n:return None
        entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
        stop=(extreme+p['stop_atr']*ar) if direction==-1 else (extreme-p['stop_atr']*ar)
        if not hc.valid_risk(entry,stop,p['max_stop_pct']):return None
        risk=abs(entry-stop)
        # Fixed-R target; parameter grid favors modest targets for high hit-rate research.
        target=entry+direction*p['target_R']*risk
        z=hc.exit_trade(day,ei,direction,stop,target,p['slip_bps'],p['time_exit'])
        if z:z['family']='vwap_reversion'
        return z
    return None

def orb_failed_break(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day;n=len(o)
    oi=np.where((m>=570)&(m<570+p['orb_min']))[0]
    if len(oi)<3:return None
    rh=float(h[oi].max());rl=float(l[oi].min());ar=float(np.nanmedian(atr[oi[-3:]]))
    if not np.isfinite(ar) or ar<=0:return None
    if (rh-rl)/ar>p['max_or_atr']:return None
    inds=np.where((m>=570+p['orb_min'])&(m<=p['sweep_cutoff']))[0]
    for i in inds:
        bdir=1 if h[i]>=rh+p['sweep_atr']*ar else (-1 if l[i]<=rl-p['sweep_atr']*ar else 0)
        if bdir==0:continue
        level=rh if bdir==1 else rl;ext=float(h[i] if bdir==1 else l[i]);ri=None
        for j in range(i,min(n,i+1+p['reclaim_bars'])):
            ext=max(ext,float(h[j])) if bdir==1 else min(ext,float(l[j]))
            back=(c[j]<level) if bdir==1 else (c[j]>level)
            emaok=(c[j]<e9[j]) if bdir==1 else (c[j]>e9[j])
            if back and (not p['ema_confirm'] or emaok):ri=j;break
        if ri is None:continue
        direction=-bdir;ei=ri+1
        if ei>=n or m[ei]>p['entry_cutoff']:continue
        entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
        stop=(ext+p['stop_atr']*ar) if bdir==1 else (ext-p['stop_atr']*ar)
        if not hc.valid_risk(entry,stop,p['max_stop_pct']):continue
        risk=abs(entry-stop);target=entry+direction*p['target_R']*risk
        z=hc.exit_trade(day,ei,direction,stop,target,p['slip_bps'],p['time_exit'])
        if z:z['family']='orb_failed_break'
        return z
    return None

def trade(day,fam,p):
    if fam=='premarket_retest':z=hc.strat_premarket_retest(day,p)
    elif fam=='gap_pullback':z=hc.strat_gap_pullback(day,p)
    elif fam=='vwap_reversion':z=vwap_reversion(day,p)
    elif fam=='orb_failed_break':z=orb_failed_break(day,p)
    else:raise ValueError(fam)
    if z:z['family']=fam
    return z

def bt(days,fam,p,y0,y1):
    out=[]
    for day in days:
        if y0<=day[0].year<=y1:
            z=trade(day,fam,p)
            if z:out.append(z)
    return out

def params_for(fam,n,seed):
    rng=np.random.default_rng(seed);out=[]
    for _ in range(n):
        p=BASE.copy();p['direction']='both';p['trend_filter']=bool(rng.integers(2));p['target_R']=[.5,.6,.75,1.0,1.25][int(rng.integers(5))];p['stop_atr']=[0,.1,.2,.3][int(rng.integers(4))];p['touch_atr']=[0,.1,.2,.3][int(rng.integers(4))];p['entry_cutoff']=[630,660,690,720][int(rng.integers(4))];p['ema_confirm']=bool(rng.integers(2))
        if fam=='premarket_retest':
            p.update(pm_start=[420,450,480,510][int(rng.integers(4))],min_range_atr=[1.5,2,3][int(rng.integers(3))],max_range_atr=[5,7,9,12][int(rng.integers(4))],break_atr=[0,.1,.2,.3][int(rng.integers(4))],break_cutoff=[630,660,690][int(rng.integers(3))],retest_bars=[2,3,4,6,9][int(rng.integers(5))])
        elif fam=='gap_pullback':
            p.update(gap_min=[.002,.003,.005,.0075][int(rng.integers(4))],gap_max=[.015,.02,.03,.05][int(rng.integers(4))],confirm_min=[15,30,45,60][int(rng.integers(4))],open_confirm=[0,.001,.002,.003][int(rng.integers(4))])
            if p['gap_min']>=p['gap_max']:continue
        elif fam=='vwap_reversion':
            p.update(observe_min=[15,30,45,60][int(rng.integers(4))],drive_atr=[1,1.5,2,2.5,3][int(rng.integers(5))],vwap_dist_atr=[.5,.75,1,1.5,2][int(rng.integers(5))],avoid_trend=bool(rng.integers(2)),body_confirm=bool(rng.integers(2)),time_exit=[720,780,840,900][int(rng.integers(4))])
        else:
            p.update(orb_min=[15,30,45,60][int(rng.integers(4))],max_or_atr=[2,3,4,5][int(rng.integers(4))],sweep_atr=[0,.1,.2,.3,.5][int(rng.integers(5))],sweep_cutoff=[630,660,690,720][int(rng.integers(4))],reclaim_bars=[1,2,3,4,6][int(rng.integers(5))],time_exit=[720,780,840,900][int(rng.integers(4))])
        out.append(p)
    return out

def select(days,fam,n=1200):
    seed={'premarket_retest':2026081521,'gap_pullback':2026081522,'vwap_reversion':2026081523,'orb_failed_break':2026081524}[fam]
    surv=[]
    for p in params_for(fam,n,seed):
        tr=bt(days,fam,p,2019,2022);tm=metrics(tr)
        if tm['n']<35 or tm['win']<.57 or tm['avgR']<=.03 or tm['pf']<1.12:continue
        a=metrics(bt(days,fam,p,2019,2020));b=metrics(bt(days,fam,p,2021,2022))
        if a['n']<12 or b['n']<12 or a['avgR']<=0 or b['avgR']<=0:continue
        surv.append((p,tm,a,b))
    valid=[]
    for p,tm,a,b in surv:
        vr=bt(days,fam,p,2023,2025);vm=metrics(vr)
        if vm['n']<20 or vm['win']<.60 or vm['avgR']<=.035 or vm['pf']<1.15:continue
        yrs=[metrics(bt(days,fam,p,y,y)) for y in [2023,2024,2025]];obs=[x for x in yrs if x['n']>=5]
        if len(obs)<2 or sum(x['avgR']>0 for x in obs)<2:continue
        if any(x['avgR'] is not None and x['avgR']<-.20 for x in obs):continue
        score=5*min(tm['win'],vm['win'])+2*min(tm['avgR'],vm['avgR'])+.25*min(tm['pf'],vm['pf'])+.0005*min(tm['n']+vm['n'],300)+.004*max(tm['maxddR'],vm['maxddR'])
        valid.append((score,p,tm,vm,yrs))
    valid.sort(key=lambda x:x[0],reverse=True);return valid
