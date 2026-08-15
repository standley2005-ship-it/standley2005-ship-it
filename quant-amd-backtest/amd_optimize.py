import pandas as pd, numpy as np, sys, json, os


def load(path):
    df=pd.read_csv(path)
    cols={c.lower().strip():c for c in df.columns}
    if 'ds' in cols: ts=df[cols['ds']]
    elif 'datetime' in cols: ts=df[cols['datetime']]
    elif 'timestamp' in cols: ts=df[cols['timestamp']]
    elif 'date' in cols and 'time' in cols: ts=df[cols['date']].astype(str)+' '+df[cols['time']].astype(str)
    elif 'date' in cols: ts=df[cols['date']]
    else: raise ValueError(df.columns)
    out=pd.DataFrame({'ts':pd.to_datetime(ts,errors='coerce')})
    for k in ['open','high','low','close']:
        if k not in cols: raise ValueError(f'missing {k}: {df.columns}')
        out[k]=pd.to_numeric(df[cols[k]],errors='coerce')
    out=out.dropna().sort_values('ts').drop_duplicates('ts')
    out=out[out.ts.dt.dayofweek<5]
    out['minute']=out.ts.dt.hour*60+out.ts.dt.minute
    out=out[(out.minute>=570)&(out.minute<=960)].copy()
    out['date']=out.ts.dt.date
    return out


def prep_days(df):
    daily=df.groupby('date').close.last().to_frame('dclose')
    daily['sma20_prev']=daily.dclose.rolling(20).mean().shift(1)
    daily['prev_close']=daily.dclose.shift(1)
    trend=np.where(daily.sma20_prev.isna(),0,np.where(daily.prev_close>daily.sma20_prev,1,-1))
    tmap=dict(zip(daily.index,trend)); days=[]
    for d,g in df.groupby('date',sort=True):
        if len(g)<70: continue
        g=g.sort_values('ts'); o=g.open.to_numpy(float); h=g.high.to_numpy(float); l=g.low.to_numpy(float); c=g.close.to_numpy(float)
        mins=g.minute.to_numpy(int); ts=g.ts.to_numpy(); med=max(float(np.median(np.abs(c[:30]-o[:30]))),1e-6)
        days.append((d,int(tmap.get(d,0)),med,mins,ts,o,h,l,c))
    return days


def trade_day(day,p):
    d,trend,med_body,mins,ts,o,h,l,c=day; n=len(o); acc_end=570+p['acc_min']
    ai=np.where((mins>=570)&(mins<acc_end))[0]
    if len(ai)<max(2,p['acc_min']//5-1): return None
    rh=float(h[ai].max()); rl=float(l[ai].min()); rw=rh-rl
    if rw<=0:return None
    rwp=rw/float(o[ai[0]])
    if not(p['min_range_pct']<=rwp<=p['max_range_pct']):return None
    pi=np.where((mins>=acc_end)&(mins<=p['sweep_cutoff']))[0]; depth=p['sweep_depth']*rw
    for i in pi:
        ls=l[i]<=rl-depth; hs=h[i]>=rh+depth
        if ls==hs: continue
        direction=1 if ls else -1
        if p['direction']=='long' and direction<0:continue
        if p['direction']=='short' and direction>0:continue
        if p['trend_filter'] and trend!=0 and direction!=trend:continue
        sweep=float(l[i] if direction==1 else h[i]); rec=None
        for j in range(i,min(i+p['reclaim_bars']+1,n)):
            if (direction==1 and c[j]>rl) or (direction==-1 and c[j]<rh):rec=j;break
            sweep=min(sweep,float(l[j])) if direction==1 else max(sweep,float(h[j]))
        if rec is None:continue
        conf=None
        for j in range(rec+1,min(rec+1+p['confirm_bars'],n)):
            body=abs(c[j]-o[j]); span=max(h[j]-l[j],1e-9); a=max(0,j-p['break_lookback'])
            if direction==1: okay=c[j]>h[a:j].max() and body>=p['disp_mult']*med_body and (h[j]-c[j])/span<=p['close_edge']
            else: okay=c[j]<l[a:j].min() and body>=p['disp_mult']*med_body and (c[j]-l[j])/span<=p['close_edge']
            if okay:conf=j;break
        if conf is None or conf+1>=n:continue
        ei=conf+1
        if mins[ei]>p['entry_cutoff']:continue
        raw=float(o[ei]); entry=raw*(1+p['slip_bps']/10000*direction)
        if direction==1: stop=sweep-p['stop_buffer']*rw; risk=entry-stop; target=entry+p['target_R']*risk
        else: stop=sweep+p['stop_buffer']*rw; risk=stop-entry; target=entry-p['target_R']*risk
        if risk<=0 or risk/entry>p['max_stop_pct']:continue
        xp=None; reason='time'; xi=n-1
        for j in range(ei,n):
            if direction==1: hit_s=l[j]<=stop; hit_t=h[j]>=target
            else: hit_s=h[j]>=stop; hit_t=l[j]<=target
            if hit_s:xp=stop;reason='stop';xi=j;break
            if hit_t:xp=target;reason='target';xi=j;break
            if mins[j]>=p['time_exit']:xp=float(c[j]);reason='time';xi=j;break
        if xp is None:xp=float(c[-1])
        xnet=xp*(1-p['slip_bps']/10000*direction); R=((xnet-entry)*direction)/risk
        return {'R':float(R),'dir':direction,'reason':reason,'date':d,'entry_ts':str(ts[ei]),'exit_ts':str(ts[xi]),'entry':entry,'stop':stop,'target':target}
    return None


def bt(days,p,y0,y1):
    rows=[]
    for day in days:
        if y0<=day[0].year<=y1:
            t=trade_day(day,p)
            if t:rows.append(t)
    return rows


def met(rows):
    if not rows:return {'n':0,'win':np.nan,'avgR':np.nan,'pf':np.nan,'maxddR':np.nan,'totalR':0}
    r=np.array([x['R'] for x in rows],float); pos=r[r>0].sum(); neg=-r[r<0].sum(); pf=pos/neg if neg>0 else 999
    eq=np.cumsum(r); dd=eq-np.maximum.accumulate(eq)
    return {'n':int(len(r)),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pf),'maxddR':float(dd.min()),'totalR':float(r.sum())}


def sc(m,minn=40):
    if m['n']<minn or not np.isfinite(m['avgR']) or m['avgR']<=0:return -999
    return m['avgR']*2+(min(m['pf'],3)-1)*.35+min(m['n'],250)/1000+m['maxddR']*.01


def sim(rows,rf=.05,start=200):
    bal=start; peak=bal; mdd=0
    for x in rows:
        bal=max(0,bal*(1+rf*x['R'])); peak=max(peak,bal); mdd=min(mdd,bal/peak-1)
    return bal,mdd


def sample_params(n=1400,seed=20260815):
    rng=np.random.default_rng(seed); base=dict(close_edge=.30,slip_bps=1.0,max_stop_pct=.015,time_exit=955)
    choices={'acc_min':[15,30,45,60],'sweep_depth':[0,.05,.10,.20],'reclaim_bars':[0,1,2],'confirm_bars':[1,2,3],'disp_mult':[1,1.25,1.5,2],'break_lookback':[2,3,4],'target_R':[1.5,2,2.5,3],'stop_buffer':[0,.05,.10],'sweep_cutoff':[660,690,720],'entry_cutoff':[720,750],'trend_filter':[False,True],'direction':['both','long','short'],'min_range_pct':[.001,.002],'max_range_pct':[.008,.012,.016]}
    out=[];seen=set()
    while len(out)<n:
        p=base.copy()
        for k,v in choices.items():p[k]=v[int(rng.integers(len(v)))]
        if p['min_range_pct']>=p['max_range_pct']:continue
        key=tuple((k,p[k]) for k in sorted(choices))
        if key not in seen:seen.add(key);out.append(p)
    return out


def main(path):
    os.makedirs('results',exist_ok=True); df=load(path); days=prep_days(df)
    print('DATA',len(df),'rows',df.date.min(),'to',df.date.max(),'complete_days',len(days),flush=True)
    survivors=[]
    for q,p in enumerate(sample_params(),1):
        tr=bt(days,p,2018,2021); m=met(tr); s=sc(m)
        if s>-999:
            a=met(bt(days,p,2018,2019)); b=met(bt(days,p,2020,2021))
            if a['n']>=15 and b['n']>=15 and a['avgR']>0 and b['avgR']>0:survivors.append((s,p,m,a,b))
        if q%200==0:print('TRAIN_PROGRESS',q,'survivors',len(survivors),flush=True)
    survivors=sorted(survivors,key=lambda z:z[0],reverse=True)[:180]; print('TRAIN_SURVIVORS',len(survivors),flush=True)
    val=[]
    for s,p,m,a,b in survivors:
        vm=met(bt(days,p,2022,2023)); vs=sc(vm,30)
        if vs>-999 and vm['pf']>1:val.append((vs+min(s,2)*.1,p,m,vm,a,b))
    if not val:print('NO_ROBUST_CANDIDATE');sys.exit(2)
    val.sort(key=lambda z:z[0],reverse=True); _,p,tm,vm,a,b=val[0]
    test=bt(days,p,2024,2024); xm=met(test); full=bt(days,p,2018,2024); fm=met(full); bal,mdd=sim(test)
    print('FROZEN_PARAMS',json.dumps(p,sort_keys=True),flush=True)
    print('TRAIN_2018_21',json.dumps(tm),flush=True); print('TRAIN_2018_19',json.dumps(a),flush=True); print('TRAIN_2020_21',json.dumps(b),flush=True)
    print('VALID_2022_23',json.dumps(vm),flush=True); print('TEST_2024',json.dumps(xm),flush=True); print('FULL_2018_24',json.dumps(fm),flush=True)
    print('TEST_200_ACCOUNT',json.dumps({'start':200,'planned_risk_frac':.05,'end':bal,'maxdd_pct':mdd*100}),flush=True)
    years=[]
    for y in range(2018,2025):
        rr=bt(days,p,y,y); mm=met(rr); yb,yd=sim(rr); years.append({'year':y,**mm,'end200':yb,'acctdd_pct':yd*100})
    print('YEAR_BREAKDOWN',json.dumps(years),flush=True)
    pd.DataFrame(test).to_csv('results/frozen_2024_trades.csv',index=False); pd.DataFrame(years).to_csv('results/year_breakdown.csv',index=False)
    top=[]
    for rank,(vs,pp,tmm,vmm,aa,bb) in enumerate(val[:20],1):
        xx=met(bt(days,pp,2024,2024)); top.append({'rank':rank,**pp,**{f'train_{k}':v for k,v in tmm.items()},**{f'val_{k}':v for k,v in vmm.items()},**{f'test_{k}':v for k,v in xx.items()}})
    pd.DataFrame(top).to_csv('results/top20_robustness.csv',index=False)
    json.dump({'params':p,'train':tm,'validation':vm,'test':xm,'full':fm,'account200':{'end':bal,'maxdd_pct':mdd*100}},open('results/summary.json','w'),indent=2)

if __name__=='__main__':main(sys.argv[1])
