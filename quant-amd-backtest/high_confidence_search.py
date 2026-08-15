import pandas as pd, numpy as np, sys, json, os

# Objective search across several intraday strategy families.
# Selection uses 2019-2025 only. 2026 is never consulted until final holdout.

def load(path):
    df=pd.read_csv(path,low_memory=False); cols={c.lower().strip():c for c in df.columns}
    if 'ds' in cols: ts=df[cols['ds']]
    elif 'datetime' in cols: ts=df[cols['datetime']]
    elif 'timestamp' in cols: ts=df[cols['timestamp']]
    elif 'date' in cols and 'time' in cols: ts=df[cols['date']].astype(str)+' '+df[cols['time']].astype(str)
    elif 'date' in cols: ts=df[cols['date']]
    else: raise ValueError(df.columns)
    out=pd.DataFrame({'ts':pd.to_datetime(ts,errors='coerce')})
    for k in ['open','high','low','close']:
        out[k]=pd.to_numeric(df[cols[k]],errors='coerce')
    if 'volume' in cols: out['volume']=pd.to_numeric(df[cols['volume']],errors='coerce').fillna(0)
    else: out['volume']=1.0
    out=out.dropna(subset=['ts','open','high','low','close']).sort_values('ts').drop_duplicates('ts')
    out=out[out.ts.dt.dayofweek<5]
    out['minute']=out.ts.dt.hour*60+out.ts.dt.minute
    out=out[(out.minute>=240)&(out.minute<=960)].copy(); out['date']=out.ts.dt.date
    return out

def prep(df):
    rth=df[(df.minute>=570)&(df.minute<=960)].copy()
    daily=rth.groupby('date').agg(dopen=('open','first'),dhigh=('high','max'),dlow=('low','min'),dclose=('close','last'))
    daily['pc']=daily.dclose.shift(1); daily['ph']=daily.dhigh.shift(1); daily['pl']=daily.dlow.shift(1)
    daily['ma20']=daily.dclose.rolling(20).mean().shift(1); daily['ma50']=daily.dclose.rolling(50).mean().shift(1)
    daily['ret5']=daily.dclose.pct_change(5).shift(1)
    maps={c:dict(zip(daily.index,daily[c])) for c in daily.columns}
    days=[]
    for d,g in df.groupby('date',sort=True):
        g=g.sort_values('ts')
        if ((g.minute>=570)&(g.minute<=960)).sum()<70: continue
        o=g.open.to_numpy(float); h=g.high.to_numpy(float); l=g.low.to_numpy(float); c=g.close.to_numpy(float); v=g.volume.to_numpy(float)
        m=g.minute.to_numpy(int); ts=g.ts.to_numpy(); n=len(g)
        prev=np.r_[o[0],c[:-1]]; tr=np.maximum.reduce([h-l,np.abs(h-prev),np.abs(l-prev)])
        atr=pd.Series(tr).rolling(14,min_periods=5).mean().to_numpy()
        ema9=pd.Series(c).ewm(span=9,adjust=False).mean().to_numpy(); ema20=pd.Series(c).ewm(span=20,adjust=False).mean().to_numpy()
        typ=(h+l+c)/3; cumv=np.cumsum(np.maximum(v,0)); vwap=np.cumsum(typ*np.maximum(v,0))/np.where(cumv>0,cumv,np.arange(n)+1)
        meta={k:maps[k].get(d,np.nan) for k in maps}
        days.append((d,meta,m,ts,o,h,l,c,v,atr,ema9,ema20,vwap))
    return days

def exit_trade(day,ei,direction,stop,target,slip_bps=1.0,time_exit=955):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day; n=len(o)
    raw=float(o[ei]); entry=raw*(1+direction*slip_bps/10000)
    risk=(entry-stop) if direction==1 else (stop-entry)
    if risk<=0:return None
    xp=None;reason='time';xi=n-1
    for j in range(ei,n):
        if m[j]<570:continue
        sh=(l[j]<=stop) if direction==1 else (h[j]>=stop)
        th=(h[j]>=target) if direction==1 else (l[j]<=target)
        # Conservative same-bar ambiguity: stop first.
        if sh: xp=stop; reason='stop'; xi=j; break
        if th: xp=target; reason='target'; xi=j; break
        if m[j]>=time_exit: xp=float(c[j]); reason='time'; xi=j; break
    if xp is None:xp=float(c[-1])
    xnet=xp*(1-direction*slip_bps/10000)
    R=((xnet-entry)*direction)/risk
    return {'date':d,'R':float(R),'dir':int(direction),'reason':reason,'entry_ts':str(ts[ei]),'exit_ts':str(ts[xi]),'entry':entry,'stop':stop,'target':target}

def valid_risk(entry,stop,max_stop_pct=.012):
    r=abs(entry-stop); return r>0 and r/entry<=max_stop_pct

def strat_premarket_retest(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day;n=len(o)
    pi=np.where((m>=p['pm_start'])&(m<570))[0]
    if len(pi)<12:return None
    ph=float(h[pi].max());pl=float(l[pi].min()); ar=float(np.nanmedian(atr[pi[-6:]]))
    if not np.isfinite(ar) or ar<=0:return None
    rw=(ph-pl)/ar
    if rw<p['min_range_atr'] or rw>p['max_range_atr']:return None
    inds=np.where((m>=570)&(m<=p['break_cutoff']))[0]
    trend=0
    if np.isfinite(meta.get('pc',np.nan)) and np.isfinite(meta.get('ma20',np.nan)):
        trend=1 if meta['pc']>meta['ma20'] else -1
    for i in inds:
        direction=1 if c[i]>ph+p['break_atr']*ar else (-1 if c[i]<pl-p['break_atr']*ar else 0)
        if direction==0:continue
        if p['trend_filter'] and trend!=direction:continue
        if p['direction']=='long' and direction<0:continue
        if p['direction']=='short' and direction>0:continue
        level=ph if direction==1 else pl
        ri=None;extreme=float(l[i] if direction==1 else h[i])
        for j in range(i+1,min(n,i+1+p['retest_bars'])):
            extreme=min(extreme,float(l[j])) if direction==1 else max(extreme,float(h[j]))
            touched=(l[j]<=level+p['touch_atr']*ar) if direction==1 else (h[j]>=level-p['touch_atr']*ar)
            reclaimed=(c[j]>level) if direction==1 else (c[j]<level)
            aligned=(c[j]>e9[j]) if direction==1 else (c[j]<e9[j])
            if touched and reclaimed and (not p['ema_confirm'] or aligned):ri=j;break
        if ri is None:continue
        ei=ri+1
        if ei>=n or m[ei]>p['entry_cutoff']:continue
        entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
        stop=(level-p['stop_atr']*ar) if direction==1 else (level+p['stop_atr']*ar)
        if not valid_risk(entry,stop,p['max_stop_pct']):continue
        risk=abs(entry-stop);target=entry+direction*p['target_R']*risk
        return exit_trade(day,ei,direction,stop,target,p['slip_bps'])
    return None

def strat_orb_retest(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day;n=len(o)
    oi=np.where((m>=570)&(m<570+p['orb_min']))[0]
    if len(oi)<3:return None
    rh=float(h[oi].max());rl=float(l[oi].min());ar=float(np.nanmedian(atr[oi[-3:]]))
    if not np.isfinite(ar) or ar<=0:return None
    if (rh-rl)/ar>p['max_or_atr']:return None
    trend=0
    if np.isfinite(meta.get('pc',np.nan)) and np.isfinite(meta.get('ma20',np.nan)):trend=1 if meta['pc']>meta['ma20'] else -1
    inds=np.where((m>=570+p['orb_min'])&(m<=p['break_cutoff']))[0]
    for i in inds:
        direction=1 if c[i]>rh+p['break_atr']*ar else (-1 if c[i]<rl-p['break_atr']*ar else 0)
        if direction==0:continue
        if p['trend_filter'] and trend!=direction:continue
        if p['direction']=='long' and direction<0:continue
        if p['direction']=='short' and direction>0:continue
        level=rh if direction==1 else rl
        ri=None
        for j in range(i+1,min(n,i+1+p['retest_bars'])):
            touched=(l[j]<=level+p['touch_atr']*ar) if direction==1 else (h[j]>=level-p['touch_atr']*ar)
            reclaim=(c[j]>level) if direction==1 else (c[j]<level)
            mom=(c[j]>e9[j] and e9[j]>e20[j]) if direction==1 else (c[j]<e9[j] and e9[j]<e20[j])
            if touched and reclaim and (not p['ema_confirm'] or mom):ri=j;break
        if ri is None:continue
        ei=ri+1
        if ei>=n or m[ei]>p['entry_cutoff']:continue
        entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
        stop=(level-p['stop_atr']*ar) if direction==1 else (level+p['stop_atr']*ar)
        if not valid_risk(entry,stop,p['max_stop_pct']):continue
        risk=abs(entry-stop);target=entry+direction*p['target_R']*risk
        return exit_trade(day,ei,direction,stop,target,p['slip_bps'])
    return None

def strat_gap_pullback(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day;n=len(o)
    pc=meta.get('pc',np.nan)
    oi=np.where(m==570)[0]
    if len(oi)==0 or not np.isfinite(pc) or pc<=0:return None
    ix=oi[0];gap=o[ix]/pc-1
    if abs(gap)<p['gap_min'] or abs(gap)>p['gap_max']:return None
    direction=1 if gap>0 else -1
    if p['direction']=='long' and direction<0:return None
    if p['direction']=='short' and direction>0:return None
    # Require opening confirmation in gap direction.
    ci=np.where((m>=570)&(m<570+p['confirm_min']))[0]
    if len(ci)<2:return None
    move=(c[ci[-1]]/o[ix]-1)*direction
    if move<p['open_confirm']:return None
    trend=0
    if np.isfinite(meta.get('ma20',np.nan)):trend=1 if pc>meta['ma20'] else -1
    if p['trend_filter'] and trend!=direction:return None
    ar=float(np.nanmedian(atr[ci[-3:]]));
    if not np.isfinite(ar) or ar<=0:return None
    inds=np.where((m>=570+p['confirm_min'])&(m<=p['entry_cutoff']))[0]
    for j in inds:
        # Pullback to EMA9/20 while retaining gap direction.
        near=(l[j]<=e9[j]+p['touch_atr']*ar) if direction==1 else (h[j]>=e9[j]-p['touch_atr']*ar)
        reclaim=(c[j]>e9[j] and c[j]>pc) if direction==1 else (c[j]<e9[j] and c[j]<pc)
        slope=(e9[j]>e20[j]) if direction==1 else (e9[j]<e20[j])
        if near and reclaim and (not p['ema_confirm'] or slope):
            ei=j+1
            if ei>=n:return None
            entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
            stop=(e20[j]-p['stop_atr']*ar) if direction==1 else (e20[j]+p['stop_atr']*ar)
            if not valid_risk(entry,stop,p['max_stop_pct']):return None
            risk=abs(entry-stop);target=entry+direction*p['target_R']*risk
            return exit_trade(day,ei,direction,stop,target,p['slip_bps'])
    return None

def strat_trend_pullback(day,p):
    d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day;n=len(o)
    # Determine an opening drive after N minutes.
    oi=np.where(m==570)[0]
    ci=np.where((m>=570)&(m<570+p['drive_min']))[0]
    if len(oi)==0 or len(ci)<2:return None
    ix=oi[0]; ar=float(np.nanmedian(atr[ci[-3:]]))
    if not np.isfinite(ar) or ar<=0:return None
    drive=(c[ci[-1]]-o[ix])/ar
    if abs(drive)<p['drive_atr']:return None
    direction=1 if drive>0 else -1
    if p['direction']=='long' and direction<0:return None
    if p['direction']=='short' and direction>0:return None
    trend=0;pc=meta.get('pc',np.nan);ma20=meta.get('ma20',np.nan)
    if np.isfinite(pc) and np.isfinite(ma20):trend=1 if pc>ma20 else -1
    if p['trend_filter'] and trend!=direction:return None
    inds=np.where((m>=570+p['drive_min'])&(m<=p['entry_cutoff']))[0]
    for j in inds:
        near=(l[j]<=e20[j]+p['touch_atr']*ar) if direction==1 else (h[j]>=e20[j]-p['touch_atr']*ar)
        reclaim=(c[j]>e9[j] and e9[j]>e20[j]) if direction==1 else (c[j]<e9[j] and e9[j]<e20[j])
        strong=((c[j]-o[j])/max(h[j]-l[j],1e-9)>=p['body_frac']) if direction==1 else ((o[j]-c[j])/max(h[j]-l[j],1e-9)>=p['body_frac'])
        if near and reclaim and strong:
            ei=j+1
            if ei>=n:return None
            entry=float(o[ei])*(1+direction*p['slip_bps']/10000)
            stop=(l[j]-p['stop_atr']*ar) if direction==1 else (h[j]+p['stop_atr']*ar)
            if not valid_risk(entry,stop,p['max_stop_pct']):return None
            risk=abs(entry-stop);target=entry+direction*p['target_R']*risk
            return exit_trade(day,ei,direction,stop,target,p['slip_bps'])
    return None

FUNCS={'premarket_retest':strat_premarket_retest,'orb_retest':strat_orb_retest,'gap_pullback':strat_gap_pullback,'trend_pullback':strat_trend_pullback}

def bt(days,fam,p,y0,y1):
    f=FUNCS[fam];out=[]
    for day in days:
        if y0<=day[0].year<=y1:
            x=f(day,p)
            if x:x['family']=fam;out.append(x)
    return out

def met(rows):
    if not rows:return {'n':0,'win':np.nan,'avgR':np.nan,'pf':np.nan,'maxddR':np.nan,'totalR':0}
    r=np.array([x['R'] for x in rows]);pos=r[r>0].sum();neg=-r[r<0].sum();eq=np.cumsum(r);dd=eq-np.maximum.accumulate(eq)
    return {'n':int(len(r)),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pos/neg if neg>0 else 999),'maxddR':float(dd.min()),'totalR':float(r.sum())}

def sim(rows,rf=.02):
    b=200.;pk=b;dd=0.
    for x in rows:b=max(0,b*(1+rf*x['R']));pk=max(pk,b);dd=min(dd,b/pk-1)
    return b,dd

def sample_params(n=3000):
    rng=np.random.default_rng(2026081507);base={'slip_bps':1.0,'max_stop_pct':.012}
    families=[]
    for _ in range(n):
        fam=['premarket_retest','orb_retest','gap_pullback','trend_pullback'][int(rng.integers(4))];p=base.copy();p['direction']=['both','long','short'][int(rng.integers(3))];p['trend_filter']=bool(rng.integers(2));p['target_R']=[.75,1.0,1.25,1.5][int(rng.integers(4))];p['stop_atr']=[0,.1,.2,.3][int(rng.integers(4))];p['touch_atr']=[0,.1,.2,.3][int(rng.integers(4))];p['entry_cutoff']=[660,690,720,750][int(rng.integers(4))];p['ema_confirm']=bool(rng.integers(2))
        if fam=='premarket_retest':
            p.update(pm_start=[420,450,480,510][int(rng.integers(4))],min_range_atr=[1.5,2,3][int(rng.integers(3))],max_range_atr=[5,7,9,12][int(rng.integers(4))],break_atr=[0,.1,.2,.3][int(rng.integers(4))],break_cutoff=[630,660,690][int(rng.integers(3))],retest_bars=[2,3,4,6][int(rng.integers(4))])
        elif fam=='orb_retest':
            p.update(orb_min=[15,30,45,60][int(rng.integers(4))],max_or_atr=[2,3,4,5][int(rng.integers(4))],break_atr=[0,.1,.2,.3][int(rng.integers(4))],break_cutoff=[660,690,720][int(rng.integers(3))],retest_bars=[2,3,4,6][int(rng.integers(4))])
        elif fam=='gap_pullback':
            p.update(gap_min=[.002,.003,.005,.0075][int(rng.integers(4))],gap_max=[.015,.02,.03,.05][int(rng.integers(4))],confirm_min=[15,30,45][int(rng.integers(3))],open_confirm=[0,.001,.002,.003][int(rng.integers(4))])
            if p['gap_min']>=p['gap_max']:continue
        else:
            p.update(drive_min=[15,30,45,60][int(rng.integers(4))],drive_atr=[.5,.75,1,1.5,2][int(rng.integers(5))],body_frac=[.2,.35,.5,.65][int(rng.integers(4))])
        families.append((fam,p))
    return families

def select(train_days):
    survivors=[]
    for i,(fam,p) in enumerate(sample_params(),1):
        tr=bt(train_days,fam,p,2019,2022);tm=met(tr)
        if tm['n']<40 or tm['win']<.54 or tm['avgR']<=.04 or tm['pf']<1.12:continue
        a=met(bt(train_days,fam,p,2019,2020));b=met(bt(train_days,fam,p,2021,2022))
        if a['n']<15 or b['n']<15 or a['avgR']<=0 or b['avgR']<=0:continue
        survivors.append((fam,p,tm,a,b))
        if i%500==0:print('SEARCH',i,'SURV',len(survivors),flush=True)
    print('TRAIN_SURVIVORS',len(survivors),flush=True)
    valid=[]
    for fam,p,tm,a,b in survivors:
        vr=bt(train_days,fam,p,2023,2025);vm=met(vr);v23=met(bt(train_days,fam,p,2023,2023));v24=met(bt(train_days,fam,p,2024,2024));v25=met(bt(train_days,fam,p,2025,2025))
        if vm['n']<25 or vm['win']<.58 or vm['avgR']<=.06 or vm['pf']<1.20:continue
        # Require positive expectancy in at least 2 of 3 recent calendar years and no catastrophic year.
        yrs=[v23,v24,v25];pos=sum(x['avgR']>0 for x in yrs if x['n']>=5)
        if pos<2 or any(x['n']>=5 and x['avgR']<-.25 for x in yrs):continue
        # Rank stability first, not in-sample profit.
        floor=min(tm['win'],vm['win']);score=4*floor+1.5*min(tm['avgR'],vm['avgR'])+.2*min(tm['pf'],vm['pf'])+.0005*min(tm['n']+vm['n'],300)+.005*max(tm['maxddR'],vm['maxddR'])
        valid.append((score,fam,p,tm,vm,a,b,v23,v24,v25))
    valid.sort(key=lambda z:z[0],reverse=True)
    return valid

def main(train_path,test_path):
    os.makedirs('confidence_results',exist_ok=True)
    train=prep(load(train_path));test=prep(load(test_path));print('TRAIN_DAYS',len(train),'TEST_DAYS',len(test),flush=True)
    valid=select(train);print('VALID_CANDIDATES',len(valid),flush=True)
    top=[]
    for rank,z in enumerate(valid[:25],1):
        score,fam,p,tm,vm,a,b,v23,v24,v25=z
        hr=bt(test,fam,p,2026,2026);hm=met(hr);bal,dd=sim(hr,.02)
        row={'rank':rank,'family':fam,'score':score,'params':json.dumps(p,sort_keys=True),'train':tm,'validation':vm,'y2023':v23,'y2024':v24,'y2025':v25,'holdout2026':hm,'end200_2pct':bal,'dd200_2pct':dd*100}
        top.append(row);print('CANDIDATE',json.dumps(row),flush=True)
    if not top: print('NO_CANDIDATES'); return
    # Winner must meet holdout target; then maximize robustness and holdout sample size.
    passed=[x for x in top if x['holdout2026']['n']>=8 and x['holdout2026']['win']>=.60 and x['holdout2026']['avgR']>0 and x['holdout2026']['pf']>=1.2]
    print('HOLDOUT_PASSED',len(passed),flush=True)
    if passed:
        winner=sorted(passed,key=lambda x:(x['holdout2026']['win'],x['holdout2026']['pf'],x['holdout2026']['n'],x['validation']['win']),reverse=True)[0]
        print('WINNER',json.dumps(winner),flush=True)
        fam=winner['family'];p=json.loads(winner['params']);tr=bt(test,fam,p,2026,2026)
        pd.DataFrame(tr).to_csv('confidence_results/winner_2026_trades.csv',index=False)
        json.dump(winner,open('confidence_results/winner.json','w'),indent=2)
    flat=[]
    for x in top:
        flat.append({'rank':x['rank'],'family':x['family'],'params':x['params'],**{f'train_{k}':v for k,v in x['train'].items()},**{f'val_{k}':v for k,v in x['validation'].items()},**{f'h26_{k}':v for k,v in x['holdout2026'].items()},'end200_2pct':x['end200_2pct'],'dd200_2pct':x['dd200_2pct']})
    pd.DataFrame(flat).to_csv('confidence_results/top25.csv',index=False)
if __name__=='__main__':main(sys.argv[1],sys.argv[2])