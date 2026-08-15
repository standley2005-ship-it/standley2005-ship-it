import sys,json,os
import high_confidence_search as hc
import portfolio_strategy_search as ps
fam=sys.argv[1];train_path=sys.argv[2];test_path=sys.argv[3]
train=hc.prep(hc.load(train_path));test=hc.prep(hc.load(test_path))
valid=ps.select_family(train,fam,n=1200)
out={'family':fam,'valid_count':len(valid),'status':'REJECT_NO_PRE2026_CANDIDATE'}
if valid:
    score,p,tm,vm,a,b,yrs=valid[0]
    h=ps.bt(test,fam,p,2026,2026);hm=ps.metrics(h)
    out={'family':fam,'valid_count':len(valid),'status':'FROZEN_AND_TESTED','score':score,'params':p,'train_2019_22':tm,'validation_2023_25':vm,'years_2023_25':yrs,'holdout_2026':hm,'sim200_2pct':ps.sim(h,.02)}
    os.makedirs('fast_results',exist_ok=True)
    import pandas as pd
    pd.DataFrame(h).to_csv(f'fast_results/{fam}_2026.csv',index=False)
os.makedirs('fast_results',exist_ok=True)
json.dump(out,open(f'fast_results/{fam}.json','w'),indent=2)
print('FAMILY_RESULT',json.dumps(out),flush=True)
