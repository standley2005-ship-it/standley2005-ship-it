import sys,json,glob,os
import pandas as pd
import high_confidence_search as hc
import portfolio_strategy_search as ps
import ensemble_eval as oe
train_path=sys.argv[1];test_path=sys.argv[2]
train=hc.prep(hc.load(train_path));test=hc.prep(hc.load(test_path))
selected={}; family_report={}
for fp in glob.glob('fast_inputs/*.json'):
    x=json.load(open(fp));family_report[x['family']]=x
    if x.get('status')=='FROZEN_AND_TESTED':selected[x['family']]=x['params']

def oce(days,y0,y1):
    return oe.combine(oe.ledger(days,oe.A,'OCE_A',y0,y1),oe.ledger(days,oe.B,'OCE_B',y0,y1),'union')

def fr(rows,name):
    return ps.df_rows(rows,name)

def build(days,y0,y1):
    frames={'OCE':oce(days,y0,y1)}
    for fam,p in selected.items():frames[fam]=fr(ps.bt(days,fam,p,y0,y1),fam)
    return ps.combine_portfolio(frames)
ph=build(train,2019,2025);p26=build(test,2026,2026)
yrs=[]
for y in range(2019,2026):
    py=build(train,y,y);yrs.append({'year':y,**ps.metrics(py)})
res={'families':family_report,'selected_families':list(selected),'OCE_2019_25':ps.metrics(oce(train,2019,2025)),'PORTFOLIO_2019_25':ps.metrics(ph),'portfolio_200_2pct':ps.sim(ph,.02),'OCE_2026':ps.metrics(oce(test,2026,2026)),'PORTFOLIO_2026':ps.metrics(p26),'portfolio_2026_200_2pct':ps.sim(p26,.02),'yearly':yrs}
os.makedirs('aggregate_results',exist_ok=True)
json.dump(res,open('aggregate_results/summary.json','w'),indent=2)
if len(ph):ph.to_csv('aggregate_results/portfolio_2019_25.csv',index=False)
if len(p26):p26.to_csv('aggregate_results/portfolio_2026.csv',index=False)
print('AGGREGATE_RESULT',json.dumps(res),flush=True)
