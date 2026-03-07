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

"""
Builds the transformed event log edges of directly following activites as entries
"""
def create_source_target_pairs(log):
    result = []
    
    for case_id, case_df in log.groupby("case:concept:name"):
        case_df = case_df.sort_values("end_timestamp").reset_index(drop=True)
        
        for i in range(len(case_df)):
            source_activity = case_df.loc[i, "concept:name"]
            source_start = case_df.loc[i, "start_timestamp"]
            source_end = case_df.loc[i, "end_timestamp"]
            
            if i < len(case_df) - 1:
                target_activity = case_df.loc[i + 1, "concept:name"]
                target_start = case_df.loc[i + 1, "start_timestamp"]
                target_end = case_df.loc[i + 1, "end_timestamp"]
            else:
                target_activity = "end"
                target_start = source_end
                target_end = source_end
            
            result.append({
                "case:concept:name": case_id,
                "source_activity": source_activity,
                "source_start": source_start,
                "source_end": source_end,
                "target_activity": target_activity,
                "target_start": target_start,
                "target_end": target_end
            })
    
    return pd.DataFrame(result)

"""
Removes (now) short cases with few activities
"""
def filter_short_cases(log, min_length = 4):
    case_lengths = log.groupby("case:concept:name").size()
    valid_cases = case_lengths[case_lengths >= min_length].index
    
    filtered = log[log["case:concept:name"].isin(valid_cases)]
    
    # removed = len(log["case:concept:name"].unique()) - len(filtered["case:concept:name"].unique())
    
    return filtered

"""
Calculates the relative frequency of transition per each pair and adds it in each pair of the log
"""
def calculate_transition_probabilities(transitions: pd.DataFrame):
    transition_counts = transitions.groupby(["source_activity", "target_activity"]).size().reset_index(name="transition_count")
    
    source_totals = transitions.groupby("source_activity").size().reset_index(name="source_total")
    
    res = transition_counts.merge(source_totals, on="source_activity")
    res["transition_probability"] = res["transition_count"] / res["source_total"]
    
    transitions = transitions.merge(
        res[["source_activity", "target_activity", "transition_probability"]], 
        on=["source_activity", "target_activity"],
        how="left"
    )
    
    return transitions

def run_pipeline(log):
    abs_state = identify_absorption_state(log)

    return (log
        .pipe(apply_absorption_effect, abs_state)
        .pipe(create_source_target_pairs)
        .pipe(filter_short_cases)
        .pipe(calculate_transition_probabilities)
    )