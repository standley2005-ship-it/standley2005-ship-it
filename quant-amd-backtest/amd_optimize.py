import pandas as pd, numpy as np, itertools, sys, json, os


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
    mins=out.ts.dt.hour*60+out.ts.dt.minute
    out=out[(mins>=570)&(mins<=960)].copy()
    out['date']=out.ts.dt.date
    return out


def prep_days(df):
    daily=df.groupby('date').agg(dclose=('close','last'))
    daily['sma20_prev']=daily.dclose.rolling(20).mean().shift(1)
    daily['prev_close']=daily.dclose.shift(1)
    trend=(daily.prev_close>daily.sma20_prev).map({True:1,False:-1})
    trend[daily.sma20_prev.isna()]=0
    days=[]
    for d,g in df.groupby('date',sort=True):
        g=g.sort_values('ts').reset_index(drop=True)
        if len(g)<70: continue
        med_body=max(float((g.close-g.open).abs().iloc[:30].median()),1e-6)
        days.append((d,g,int(trend.get(d,0)),med_body))
    return days


def trade_day(g,trend,med_body,p):
    acc_end=570+p['acc_min']
    mins=g.ts.dt.hour*60+g.ts.dt.minute
    acc=g[(mins>=570)&(mins<acc_end)]
    if len(acc)<max(2,p['acc_min']//5-1): return None
    rh=float(acc.high.max()); rl=float(acc.low.min()); rw=rh-rl
    if rw<=0: return None
    rwp=rw/float(acc.open.iloc[0])
    if rwp<p['min_range_pct'] or rwp>p['max_range_pct']: return None
    post=g[(mins>=acc_end)&(mins<=p['sweep_cutoff'])]
    depth=p['sweep_depth']*rw
    for i in post.index:
        row=g.loc[i]
        low_sweep=row.low<=rl-depth; high_sweep=row.high>=rh+depth
        if low_sweep and high_sweep: continue
        if not(low_sweep or high_sweep): continue
        direction=1 if low_sweep else -1
        if p['direction']=='long' and direction<0: continue
        if p['direction']=='short' and direction>0: continue
        if p['trend_filter'] and trend!=0 and direction!=trend: continue
        sweep_ext=float(row.low if direction==1 else row.high)
        reclaim_idx=None
        for j in range(i,min(i+p['reclaim_bars']+1,len(g))):
            c=float(g.loc[j,'close'])
            if (direction==1 and c>rl) or (direction==-1 and c<rh):
                reclaim_idx=j; break
            sweep_ext=min(sweep_ext,float(g.loc[j,'low'])) if direction==1 else max(sweep_ext,float(g.loc[j,'high']))
        if reclaim_idx is None: continue
        conf=None
        for j in range(reclaim_idx+1,min(reclaim_idx+1+p['confirm_bars'],len(g))):
            r=g.loc[j]; body=abs(float(r.close-r.open)); span=max(float(r.high-r.low),1e-9)
            look=g.loc[max(0,j-p['break_lookback']):j-1]
            if look.empty: continue
            if direction==1:
                okay=(r.close>float(look.high.max()) and body>=p['disp_mult']*med_body and (r.high-r.close)/span<=p['close_edge'])
            else:
                okay=(r.close<float(look.low.min()) and body>=p['disp_mult']*med_body and (r.close-r.low)/span<=p['close_edge'])
            if okay: conf=j; break
        if conf is None or conf+1>=len(g): continue
        entry_i=conf+1
        em=int(g.loc[entry_i,'ts'].hour*60+g.loc[entry_i,'ts'].minute)
        if em>p['entry_cutoff']: continue
        raw_entry=float(g.loc[entry_i,'open'])
        entry=raw_entry*(1+p['slip_bps']/10000*direction)
        if direction==1:
            stop=sweep_ext-p['stop_buffer']*rw; risk=entry-stop; target=entry+p['target_R']*risk
        else:
            stop=sweep_ext+p['stop_buffer']*rw; risk=stop-entry; target=entry-p['target_R']*risk
        if risk<=0 or risk/entry>p['max_stop_pct']: continue
        exit_px=None; reason=None; exit_i=None
        for j in range(entry_i,len(g)):
            m=int(g.loc[j,'ts'].hour*60+g.loc[j,'ts'].minute); r=g.loc[j]
            if direction==1: hs=r.low<=stop; ht=r.high>=target
            else: hs=r.high>=stop; ht=r.low<=target
            if hs: exit_px=stop; reason='stop'; exit_i=j; break
            if ht: exit_px=target; reason='target'; exit_i=j; break
            if m>=p['time_exit']: exit_px=float(r.close); reason='time'; exit_i=j; break
        if exit_px is None: exit_i=len(g)-1; exit_px=float(g.iloc[-1].close); reason='time'
        exit_net=exit_px*(1-p['slip_bps']/10000*direction)
        R=((exit_net-entry)*direction)/risk
        return {'R':R,'dir':direction,'reason':reason,'entry_ts':g.loc[entry_i,'ts'],'exit_ts':g.loc[exit_i,'ts'],'entry':entry,'stop':stop,'target':target,'range_width':rw,'sweep_ext':sweep_ext}
    return None


def backtest(days,p,start_year,end_year):
    rows=[]
    for d,g,tr,mb in days:
        if start_year<=d.year<=end_year:
            t=trade_day(g,tr,mb,p)
            if t: t['date']=d; rows.append(t)
    return pd.DataFrame(rows)


def metrics(t):
    if len(t)==0:return {'n':0,'win':np.nan,'avgR':np.nan,'pf':np.nan,'maxddR':np.nan,'totalR':0}
    r=t.R.astype(float); pos=r[r>0].sum(); neg=-r[r<0].sum(); pf=pos/neg if neg>0 else 999
    eq=r.cumsum(); dd=eq-eq.cummax()
    return {'n':len(r),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pf),'maxddR':float(dd.min()),'totalR':float(r.sum())}


def score(m):
    if m['n']<40 or not np.isfinite(m['avgR']) or m['avgR']<=0:return -999
    return m['avgR']*2+(min(m['pf'],3)-1)*.35+min(m['n'],250)/1000+m['maxddR']*.01


def simulate_200(t,risk_frac=.05,start=200):
    bal=start; peak=bal; maxdd=0
    for R in t.R:
        bal=max(0,bal*(1+risk_frac*R)); peak=max(peak,bal); maxdd=min(maxdd,bal/peak-1)
    return bal,maxdd


def main(path,outdir='results'):
    os.makedirs(outdir,exist_ok=True)
    df=load(path); print('rows',len(df),'dates',df.date.min(),df.date.max())
    days=prep_days(df); print('complete days',len(days))
    base=dict(close_edge=.30,slip_bps=1.0,max_stop_pct=.015,time_exit=955)
    rng=np.random.default_rng(20260815)
    choices={'acc_min':[15,30,45,60],'sweep_depth':[0,.05,.10,.20],'reclaim_bars':[0,1,2],'confirm_bars':[1,2,3],'disp_mult':[1,1.25,1.5,2],'break_lookback':[2,3,4],'target_R':[1.5,2,2.5,3],'stop_buffer':[0,.05,.10],'sweep_cutoff':[660,690,720],'entry_cutoff':[720,750],'trend_filter':[False,True],'direction':['both','long','short'],'min_range_pct':[.001,.002],'max_range_pct':[.008,.012,.016]}
    params=[]; seen=set()
    while len(params)<700:
        p={**base}
        for k,v in choices.items():p[k]=v[int(rng.integers(len(v)))]
        if p['min_range_pct']>=p['max_range_pct']:continue
        key=tuple((k,p[k]) for k in sorted(choices))
        if key in seen:continue
        seen.add(key);params.append(p)
    grid=[]
    for p in params:
        tr=backtest(days,p,2018,2021);m=metrics(tr);s=score(m)
        if s<=-999:continue
        a=metrics(backtest(days,p,2018,2019));b=metrics(backtest(days,p,2020,2021))
        if a['n']<15 or b['n']<15 or a['avgR']<=0 or b['avgR']<=0:continue
        grid.append((s,p,m))
    print('viable train combos',len(grid))
    grid=sorted(grid,key=lambda x:x[0],reverse=True)[:120]
    valrows=[]
    for ts,p,tm in grid:
        vm=metrics(backtest(days,p,2022,2023));vs=score(vm)
        if tm['avgR']>0 and vm['avgR']>0 and tm['pf']>1 and vm['pf']>1 and vm['n']>=30:
            valrows.append((vs+min(ts,2)*.10,p,tm,vm))
    if not valrows:print('NO ROBUST CANDIDATE SURVIVED VALIDATION');sys.exit(2)
    valrows=sorted(valrows,key=lambda x:x[0],reverse=True)
    _,p,tm,vm=valrows[0]
    test=backtest(days,p,2024,2024);xm=metrics(test);full=backtest(days,p,2018,2024);fm=metrics(full)
    b200,dd200=simulate_200(test,.05,200)
    print('\nFROZEN BEST PARAMS (chosen before 2024 test)');print(json.dumps(p,indent=2))
    print('TRAIN 2018-21',tm);print('VALID 2022-23',vm);print('TEST 2024',xm);print('FULL 2018-24',fm)
    print('2024 $200 @ 5% planned risk/trade =>',round(b200,2),'max account DD',round(dd200*100,2),'%')
    years=[]
    for y in range(2018,2025):
        tt=backtest(days,p,y,y);mm=metrics(tt);bal,dd=simulate_200(tt,.05,200);years.append({'year':y,**mm,'$200_end_5pct':bal,'acct_dd_pct':dd*100})
    yd=pd.DataFrame(years);print('\nYEAR BREAKDOWN\n',yd.to_string(index=False))
    tops=[]
    for rank,(rs,pp,tmm,vmm) in enumerate(valrows[:20],1):
        xmm=metrics(backtest(days,pp,2024,2024));tops.append({'rank':rank,**pp,**{f'train_{k}':v for k,v in tmm.items()},**{f'val_{k}':v for k,v in vmm.items()},**{f'test_{k}':v for k,v in xmm.items()}})
    pd.DataFrame(tops).to_csv(f'{outdir}/top20_robustness.csv',index=False);test.to_csv(f'{outdir}/frozen_2024_trades.csv',index=False);yd.to_csv(f'{outdir}/year_breakdown.csv',index=False)
    with open(f'{outdir}/best_params.json','w') as f:json.dump(p,f,indent=2)
    with open(f'{outdir}/summary.json','w') as f:json.dump({'params':p,'train':tm,'validation':vm,'test_2024':xm,'full':fm,'test_200_start':200,'test_200_end':b200,'test_200_maxdd_pct':dd200*100},f,indent=2,default=str)

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'qqq5m.csv')
