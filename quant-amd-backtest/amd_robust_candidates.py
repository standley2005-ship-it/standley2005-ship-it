import sys, json, pandas as pd
import amd_premarket as a

CANDIDATES={
'HR1_stable': {'slip_bps':1.0,'max_stop_pct':0.015,'acc_pair':(450,540),'min_acc_atr':1.5,'max_acc_atr':5,'sweep_atr':0.1,'reclaim_bars':2,'confirm_bars':1,'disp_atr':0.8,'break_lookback':3,'entry_mode':'next','ema_wait':3,'target_R':1.5,'stop_atr':0.1,'sweep_cutoff':690,'entry_cutoff':720,'trend_filter':False,'direction':'both'},
'HR2_long_convex': {'slip_bps':1.0,'max_stop_pct':0.015,'acc_pair':(450,540),'min_acc_atr':2.0,'max_acc_atr':12,'sweep_atr':0.0,'reclaim_bars':1,'confirm_bars':3,'disp_atr':1.0,'break_lookback':2,'entry_mode':'next','ema_wait':1,'target_R':3.0,'stop_atr':0.2,'sweep_cutoff':630,'entry_cutoff':750,'trend_filter':False,'direction':'long'},
'HR3_smoother': {'slip_bps':1.0,'max_stop_pct':0.015,'acc_pair':(480,570),'min_acc_atr':2.0,'max_acc_atr':12,'sweep_atr':0.2,'reclaim_bars':0,'confirm_bars':3,'disp_atr':0.6,'break_lookback':2,'entry_mode':'ema','ema_wait':3,'target_R':1.5,'stop_atr':0.1,'sweep_cutoff':690,'entry_cutoff':720,'trend_filter':False,'direction':'long'},
}

def main(path):
 df=a.load(path); days=a.prep(df); out=[]
 for name,p in CANDIDATES.items():
  allr=a.bt(days,p,2019,2025); m=a.met(allr); bal,dd=a.sim(allr,.05)
  row={'candidate':name,**m,'end200_all':bal,'acctdd_all_pct':dd*100}; out.append(row)
  print('\nCANDIDATE',name,json.dumps(p,sort_keys=True));print('FULL',json.dumps(row))
  years=[]
  for y in range(2019,2026):
   r=a.bt(days,p,y,y); mm=a.met(r); b,d=a.sim(r,.05); years.append({'candidate':name,'year':y,**mm,'end200_if_reset':b,'acctdd_pct':d*100})
  print('YEARS',json.dumps(years)); pd.DataFrame(allr).to_csv(f'premarket_results/{name}_trades.csv',index=False);pd.DataFrame(years).to_csv(f'premarket_results/{name}_years.csv',index=False)
 pd.DataFrame(out).to_csv('premarket_results/robust_candidates_summary.csv',index=False)
if __name__=='__main__':main(sys.argv[1])
