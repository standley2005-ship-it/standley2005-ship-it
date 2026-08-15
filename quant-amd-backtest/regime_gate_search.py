import json, os, sys
import numpy as np
import pandas as pd
import yfinance as yf
import high_confidence_search as hc
import final_portfolio_eval as fp

SEED=2026081503


def met(df):
    return fp.metrics(df) if df is not None else fp.metrics(pd.DataFrame())


def sim(df, rf=.02):
    return fp.sim(df, rf) if df is not None else {'end':200.0,'maxdd_pct':0.0}


def daily_features(raw, days):
    x=raw.copy().sort_values('ts')
    rth=x[(x.minute>=570)&(x.minute<=960)].copy()
    daily=rth.groupby('date').agg(dopen=('open','first'),dclose=('close','last'),dhigh=('high','max'),dlow=('low','min'))
    daily['pc']=daily.dclose.shift(1)
    daily['ret1']=daily.dclose.pct_change().shift(1)
    daily['ret5']=daily.dclose.pct_change(5).shift(1)
    daily['ma20']=daily.dclose.rolling(20).mean().shift(1)
    daily['ma50']=daily.dclose.rolling(50).mean().shift(1)
    daily['trend20']=daily.pc/daily.ma20-1
    daily['trend50']=daily.pc/daily.ma50-1
    daily['rv20']=daily.dclose.pct_change().rolling(20).std().shift(1)*np.sqrt(252)
    out={}
    for day in days:
        d,meta,m,ts,o,h,l,c,v,atr,e9,e20,vwap=day
        if d not in daily.index: continue
        z=daily.loc[d]
        oi=np.where(m==570)[0]
        if len(oi)==0 or not np.isfinite(z.pc) or z.pc<=0: continue
        ix=oi[0]
        gap=float(o[ix]/z.pc-1)
        pi=np.where((m>=480)&(m<570))[0]
        if len(pi)>=6:
            pmret=float(c[pi[-1]]/o[pi[0]]-1)
            ar=float(np.nanmedian(atr[pi[-6:]]))
            pmrange=float((h[pi].max()-l[pi].min())/ar) if np.isfinite(ar) and ar>0 else np.nan
        else:
            pmret=np.nan; pmrange=np.nan
        out[str(d)]={
            'rv20':float(z.rv20) if np.isfinite(z.rv20) else np.nan,
            'ret5':float(z.ret5) if np.isfinite(z.ret5) else np.nan,
            'trend20':float(z.trend20) if np.isfinite(z.trend20) else np.nan,
            'trend50':float(z.trend50) if np.isfinite(z.trend50) else np.nan,
            'gap':gap,'pmret':pmret,'pmrange_atr':pmrange,
        }
    return out


def portfolio(days,y0,y1):
    return fp.evaluate(days,y0,y1)[2]


def attach(df, fmap):
    if df is None or len(df)==0: return pd.DataFrame()
    rows=[]
    for r in df.itertuples(index=False):
        d=str(r.date); f=fmap.get(d)
        if not f: continue
        z=r._asdict(); z.update(f); rows.append(z)
    return pd.DataFrame(rows)


def gate_mask(df,p):
    if len(df)==0:return np.array([],dtype=bool)
    req=['rv20','ret5','trend20','trend50','gap','pmret','pmrange_atr']
    m=np.ones(len(df),dtype=bool)
    for c in req:m &= np.isfinite(pd.to_numeric(df[c],errors='coerce').to_numpy(float))
    rv=np.abs(df.rv20.to_numpy(float)); r5=np.abs(df.ret5.to_numpy(float)); t20=np.abs(df.trend20.to_numpy(float)); t50=np.abs(df.trend50.to_numpy(float)); gap=np.abs(df.gap.to_numpy(float)); pmr=df.pmrange_atr.to_numpy(float); pma=np.abs(df.pmret.to_numpy(float))
    m &= (rv>=p['rv_min'])&(rv<=p['rv_max'])
    m &= r5<=p['ret5_max']
    m &= (t20>=p['trend20_min'])&(t20<=p['trend20_max'])
    m &= t50<=p['trend50_max']
    m &= gap<=p['gap_max']
    m &= (pmr>=p['pmrange_min'])&(pmr<=p['pmrange_max'])
    m &= pma<=p['pmret_max']
    return m


def apply(df,p):
    if len(df)==0:return df.copy()
    return df.loc[gate_mask(df,p)].copy().sort_values('date')


def sample(n=8000):
    rng=np.random.default_rng(SEED); seen=set(); out=[]
    vals={
      'rv_min':[0,.10,.14,.18], 'rv_max':[.18,.22,.26,.32,.40,1.0],
      'ret5_max':[.02,.035,.05,.075,.12,1.0],
      'trend20_min':[0,.003,.0075,.015,.025], 'trend20_max':[.02,.04,.06,.10,1.0],
      'trend50_max':[.03,.06,.10,.15,1.0], 'gap_max':[.003,.006,.01,.02,1.0],
      'pmrange_min':[0,.5,1.0,1.5], 'pmrange_max':[1.5,2.5,3.5,5.0,8.0,999.0],
      'pmret_max':[.003,.006,.01,.02,1.0],
    }
    keys=list(vals)
    while len(out)<n:
        p={k:vals[k][int(rng.integers(len(vals[k])))] for k in keys}
        if p['rv_min']>=p['rv_max'] or p['trend20_min']>=p['trend20_max'] or p['pmrange_min']>=p['pmrange_max']:continue
        k=json.dumps(p,sort_keys=True)
        if k not in seen:seen.add(k);out.append(p)
    return out


def download_recent():
    h=yf.Ticker('QQQ').history(period='60d',interval='5m',prepost=True,auto_adjust=False,actions=False)
    idx=pd.DatetimeIndex(h.index)
    if idx.tz is not None:idx=idx.tz_convert('America/New_York').tz_localize(None)
    d=pd.DataFrame({'timestamp':idx,'open':h.Open.to_numpy(),'high':h.High.to_numpy(),'low':h.Low.to_numpy(),'close':h.Close.to_numpy(),'volume':h.Volume.fillna(0).to_numpy()}).dropna(subset=['open','high','low','close'])
    d.to_csv('regime_recent_qqq.csv',index=False)
    return 'regime_recent_qqq.csv'


def pack(df):
    return {'metrics':met(df),'sim200_2pct':sim(df,.02),'dates':[str(x) for x in df.date.tolist()] if len(df) else []}


def main(train_path,early26_path):
    os.makedirs('regime_gate_results',exist_ok=True)
    raw=hc.load(train_path); days=hc.prep(raw); fmap=daily_features(raw,days)
    allp=attach(portfolio(days,2019,2025),fmap)
    tr=allp[pd.to_datetime(allp.date).dt.year.between(2019,2022)].copy()
    va=allp[pd.to_datetime(allp.date).dt.year.between(2023,2024)].copy()
    t25=allp[pd.to_datetime(allp.date).dt.year==2025].copy()
    print('BASE_TRAIN',json.dumps(met(tr)),'BASE_VAL',json.dumps(met(va)),'BASE_2025',json.dumps(met(t25)),flush=True)

    survivors=[]
    for p in sample():
        a=apply(tr,p); am=met(a)
        if am['n']<80 or am['win'] is None or am['win']<.63 or am['avgR']<.085 or am['pf']<1.28:continue
        # Must not simply erase the historically difficult 2021 period.
        y21=a[pd.to_datetime(a.date).dt.year==2021]; m21=met(y21)
        if m21['n']<15:continue
        survivors.append((p,am,m21))
    print('TRAIN_SURV',len(survivors),flush=True)

    valid=[]
    for p,am,m21 in survivors:
        b=apply(va,p); bm=met(b)
        if bm['n']<30 or bm['win'] is None or bm['win']<.63 or bm['avgR']<.085 or bm['pf']<1.25:continue
        # score rewards worst-period hit rate, expectancy, and retained opportunity count
        score=4*min(am['win'],bm['win'])+1.5*min(am['avgR'],bm['avgR'])+.25*min(am['pf'],bm['pf'])+.001*min(am['n']+bm['n'],220)
        valid.append((score,p,am,bm,m21))
    valid.sort(key=lambda x:x[0],reverse=True)
    print('VALID',len(valid),flush=True)
    if not valid:
        json.dump({'status':'REJECT_NO_GATE'},open('regime_gate_results/summary.json','w'),indent=2);return

    score,p,am,bm,m21=valid[0]
    # Freeze here. Everything below is test-only.
    g25=apply(t25,p)

    raw26=hc.load(early26_path); d26=hc.prep(raw26); f26=daily_features(raw26,d26); p26=attach(portfolio(d26,2026,2026),f26); gp26=apply(p26,p)
    recent_path=download_recent(); rr=hc.load(recent_path); dr=hc.prep(rr); fr=daily_features(rr,dr); pr=attach(portfolio(dr,2026,2026),fr); gpr=apply(pr,p)

    years={}
    for y in range(2019,2026):
        z=allp[pd.to_datetime(allp.date).dt.year==y]; years[str(y)]={'base':met(z),'gated':met(apply(z,p))}
    result={
      'status':'FROZEN_AND_TESTED','score':score,'gate':p,
      'train_2019_22':{'base':met(tr),'gated':am},
      'validation_2023_24':{'base':met(va),'gated':bm},
      'test_2025':{'base':met(t25),'gated':met(g25)},
      'early_2026':{'base':met(p26),'gated':met(gp26)},
      'recent_2026_60d':{'base':met(pr),'gated':met(gpr)},
      'recent_window':{'first':str(dr[0][0]) if dr else None,'last':str(dr[-1][0]) if dr else None},
      'years':years,
      'combined_2019_25_gated':pack(apply(allp,p)),
    }
    json.dump(result,open('regime_gate_results/summary.json','w'),indent=2)
    apply(allp,p).to_csv('regime_gate_results/gated_2019_25.csv',index=False)
    gp26.to_csv('regime_gate_results/gated_early_2026.csv',index=False);gpr.to_csv('regime_gate_results/gated_recent_2026.csv',index=False)
    print('REGIME_RESULT',json.dumps(result),flush=True)

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
