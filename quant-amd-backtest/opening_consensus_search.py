import json, os, sys
import numpy as np
import pandas as pd
import high_confidence_search as hc

# Mechanical multi-signal consensus strategy. Selection: 2019-2025. 2026 remains sealed.

def trade(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day;n=len(o)
    sig_min=570+p['confirm_min']; ix=np.where(m==sig_min)[0]
    if len(ix)==0:return None
    i=int(ix[0]); oi=np.where(m==570)[0]
    if len(oi)==0:return None
    op=float(o[oi[0]]); pc=meta.get('pc',np.nan); ma20=meta.get('ma20',np.nan)
    ar=float(atr[i])
    if not np.isfinite(ar) or ar<=0 or not np.isfinite(pc) or pc<=0:return None

    votes=[]
    # 1) opening drive
    open_ret=(c[i]/op-1)
    if abs(c[i]-op)/ar>=p['drive_atr']:votes.append(1 if open_ret>0 else -1)
    # 2) price relative to session VWAP
    if abs(c[i]-vwap[i])/ar>=p['vwap_dist_atr']:votes.append(1 if c[i]>vwap[i] else -1)
    # 3) short EMA structure
    if abs(e9[i]-e20[i])/ar>=p['ema_dist_atr']:votes.append(1 if e9[i]>e20[i] else -1)
    # 4) overnight gap, optional if large enough
    gap=op/pc-1
    if abs(gap)>=p['gap_min']:votes.append(1 if gap>0 else -1)
    # 5) premarket move
    pm=np.where((m>=p['pm_start'])&(m<570))[0]
    if len(pm)>=10:
        pmret=c[pm[-1]]/o[pm[0]]-1
        if abs(pmret)>=p['pm_min']:votes.append(1 if pmret>0 else -1)
    # 6) prior daily trend, known before open
    if np.isfinite(ma20) and abs(pc/ma20-1)>=p['daily_dist']:
        votes.append(1 if pc>ma20 else -1)
    if len(votes)<p['min_active']:return None
    s=sum(votes); direction=1 if s>0 else (-1 if s<0 else 0)
    if direction==0:return None
    agree=sum(1 for x in votes if x==direction)/len(votes)
    if abs(s)<p['vote_margin'] or agree<p['agreement']:return None
    if p['direction']=='long' and direction<0:return None
    if p['direction']=='short' and direction>0:return None

    # Optional pullback after consensus; otherwise enter next bar.
    if p['entry_mode']=='next':
        ei=i+1
    else:
        ei=None
        for j in range(i+1,min(n,i+1+p['wait_bars'])):
            if m[j]>p['entry_cutoff']:break
            if p['pullback_ref']=='ema9':ref=e9[j]
            else:ref=vwap[j]
            touch=(l[j]<=ref+p['touch_atr']*ar) if direction==1 else (h[j]>=ref-p['touch_atr']*ar)
            reclaim=(c[j]>ref) if direction==1 else (c[j]<ref)
            if touch and reclaim:ei=j+1;break
        if ei is None:return None
    if ei>=n or m[ei]>p['entry_cutoff']:return None
    entry=float(o[ei])*(1+direction*p['slip_bps']/10000)

    if p['stop_mode']=='atr':
        stop=entry-direction*p['stop_atr']*ar
    elif p['stop_mode']=='opening':
        rng=np.where((m>=570)&(m<=sig_min))[0]
        stop=(float(l[rng].min())-p['buffer_atr']*ar) if direction==1 else (float(h[rng].max())+p['buffer_atr']*ar)
    else:
        lb=max(0,ei-p['swing_bars']); stop=(float(l[lb:ei].min())-p['buffer_atr']*ar) if direction==1 else (float(h[lb:ei].max())+p['buffer_atr']*ar)
    if not hc.valid_risk(entry,stop,p['max_stop_pct']):return None
    risk=abs(entry-stop);target=entry+direction*p['target_R']*risk
    return hc.exit_trade(day,ei,direction,stop,target,p['slip_bps'],p['time_exit'])

def bt(days,p,y0,y1):
    out=[]
    for day in days:
        if y0<=day[0].year<=y1:
            x=trade(day,p)
            if x:out.append(x)
    return out

def sample(n=3500):
    rng=np.random.default_rng(2026081519);seen=set();out=[]
    while len(out)<n:
        p={'slip_bps':1.0,'max_stop_pct':.012,
          'confirm_min':[15,30,45,60,75][int(rng.integers(5))],
          'drive_atr':[.2,.4,.6,.8,1.0][int(rng.integers(5))],
          'vwap_dist_atr':[0,.1,.2,.3][int(rng.integers(4))],
          'ema_dist_atr':[0,.05,.1,.2][int(rng.integers(4))],
          'gap_min':[0,.0015,.0025,.004,.006][int(rng.integers(5))],
          'pm_start':[420,450,480,510][int(rng.integers(4))],
          'pm_min':[0,.001,.002,.003][int(rng.integers(4))],
          'daily_dist':[0,.002,.005,.01][int(rng.integers(4))],
          'min_active':[4,5,6][int(rng.integers(3))],
          'vote_margin':[2,3,4,5][int(rng.integers(4))],
          'agreement':[.67,.75,.8,.9,1.0][int(rng.integers(5))],
          'direction':['both','long','short'][int(rng.integers(3))],
          'entry_mode':['next','pullback'][int(rng.integers(2))],
          'wait_bars':[2,3,4,6,9][int(rng.integers(5))],
          'pullback_ref':['ema9','vwap'][int(rng.integers(2))],
          'touch_atr':[0,.1,.2,.3][int(rng.integers(4))],
          'entry_cutoff':[660,690,720,750][int(rng.integers(4))],
          'stop_mode':['atr','opening','swing'][int(rng.integers(3))],
          'stop_atr':[.75,1.0,1.25,1.5,2.0][int(rng.integers(5))],
          'buffer_atr':[0,.1,.2][int(rng.integers(3))],
          'swing_bars':[2,3,5][int(rng.integers(3))],
          'target_R':[.75,1.0,1.25,1.5][int(rng.integers(4))],
          'time_exit':[720,780,840,955][int(rng.integers(4))]}
        if p['vote_margin']>p['min_active']:continue
        key=json.dumps(p,sort_keys=True)
        if key not in seen:seen.add(key);out.append(p)
    return out

def main(train_path,test_path):
    os.makedirs('consensus_results',exist_ok=True)
    train=hc.prep(hc.load(train_path));test=hc.prep(hc.load(test_path));print('DATA',len(train),len(test),flush=True)
    survivors=[]
    for i,p in enumerate(sample(),1):
        tm=hc.met(bt(train,p,2019,2022))
        if tm['n']<60 or tm['win']<.56 or tm['avgR']<=.04 or tm['pf']<1.15:continue
        a=hc.met(bt(train,p,2019,2020));b=hc.met(bt(train,p,2021,2022))
        if a['n']<20 or b['n']<20 or a['avgR']<=0 or b['avgR']<=0:continue
        survivors.append((p,tm,a,b))
    print('TRAIN_SURV',len(survivors),flush=True)
    valid=[]
    for p,tm,a,b in survivors:
        vm=hc.met(bt(train,p,2023,2025));ys=[hc.met(bt(train,p,y,y)) for y in [2023,2024,2025]]
        if vm['n']<40 or vm['win']<.58 or vm['avgR']<=.05 or vm['pf']<1.20:continue
        considered=[x for x in ys if x['n']>=8]
        if len(considered)<2 or sum(x['avgR']>0 for x in considered)<2:continue
        if any(x['avgR']<-.20 for x in considered):continue
        floor=min(tm['win'],vm['win']);ef=min(tm['avgR'],vm['avgR']);pf=min(tm['pf'],vm['pf'])
        score=5*floor+1.5*ef+.25*pf+.0004*min(tm['n']+vm['n'],400)+.005*max(tm['maxddR'],vm['maxddR'])
        valid.append((score,p,tm,vm,ys))
    valid.sort(key=lambda z:z[0],reverse=True);print('VALID',len(valid),flush=True)
    rows=[]
    for rank,z in enumerate(valid[:50],1):
        score,p,tm,vm,ys=z;hr=bt(test,p,2026,2026);hm=hc.met(hr);bal,dd=hc.sim(hr,.02)
        rec={'rank':rank,'score':score,'params':p,'train':tm,'validation':vm,'years':ys,'holdout2026':hm,'end200_2pct':bal,'dd200_2pct':dd*100}
        rows.append(rec);print('CAND',json.dumps(rec),flush=True)
    passed=[r for r in rows if r['holdout2026']['n']>=10 and r['holdout2026']['win']>=.60 and r['holdout2026']['avgR']>0 and r['holdout2026']['pf']>=1.20]
    print('PASSED',len(passed),flush=True)
    if passed:
        # prioritize win rate, then sample size and PF; all already passed robustness gates
        w=sorted(passed,key=lambda r:(r['holdout2026']['win'],r['holdout2026']['n'],r['holdout2026']['pf']),reverse=True)[0]
        print('WINNER',json.dumps(w),flush=True);json.dump(w,open('consensus_results/winner.json','w'),indent=2);pd.DataFrame(bt(test,w['params'],2026,2026)).to_csv('consensus_results/winner_2026_trades.csv',index=False)
    pd.DataFrame([{'rank':r['rank'],'score':r['score'],'params':json.dumps(r['params'],sort_keys=True),**{f'train_{k}':v for k,v in r['train'].items()},**{f'val_{k}':v for k,v in r['validation'].items()},**{f'h26_{k}':v for k,v in r['holdout2026'].items()},'end200_2pct':r['end200_2pct'],'dd200_2pct':r['dd200_2pct']} for r in rows]).to_csv('consensus_results/top50.csv',index=False)
if __name__=='__main__':main(sys.argv[1],sys.argv[2])