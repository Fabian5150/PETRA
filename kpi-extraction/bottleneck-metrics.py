import pm4py as pm
import pandas as pd

"""
TODO: Map this to a bpmn model, so the measures can be display in bpmn-js
"""
def get_performance_dfg(data):
    performance_dfg, _, _ = pm.discover_performance_dfg(data)

    return performance_dfg

# TODO: Extract better metrics for this and format them in a way an api can send to the frontend
def get_bottlnecks(performance_dfg):
    perf_df = pd.DataFrame([
        {
            "from": k[0],
            "to": k[1],
            **v  # extracts mean, median, max, min, sum, stdev
        }
        for k, v in performance_dfg.items()
    ])

    top3_bottlenecks = perf_df.sort_values("mean", ascending=False).head(3)

    print(top3_bottlenecks[["from", "to", "mean", "median", "max", "stdev"]])

    summary_stats = {
        "median_mean": perf_df["mean"].median(),
        "std_mean": perf_df["mean"].std(),
        "max": perf_df["max"].max()
    }

    print("\nbottlneck times:")
    for k, v in summary_stats.items():
        print(f"{k}: {round(v / 3600, 3)} h")