import sys,json,os,pandas as pd
import high_confidence_search as hc
import second_wave_core as sw
fam=sys.argv[1];train=hc.prep(hc.load(sys.argv[2]));test=hc.prep(hc.load(sys.argv[3]))
valid=sw.select(train,fam,1200);out={'family':fam,'valid_count':len(valid),'status':'REJECT_NO_PRE2026_CANDIDATE'}
if valid:
 score,p,tm,vm,yrs=valid[0];h=sw.bt(test,fam,p,2026,2026);out={'family':fam,'valid_count':len(valid),'status':'FROZEN_AND_TESTED','score':score,'params':p,'train_2019_22':tm,'validation_2023_25':vm,'years_2023_25':yrs,'holdout_2026':sw.metrics(h),'sim200_2pct':sw.sim(h,.02)}
 os.makedirs('second_results',exist_ok=True);pd.DataFrame(h).to_csv(f'second_results/{fam}_2026.csv',index=False)
os.makedirs('second_results',exist_ok=True);json.dump(out,open(f'second_results/{fam}.json','w'),indent=2);print('SECOND_RESULT',json.dumps(out),flush=True)
