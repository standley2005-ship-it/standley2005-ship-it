import sys, json
import pandas as pd
import high_confidence_search as hc
import ensemble_eval as ee

raw=hc.load(sys.argv[1]).copy()
raw=raw.set_index('ts').sort_index()
agg=raw.resample('5min',origin='start_day',label='left',closed='left').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna(subset=['open','high','low','close']).reset_index()
# hc.prep expects the tuple-form prepared data; recreate date/minute after resampling.
agg['minute']=agg.ts.dt.hour*60+agg.ts.dt.minute
agg['date']=agg.ts.dt.date
# Keep 4am-4pm as prior scripts do.
agg=agg[(agg.minute>=240)&(agg.minute<=960)]
# Reuse prep logic by writing the normalized data in-memory style via helper below.
# prep accepts DataFrame with ts/open/high/low/close/volume/minute/date.
days=hc.prep(agg)
cut=pd.Timestamp('2026-03-20').date()
days=[x for x in days if x[0]>cut]
print('EXTENSION_DAYS',len(days), [str(x[0]) for x in days])
la=ee.ledger(days,ee.A,'A',2026,2026);lb=ee.ledger(days,ee.B,'B',2026,2026)
u=ee.combine(la,lb,'union');ov=ee.combine(la,lb,'overlap')
print('EXT_A',json.dumps(ee.metrics(la)))
print('EXT_B',json.dumps(ee.metrics(lb)))
print('EXT_UNION',json.dumps(ee.metrics(u)))
print('EXT_OVERLAP',json.dumps(ee.metrics(ov)))
if len(u): print('EXT_TRADES',json.dumps(u[['date','R','dir','model','entry_ts','exit_ts']].astype(str).to_dict('records')))
