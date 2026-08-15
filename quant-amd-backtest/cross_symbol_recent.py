import json, os, sys
import pandas as pd
import numpy as np
import yfinance as yf
import high_confidence_search as hc
import ensemble_eval as oe

SYMBOLS=['QQQ','SPY','IWM','NVDA','AMD','AAPL','META']
GAP={"slip_bps":1.0,"max_stop_pct":0.012,"direction":"both","trend_filter":True,"target_R":0.6,"stop_atr":0,"touch_atr":0.3,"entry_cutoff":660,"ema_confirm":True,"gap_min":0.005,"gap_max":0.02,"confirm_min":45,"open_confirm":0.003}


def met(df):
    if df is None or len(df)==0:
        return {'n':0,'win':None,'avgR':None,'pf':None,'totalR':0.0,'maxddR':None}
    r=df.R.to_numpy(float)
    pos=r[r>0].sum(); neg=-r[r<0].sum(); eq=np.cumsum(r); dd=eq-np.maximum.accumulate(eq)
    return {'n':int(len(r)),'win':float((r>0).mean()),'avgR':float(r.mean()),'pf':float(pos/neg if neg>0 else 999),'totalR':float(r.sum()),'maxddR':float(dd.min())}


def download_symbol(symbol, outdir):
    h=yf.Ticker(symbol).history(period='60d',interval='5m',prepost=True,auto_adjust=False,actions=False)
    if h is None or len(h)==0:
        raise RuntimeError(f'No yfinance data for {symbol}')
    idx=pd.DatetimeIndex(h.index)
    if idx.tz is not None:
        idx=idx.tz_convert('America/New_York').tz_localize(None)
    d=pd.DataFrame({
        'timestamp':idx,
        'open':pd.to_numeric(h['Open'],errors='coerce').to_numpy(),
        'high':pd.to_numeric(h['High'],errors='coerce').to_numpy(),
        'low':pd.to_numeric(h['Low'],errors='coerce').to_numpy(),
        'close':pd.to_numeric(h['Close'],errors='coerce').to_numpy(),
        'volume':pd.to_numeric(h['Volume'],errors='coerce').fillna(0).to_numpy(),
    }).dropna(subset=['open','high','low','close'])
    path=os.path.join(outdir,f'{symbol}_60d_5m.csv')
    d.to_csv(path,index=False)
    return path, d


def gap_ledger(days):
    rows=[]
    for day in days:
        z=hc.strat_gap_pullback(day,GAP)
        if z:
            z=dict(z); z['model']='GAP'; rows.append(z)
    return pd.DataFrame(rows)


def portfolio(oce,gap):
    if len(oce)==0 and len(gap)==0:return pd.DataFrame()
    a={str(r.date):r for r in oce.itertuples(index=False)} if len(oce) else {}
    b={str(r.date):r for r in gap.itertuples(index=False)} if len(gap) else {}
    rows=[]
    for d in sorted(set(a)|set(b)):
        x=a.get(d); y=b.get(d)
        if x is not None and y is not None:
            if int(x.dir)!=int(y.dir):continue
            chosen=x if str(x.entry_ts)<=str(y.entry_ts) else y
            rec=chosen._asdict(); rec['sources']='OCE+GAP'; rec['agreement_count']=2; rows.append(rec)
        else:
            chosen=x if x is not None else y
            rec=chosen._asdict(); rec['sources']='OCE' if x is not None else 'GAP'; rec['agreement_count']=1; rows.append(rec)
    return pd.DataFrame(rows)


def main():
    outdir='cross_symbol_results'; os.makedirs(outdir,exist_ok=True)
    reports={}; pooled=[]
    for s in SYMBOLS:
        try:
            path,raw=download_symbol(s,outdir)
            days=hc.prep(hc.load(path))
            if not days:
                raise RuntimeError('No complete RTH days after normalization')
            y0=min(d[0].year for d in days); y1=max(d[0].year for d in days)
            la=oe.ledger(days,oe.A,'OCE_A',y0,y1); lb=oe.ledger(days,oe.B,'OCE_B',y0,y1)
            oce=oe.combine(la,lb,'union'); gap=gap_ledger(days); port=portfolio(oce,gap)
            if len(port):
                port=port.copy(); port['symbol']=s; pooled.append(port)
                port.to_csv(os.path.join(outdir,f'{s}_portfolio.csv'),index=False)
            rec={
                'symbol':s,'bars':int(len(raw)),'complete_days':int(len(days)),
                'first_day':str(days[0][0]),'last_day':str(days[-1][0]),
                'OCE':met(oce),'GAP':met(gap),'PORT':met(port),
                'gap_only':int(sum(1 for x in port.sources if x=='GAP')) if len(port) else 0,
                'oce_only':int(sum(1 for x in port.sources if x=='OCE')) if len(port) else 0,
                'agreement':int(sum(1 for x in port.sources if x=='OCE+GAP')) if len(port) else 0,
            }
            reports[s]=rec; print('SYMBOL',json.dumps(rec),flush=True)
        except Exception as e:
            reports[s]={'symbol':s,'error':repr(e)}; print('SYMBOL_ERROR',s,repr(e),flush=True)
    allp=pd.concat(pooled,ignore_index=True) if pooled else pd.DataFrame()
    if len(allp):
        allp.to_csv(os.path.join(outdir,'all_opportunities.csv'),index=False)
        bydate=allp.groupby('date').size()
        pooled_meta={
            'opportunities':int(len(allp)),
            'win':float((allp.R>0).mean()),
            'avgR':float(allp.R.mean()),
            'pf':float(allp.loc[allp.R>0,'R'].sum()/(-allp.loc[allp.R<0,'R'].sum())) if (allp.R<0).any() else 999,
            'unique_trade_days':int(bydate.size),
            'days_with_multiple_symbols':int((bydate>1).sum()),
            'max_signals_same_day':int(bydate.max()),
        }
    else: pooled_meta={'opportunities':0}
    result={'window_note':'yfinance rolling 60d 5m pre/post, frozen rules, no per-symbol tuning','symbols':reports,'pooled_raw_opportunities':pooled_meta}
    json.dump(result,open(os.path.join(outdir,'summary.json'),'w'),indent=2)
    print('FINAL',json.dumps(result),flush=True)

if __name__=='__main__':main()
