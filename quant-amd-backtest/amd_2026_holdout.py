import sys,json
import amd_premarket as a
P={'slip_bps':1.0,'max_stop_pct':0.015,'acc_pair':(450,540),'min_acc_atr':1.5,'max_acc_atr':5,'sweep_atr':0.1,'reclaim_bars':2,'confirm_bars':1,'disp_atr':0.8,'break_lookback':3,'entry_mode':'next','ema_wait':3,'target_R':1.5,'stop_atr':0.1,'sweep_cutoff':690,'entry_cutoff':720,'trend_filter':False,'direction':'both'}
df=a.load(sys.argv[1]);days=a.prep(df);r=a.bt(days,P,2026,2026);m=a.met(r);bal,dd=a.sim(r,.05)
print('FROZEN_HR1',json.dumps(P,sort_keys=True));print('HOLDOUT_2026',json.dumps(m));print('ACCOUNT_200_5PCT',json.dumps({'end':bal,'maxdd_pct':dd*100}));
for x in r: print('TRADE',json.dumps(x,default=str))
