import json, os
import pandas as pd
import numpy as np
import high_confidence_search as hc
import ensemble_eval as oe
import cross_symbol_recent as csr
import regime_gate_search as rg

GATE={'rv_min':0.14,'rv_max':0.4,'ret5_max':0.035,'trend20_min':0.003,'trend20_max':1.0,'trend50_max':0.1,'gap_max':1.0,'pmrange_min':0,'pmrange_max':999.0,'pmret_max':0.02}
SYMBOLS=csr.SYMBOLS


def run_symbol(s,outdir):
    path,raw0=csr.download_symbol(s,outdir)
    raw=hc.load(path); days=hc.prep(raw)
    y0=min(d[0].year for d in days); y1=max(d[0].year for d in days)
    la=oe.ledger(days,oe.A,'OCE_A',y0,y1);lb=oe.ledger(days,oe.B,'OCE_B',y0,y1)
    oce=oe.combine(la,lb,'union');gap=csr.gap_ledger(days);port=csr.portfolio(oce,gap)
    fmap=rg.daily_features(raw,days);attached=rg.attach(port,fmap);gated=rg.apply(attached,GATE)
    return {'symbol':s,'base':csr.met(attached),'gated':csr.met(gated),'base_n':len(attached),'gated_n':len(gated),'first_day':str(days[0][0]),'last_day':str(days[-1][0])},attached,gated


def pooled_metrics(frames):
    if not frames:return {'n':0}
    x=pd.concat(frames,ignore_index=True).sort_values(['date','symbol'])
    return csr.met(x),x


def main():
    out='regime_gate_seven_results';os.makedirs(out,exist_ok=True)
    reps={};bases=[];gates=[]
    for s in SYMBOLS:
        try:
            r,b,g=run_symbol(s,out);reps[s]=r
            if len(b):b=b.copy();b['symbol']=s;bases.append(b)
            if len(g):g=g.copy();g['symbol']=s;gates.append(g)
            print('SYMBOL_GATE',json.dumps(r),flush=True)
        except Exception as e:
            reps[s]={'symbol':s,'error':repr(e)};print('ERROR',s,repr(e),flush=True)
    bm,bx=pooled_metrics(bases);gm,gx=pooled_metrics(gates)
    # also report unique trade days and multi-symbol opportunity count
    meta={}
    for k,x in [('base',bx),('gated',gx)]:
        if len(x):
            by=x.groupby('date').size();meta[k]={'unique_trade_days':int(len(by)),'days_multi':int((by>1).sum()),'max_same_day':int(by.max())}
        else:meta[k]={'unique_trade_days':0,'days_multi':0,'max_same_day':0}
    result={'gate':GATE,'symbols':reps,'pooled_base':bm,'pooled_gated':gm,'pool_meta':meta}
    json.dump(result,open(out+'/summary.json','w'),indent=2)
    if len(bx):bx.to_csv(out+'/pooled_base.csv',index=False)
    if len(gx):gx.to_csv(out+'/pooled_gated.csv',index=False)
    print('SEVEN_GATE_FINAL',json.dumps(result),flush=True)

if __name__=='__main__':main()
