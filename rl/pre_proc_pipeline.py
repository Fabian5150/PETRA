import pandas as pd

"""
Identifies the worst bottleneck to be used as "absorption state"
"""
def identify_absorption_state(log):
    log["duration"] = (pd.to_datetime(log["end_timestamp"]) - pd.to_datetime(log["start_timestamp"])).dt.total_seconds()
    
    avg_duration = log.groupby("concept:name")["duration"].mean()
    bottleneck = avg_duration.idxmax()
    
    return bottleneck

"""
Given an absorpion state, removes all activities following it in a case
"""
def apply_absorption_effect(log, bottleneck: str):
    
    result = []
    
    for _, case_log in log.groupby("case:concept:name"):
        case_log = case_log.sort_values("time:timestamp").reset_index(drop=True)
        
        bottleneck_indices = case_log[case_log["concept:name"] == bottleneck].index
        
        if len(bottleneck_indices) > 0:
            cutoff = bottleneck_indices[0] + 1
            result.append(case_log.iloc[:cutoff])
        else:
            result.append(case_log)
    
    return pd.concat(result, ignore_index=True)