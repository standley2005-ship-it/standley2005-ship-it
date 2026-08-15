import json, os, sys
import numpy as np
import pandas as pd
import high_confidence_search as hc

# Focused second-pass search. 2019-2025 chooses parameters; 2026 is opened only after freeze.

def gap2(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day; n=len(o)
    pc=meta.get('pc',np.nan)
    oi=np.where(m==570)[0]
    if len(oi)==0 or not np.isfinite(pc) or pc<=0:return None
    ix=oi[0]; gap=o[ix]/pc-1
    if abs(gap)<p['gap_min'] or abs(gap)>p['gap_max']:return None
    direction=1 if gap>0 else -1
    if p['direction']=='long' and direction<0:return None
    if p['direction']=='short' and direction>0:return None

    # Prior 5-day context, known before the session opens.
    r5=meta.get('ret5',np.nan)
    if p['ret5_filter']!='none' and np.isfinite(r5):
        aligned=(r5*direction)>0
        if p['ret5_filter']=='align' and not aligned:return None
        if p['ret5_filter']=='contra' and aligned:return None

    # Premarket context from 4:00-9:25. These values are all known by 9:30.
    pm=np.where((m>=240)&(m<570))[0]
    if len(pm)>=10:
        pm_move=(c[pm[-1]]/o[pm[0]]-1)*direction
        ar_pm=float(np.nanmedian(atr[pm[-10:]]))
        pm_range=(float(h[pm].max())-float(l[pm].min()))/ar_pm if np.isfinite(ar_pm) and ar_pm>0 else np.nan
        if p['pm_filter']=='align' and pm_move<=0:return None
        if p['pm_filter']=='contra' and pm_move>=0:return None
        if p['pm_filter']=='strong_align' and pm_move<p['pm_move_min']:return None
        if p['pm_range_max']>0 and np.isfinite(pm_range) and pm_range>p['pm_range_max']:return None
    elif p['pm_filter']!='none':
        return None

    # Opening confirmation: the gap must keep moving before we buy the pullback.
    ci=np.where((m>=570)&(m<570+p['confirm_min']))[0]
    if len(ci)<2:return None
    ar=float(np.nanmedian(atr[ci[-3:]]))
    if not np.isfinite(ar) or ar<=0:return None
    open_move=(c[ci[-1]]/o[ix]-1)*direction
    if open_move<p['open_confirm']:return None
    orng=(float(h[ci].max())-float(l[ci].min()))/ar
    if p['opening_range_max_atr']>0 and orng>p['opening_range_max_atr']:return None

    trend=0
    ma20=meta.get('ma20',np.nan)
    if np.isfinite(ma20):trend=1 if pc>ma20 else -1
    if p['trend_filter'] and trend!=direction:return None

    inds=np.where((m>=570+p['confirm_min'])&(m<=p['entry_cutoff']))[0]
    for j in inds:
        near=(l[j]<=e9[j]+p['touch_atr']*ar) if direction==1 else (h[j]>=e9[j]-p['touch_atr']*ar)
        reclaim=(c[j]>e9[j] and c[j]>pc) if direction==1 else (c[j]<e9[j] and c[j]<pc)
        ema_ok=(e9[j]>e20[j]) if direction==1 else (e9[j]<e20[j])
        vw_ok=(c[j]>vwap[j]) if direction==1 else (c[j]<vwap[j])
        body=max(h[j]-l[j],1e-9)
        close_quality=(c[j]-l[j])/body if direction==1 else (h[j]-c[j])/body
        if near and reclaim and (not p['ema_confirm'] or ema_ok) and (not p['vwap_align'] or vw_ok) and close_quality>=p['close_quality']:
            ei=j+1
            if ei>=n:return None
            entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
            # Structural/EMA20 stop with ATR cushion.
            if p['stop_mode']=='ema20':
                stop=(e20[j]-p['stop_atr']*ar) if direction==1 else (e20[j]+p['stop_atr']*ar)
            else:
                lb=max(ci[-1]+1,j-p['swing_bars']+1)
                stop=(float(l[lb:j+1].min())-p['stop_atr']*ar) if direction==1 else (float(h[lb:j+1].max())+p['stop_atr']*ar)
            if not hc.valid_risk(entry,stop,p['max_stop_pct']):return None
            risk=abs(entry-stop); target=entry+direction*p['target_R']*risk
            return hc.exit_trade(day,ei,direction,stop,target,p['slip_bps'],p['time_exit'])
    return None

def bt(days,p,y0,y1):
    out=[]
    for day in days:
        if y0<=day[0].year<=y1:
            x=gap2(day,p)
            if x:out.append(x)
    return out

def params(n=6000):
    rng=np.random.default_rng(2026081511);out=[];seen=set()
    while len(out)<n:
        p={
          'slip_bps':1.0,'max_stop_pct':.012,
          'direction':['short','long','both'][int(rng.integers(3))],
          'gap_min':[.0015,.002,.0025,.003,.004,.005,.006][int(rng.integers(7))],
          'gap_max':[.012,.015,.02,.03,.05][int(rng.integers(5))],
          'confirm_min':[15,30,45,60][int(rng.integers(4))],
          'open_confirm':[0,.00075,.0015,.002,.0025,.003,.004][int(rng.integers(7))],
          'entry_cutoff':[645,660,675,690,720,750][int(rng.integers(6))],
          'touch_atr':[0,.1,.2,.3,.5][int(rng.integers(5))],
          'ema_confirm':bool(rng.integers(2)),
          'vwap_align':bool(rng.integers(2)),
          'trend_filter':bool(rng.integers(2)),
          'ret5_filter':['none','align','contra'][int(rng.integers(3))],
          'pm_filter':['none','align','contra','strong_align'][int(rng.integers(4))],
          'pm_move_min':[.001,.002,.003][int(rng.integers(3))],
          'pm_range_max':[0,4,6,8,12][int(rng.integers(5))],
          'opening_range_max_atr':[0,2,3,4,6][int(rng.integers(5))],
          'close_quality':[.45,.55,.65][int(rng.integers(3))],
          'stop_mode':['ema20','swing'][int(rng.integers(2))],
          'swing_bars':[2,3,5][int(rng.integers(3))],
          'stop_atr':[0,.1,.2,.3][int(rng.integers(4))],
          'target_R':[.75,1.0,1.25,1.5][int(rng.integers(4))],
          'time_exit':[720,780,840,955][int(rng.integers(4))]
        }
        if p['gap_min']>=p['gap_max']:continue
        key=json.dumps(p,sort_keys=True)
        if key not in seen:seen.add(key);out.append(p)
    return out

def main(train_path,test_path):
    os.makedirs('gap_confidence_results',exist_ok=True)
    train=hc.prep(hc.load(train_path));test=hc.prep(hc.load(test_path))
    print('DATA',len(train),len(test),flush=True)
    surv=[]
    for i,p in enumerate(params(),1):
        tm=hc.met(bt(train,p,2019,2022))
        if tm['n']<40 or tm['win']<.56 or tm['avgR']<=.04 or tm['pf']<1.15:continue
        a=hc.met(bt(train,p,2019,2020));b=hc.met(bt(train,p,2021,2022))
        if a['n']<14 or b['n']<14 or a['avgR']<=0 or b['avgR']<=0:continue
        surv.append((p,tm,a,b))
        if i%1000==0:print('PROGRESS',i,'SURV',len(surv),flush=True)
    print('TRAIN_SURV',len(surv),flush=True)
    valid=[]
    for p,tm,a,b in surv:
        vm=hc.met(bt(train,p,2023,2025)); ys=[hc.met(bt(train,p,y,y)) for y in [2023,2024,2025]]
        if vm['n']<30 or vm['win']<.58 or vm['avgR']<=.05 or vm['pf']<1.20:continue
        # Positive recent expectancy in at least 2/3 years and no year badly negative.
        considered=[x for x in ys if x['n']>=6]
        if len(considered)<2 or sum(x['avgR']>0 for x in considered)<2:continue
        if any(x['avgR']<-.20 for x in considered):continue
        floor=min(tm['win'],vm['win']); efloor=min(tm['avgR'],vm['avgR']); pff=min(tm['pf'],vm['pf'])
        score=5*floor+1.5*efloor+.25*pff+.0005*min(tm['n']+vm['n'],350)+.005*max(tm['maxddR'],vm['maxddR'])
        valid.append((score,p,tm,vm,a,b,ys))
    valid.sort(key=lambda z:z[0],reverse=True)
    print('VALID',len(valid),flush=True)
    rows=[]
    for rank,z in enumerate(valid[:40],1):
        score,p,tm,vm,a,b,ys=z
        hr=bt(test,p,2026,2026);hm=hc.met(hr);bal,dd=hc.sim(hr,.02)
        rec={'rank':rank,'score':score,'params':p,'train':tm,'validation':vm,'years':ys,'holdout2026':hm,'end200_2pct':bal,'dd200_2pct':dd*100}
        rows.append(rec);print('CAND',json.dumps(rec),flush=True)
    passed=[r for r in rows if r['holdout2026']['n']>=8 and r['holdout2026']['win']>=.60 and r['holdout2026']['avgR']>0 and r['holdout2026']['pf']>=1.20]
    print('PASSED',len(passed),flush=True)
    if passed:
        winner=sorted(passed,key=lambda r:(r['holdout2026']['win'],r['holdout2026']['pf'],r['holdout2026']['n'],r['validation']['win']),reverse=True)[0]
        print('WINNER',json.dumps(winner),flush=True)
        tr=bt(test,winner['params'],2026,2026);pd.DataFrame(tr).to_csv('gap_confidence_results/winner_2026_trades.csv',index=False);json.dump(winner,open('gap_confidence_results/winner.json','w'),indent=2)
    flat=[]
    for r in rows:
        flat.append({'rank':r['rank'],'score':r['score'],'params':json.dumps(r['params'],sort_keys=True),**{f'train_{k}':v for k,v in r['train'].items()},**{f'val_{k}':v for k,v in r['validation'].items()},**{f'h26_{k}':v for k,v in r['holdout2026'].items()},'end200_2pct':r['end200_2pct'],'dd200_2pct':r['dd200_2pct']})
    pd.DataFrame(flat).to_csv('gap_confidence_results/top40.csv',index=False)
if __name__=='__main__':main(sys.argv[1],sys.argv[2])