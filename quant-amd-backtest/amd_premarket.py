import pandas as pd, numpy as np, sys, json, os

def load(path):
    df=pd.read_csv(path,low_memory=False); cols={c.lower().strip():c for c in df.columns}
    if 'ds' in cols: ts=df[cols['ds']]
    elif 'datetime' in cols: ts=df[cols['datetime']]
    elif 'timestamp' in cols: ts=df[cols['timestamp']]
    elif 'date' in cols and 'time' in cols: ts=df[cols['date']].astype(str)+' '+df[cols['time']].astype(str)
    elif 'date' in cols: ts=df[cols['date']]
    else: raise ValueError(df.columns)
    out=pd.DataFrame({'ts':pd.to_datetime(ts,errors='coerce')})
    for k in ['open','high','low','close']: out[k]=pd.to_numeric(df[cols[k]],errors='coerce')
    out=out.dropna().sort_values('ts').drop_duplicates('ts'); out=out[out.ts.dt.dayofweek<5]
    out['minute']=out.ts.dt.hour*60+out.ts.dt.minute; out=out[(out.minute>=240)&(out.minute<=960)].copy(); out['date']=out.ts.dt.date
    return out

def prep(df):
    rth=df[(df.minute>=570)&(df.minute<=960)]; daily=rth.groupby('date').close.last().to_frame('dclose'); daily['ma20']=daily.dclose.rolling(20).mean().shift(1); daily['pc']=daily.dclose.shift(1)
    t=np.where(daily.ma20.isna(),0,np.where(daily.pc>daily.ma20,1,-1)); tmap=dict(zip(daily.index,t)); days=[]
    for d,g in df.groupby('date',sort=True):
        g=g.sort_values('ts')
        if ((g.minute>=570)&(g.minute<=960)).sum()<70:continue
        o=g.open.to_numpy(float);h=g.high.to_numpy(float);l=g.low.to_numpy(float);c=g.close.to_numpy(float);m=g.minute.to_numpy(int);ts=g.ts.to_numpy()
        prev=np.r_[o[0],c[:-1]];tr=np.maximum.reduce([h-l,np.abs(h-prev),np.abs(l-prev)]);atr=pd.Series(tr).rolling(14,min_periods=5).mean().to_numpy();ema=pd.Series(c).ewm(span=9,adjust=False).mean().to_numpy()
        days.append((d,int(tmap.get(d,0)),m,ts,o,h,l,c,atr,ema))
    return days

def one(day,p):
    d,trend,m,ts,o,h,l,c,atr,ema=day;n=len(o);a0,a1=p['acc_pair'];ai=np.where((m>=a0)&(m<a1))[0]
    if len(ai)<8:return None
    rh=float(h[ai].max());rl=float(l[ai].min());rw=rh-rl;ar=float(atr[ai[-1]])
    if not np.isfinite(ar) or ar<=0:return None
    if not(p['min_acc_atr']<=rw/ar<=p['max_acc_atr']):return None
    pi=np.where((m>=570)&(m<=p['sweep_cutoff']))[0];depth=p['sweep_atr']*ar
    for i in pi:
        ls=l[i]<=rl-depth;hs=h[i]>=rh+depth
        if ls==hs:continue
        direction=1 if ls else -1
        if p['direction']=='long' and direction<0:continue
        if p['direction']=='short' and direction>0:continue
        if p['trend_filter'] and trend!=0 and direction!=trend:continue
        sweep=float(l[i] if direction==1 else h[i]);rec=None
        for j in range(i,min(i+p['reclaim_bars']+1,n)):
            if (direction==1 and c[j]>rl) or (direction==-1 and c[j]<rh):rec=j;break
            sweep=min(sweep,float(l[j])) if direction==1 else max(sweep,float(h[j]))
        if rec is None:continue
        conf=None
        for j in range(rec+1,min(rec+1+p['confirm_bars'],n)):
            body=abs(c[j]-o[j]);span=max(h[j]-l[j],1e-9);a=max(0,j-p['break_lookback'])
            if direction==1:ok=c[j]>h[a:j].max() and body>=p['disp_atr']*ar and (h[j]-c[j])/span<=.30
            else:ok=c[j]<l[a:j].min() and body>=p['disp_atr']*ar and (c[j]-l[j])/span<=.30
            if ok:conf=j;break
        if conf is None:continue
        if p['entry_mode']=='next':ei=conf+1
        else:
            ei=None
            for j in range(conf+1,min(conf+1+p['ema_wait']+1,n)):
                if direction==1 and l[j]<=ema[j] and c[j]>ema[j]:ei=j+1;break
                if direction==-1 and h[j]>=ema[j] and c[j]<ema[j]:ei=j+1;break
            if ei is None:continue
        if ei>=n or m[ei]>p['entry_cutoff']:continue
        raw=float(o[ei]);entry=raw*(1+p['slip_bps']/10000*direction);buf=p['stop_atr']*ar
        if direction==1:stop=sweep-buf;risk=entry-stop;target=entry+p['target_R']*risk
        else:stop=sweep+buf;risk=stop-entry;target=entry-p['target_R']*risk
        if risk<=0 or risk/entry>p['max_stop_pct']:continue
        xp=None;reason='time';xi=n-1
        for j in range(ei,n):
            if m[j]<570:continue
            if direction==1:stop_hit=l[j]<=stop;target_hit=h[j]>=target
            else:stop_hit=h[j]>=stop;target_hit=l[j]<=target
            if stop_hit:xp=stop;reason='stop';xi=j;break
            if target_hit:xp=target;reason='target';xi=j;break
            if m[j]>=955:xp=float(c[j]);reason='time';xi=j;break
        if xp is None:xp=float(c[-1])
        xnet=xp*(1-p['slip_bps']/10000*direction);R=((xnet-entry)*direction)/risk
        return {'date':d,'R':float(R),'dir':direction,'reason':reason,'entry_ts':str(ts[ei]),'exit_ts':str(ts[xi]),'entry':entry,'stop':stop,'target':target}
    return None

def bt(days,p,y0,y1):
    r=[]
    for day in days:
        if y0<=day[0].year<=y1:
            x=one(day,p)
            if x:r.append(x)
    return r

def met(rows):
    if not rows:return {'n':0,'win':np.nan,'avgR':np.nan,'pf':np.nan,'maxddR':np.nan,'totalR':0}
    r=np.array([x['R'] for x in rows]);pos=r[r>0].sum();neg=-r[r<0].sum();pf=pos/neg if neg>0 else 999;eq=np.cumsum(r);dd=eq-np.maximum.accumulate(eq)
    return {'n':int(len(r)),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pf),'maxddR':float(dd.min()),'totalR':float(r.sum())}
def score(x,n=40):
    if x['n']<n or not np.isfinite(x['avgR']) or x['avgR']<=0:return -999
    return 2*x['avgR']+.35*(min(x['pf'],3)-1)+min(x['n'],250)/1000+.01*x['maxddR']
def sim(rows,rf=.05):
    b=200;pk=b;dd=0
    for x in rows:b=max(0,b*(1+rf*x['R']));pk=max(pk,b);dd=min(dd,b/pk-1)
    return b,dd

def params(n=1800):
    rng=np.random.default_rng(2026081502);base={'slip_bps':1.0,'max_stop_pct':.015}
    ch={'acc_pair':[(420,510),(450,540),(480,570),(510,570),(420,570)],'min_acc_atr':[1.5,2,3],'max_acc_atr':[5,7,9,12],'sweep_atr':[0,.1,.2,.3],'reclaim_bars':[0,1,2],'confirm_bars':[1,2,3],'disp_atr':[.6,.8,1.0,1.2],'break_lookback':[2,3,4],'entry_mode':['next','ema'],'ema_wait':[1,2,3,4],'target_R':[1.5,2,2.5,3],'stop_atr':[0,.1,.2],'sweep_cutoff':[630,660,690],'entry_cutoff':[690,720,750],'trend_filter':[False,True],'direction':['both','long','short']}
    out=[];seen=set()
    while len(out)<n:
        p=base.copy()
        for k,v in ch.items():p[k]=v[int(rng.integers(len(v)))]
        if p['min_acc_atr']>=p['max_acc_atr']:continue
        key=tuple((k,str(p[k])) for k in sorted(ch))
        if key not in seen:seen.add(key);out.append(p)
    return out

def main(path):
    os.makedirs('premarket_results',exist_ok=True);df=load(path);days=prep(df);print('DATA',len(df),df.date.min(),df.date.max(),'DAYS',len(days),flush=True);surv=[]
    for i,p in enumerate(params(),1):
        r=bt(days,p,2019,2022);mm=met(r);ss=score(mm)
        if ss>-999:
            a=met(bt(days,p,2019,2020));b=met(bt(days,p,2021,2022))
            if a['n']>=15 and b['n']>=15 and a['avgR']>0 and b['avgR']>0:surv.append((ss,p,mm,a,b))
        if i%300==0:print('TRAIN_PROGRESS',i,'SURV',len(surv),flush=True)
    surv=sorted(surv,key=lambda z:z[0],reverse=True)[:220];print('TRAIN_SURVIVORS',len(surv),flush=True);val=[]
    for ss,p,mm,a,b in surv:
        vm=met(bt(days,p,2023,2024));vs=score(vm,30)
        if vs>-999 and vm['pf']>1:val.append((vs+min(ss,2)*.1,p,mm,vm,a,b))
    if not val:print('NO_ROBUST_CANDIDATE');sys.exit(2)
    val.sort(key=lambda z:z[0],reverse=True);_,p,tm,vm,a,b=val[0];test=bt(days,p,2025,2025);xm=met(test);full=bt(days,p,2019,2025);fm=met(full);bal,dd=sim(test)
    print('FROZEN_PARAMS',json.dumps(p,sort_keys=True),flush=True);print('TRAIN_2019_22',json.dumps(tm),flush=True);print('TRAIN_2019_20',json.dumps(a),flush=True);print('TRAIN_2021_22',json.dumps(b),flush=True);print('VALID_2023_24',json.dumps(vm),flush=True);print('TEST_2025',json.dumps(xm),flush=True);print('FULL_2019_25',json.dumps(fm),flush=True);print('TEST_200_ACCOUNT',json.dumps({'start':200,'risk_frac':.05,'end':bal,'maxdd_pct':dd*100}),flush=True)
    years=[]
    for y in range(2019,2026):
        rr=bt(days,p,y,y);m=met(rr);yb,yd=sim(rr);years.append({'year':y,**m,'end200':yb,'acctdd_pct':yd*100})
    print('YEAR_BREAKDOWN',json.dumps(years),flush=True);pd.DataFrame(test).to_csv('premarket_results/frozen_2025_trades.csv',index=False);pd.DataFrame(years).to_csv('premarket_results/year_breakdown.csv',index=False);json.dump({'params':p,'train':tm,'validation':vm,'test':xm,'full':fm,'account200':{'end':bal,'maxdd_pct':dd*100}},open('premarket_results/summary.json','w'),indent=2)
    top=[]
    for rank,(vs,pp,tmm,vmm,aa,bb) in enumerate(val[:20],1):
        xx=met(bt(days,pp,2025,2025));top.append({'rank':rank,**{k:str(v) if isinstance(v,tuple) else v for k,v in pp.items()},**{f'train_{k}':v for k,v in tmm.items()},**{f'val_{k}':v for k,v in vmm.items()},**{f'test_{k}':v for k,v in xx.items()}})
    pd.DataFrame(top).to_csv('premarket_results/top20_robustness.csv',index=False)
if __name__=='__main__':main(sys.argv[1])
