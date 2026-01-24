import pm4py as pm
import pandas as pd

"""
Uses the heuristic net and a min time difference of 48h 
to determine (probably) plannend and unplanned loops
to distinguish between planned repetition and actual rework
TODO: Refactor with pm4py's build in filter_activities_rework ( https://processintelligence.solutions/static/api/2.7.17/pm4py.html#pm4py.filtering.filter_activities_rework )
"""
def get_reworkrate(data):
    heu_net = pm.discover_heuristics_net(log = data)
    dep_matrix = heu_net.dependency_matrix

    self_loops = []

    for act_a, inner_dict in dep_matrix.items():
        for act_b, dep_val in inner_dict.items():
            if act_a == act_b:
                self_loops.append((act_a, dep_val))

    allowed_loops = [act for act, dep in self_loops if dep >= 0.8]

    data["time:timestamp"] = pd.to_datetime(data["time:timestamp"])
    data.sort_values(["case:concept:name", "time:timestamp"], inplace=True)

    reworks = []

    for case_id, group in data.groupby("case:concept:name"):
        acts = group["concept:name"].tolist()
        starts = group["start_timestamp"].tolist()
        ends = group["end_timestamp"].tolist()

        for i, act in enumerate(acts):
            later_indices = [j for j, x in enumerate(acts[i+1:], start=i+1) if x == act]

            for j in later_indices:
                time_diff_hours = (ends[j] - starts[i]).total_seconds() / 60
                rework_time = ends[j] - starts[j]

                if act not in allowed_loops and time_diff_hours < 48:
                    reworks.append((case_id, act, rework_time, time_diff_hours))

    df_reworks = pd.DataFrame(reworks, columns=["case","activity","rework_time", "rework_time_diff"])

    total_cases = data["case:concept:name"].nunique()
    affected_cases = df_reworks["case"].nunique()

    rework_rate_pct = affected_cases / total_cases * 100
    avg_reworks_per_case = df_reworks.groupby("case")["activity"].count().mean()

    median_rework_time = df_reworks["rework_time"].median().total_seconds() / 60
    median_rework_time_diff = df_reworks["rework_time_diff"].median()

    return {
        "rework-cases-total": affected_cases,
        "rework-cases-percentage": round(rework_rate_pct, 2),
        "rework-amount-mean": round(avg_reworks_per_case, 2),
        "rework-time-med-min": round(median_rework_time, 0), # sum of activity times of reworks
        "rework-time-diff-med-min": round(median_rework_time_diff, 0) # time delta between first and second occurence of rework activity
    }