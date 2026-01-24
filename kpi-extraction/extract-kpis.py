import pm4py as pm
import numpy as np
from pm4py.statistics.traces.generic.pandas import case_statistics

"""
Returns the median, standard deviation and 95th percentile
of the case's cycle times
"""
def get_cycle_time(cycle_times):
    median = cycle_times["duration"].median()
    std = cycle_times["duration"].std()
    p95 = cycle_times["duration"].quantile(0.95)

    return {
        "median": median,
        "std": std,
        "p95": p95
    }

"""
Returns a cycle time stability index (0-1)
"""
def get_ct_stability(cycle_times):
    cycle_times["duration_sec"] = cycle_times["duration"].dt.total_seconds()

    ct_mean_sec = cycle_times["duration_sec"].mean()
    ct_std_sec = cycle_times["duration_sec"].std()

    # variation coefficient
    ct_stability = ct_std_sec / ct_mean_sec 

    # normalized stability score
    ct_stability_index = 1 / (1 + ct_stability)

    return ct_stability_index

"""
Returns a activity time stability index (mean)
Needs df with start and endtimestamp per activity
"""
def get_activity_time_stability(data):
    activity_durations_vc = (
        data.assign(duration=lambda df: df['end_timestamp'] - df['start_timestamp'])
        .groupby('concept:name')['duration']
        .apply(lambda x: x.dt.total_seconds().std() / x.dt.total_seconds().mean())
    )

    activity_durations_vc = 1 / (1 + activity_durations_vc)

    return activity_durations_vc.mean()

"""
Returns the amount of distinc variants and ap path stability index (shannon entropy)
"""
def get_path_stability(data):
    variants_count = case_statistics.get_variant_statistics(data)

    total_cases = data['case:concept:name'].nunique()

    # shannon entropy
    entropy_variants = -sum(
        (v["case:concept:name"]/total_cases) * np.log(v["case:concept:name"] / total_cases)
        for v in variants_count if v["case:concept:name"] > 0
    )

    entropy_normed = entropy_variants / np.log(len(variants_count))
    path_stability_index = 1 - entropy_normed

    return {
        "variant_amount": len(variants_count),
        "index": path_stability_index
    }

# --- aux functions ---
"""
TODO: ggf. Refactor to just use time:timestamp instead of start and end times
"""
def get_grouped_cycle_time_df(data):
    cycle_times = data.groupby("case:concept:name").agg(
        start=("start_timestamp", "min"),
        end=("end_timestamp", "max")
    )

    cycle_times["duration"] = cycle_times["end"] - cycle_times["start"]

    return cycle_times