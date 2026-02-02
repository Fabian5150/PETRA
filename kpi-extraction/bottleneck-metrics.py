import pm4py as pm
import pandas as pd

"""
TODO: Map this to a bpmn model, so the measures can be display in bpmn-js
"""
def get_performance_dfg(data):
    performance_dfg, _, _ = pm.discover_performance_dfg(data)

    return performance_dfg

# TODO: Extract more and better metrics from the performance dfg
def get_bottlnecks(performance_dfg):
    perf_df = pd.DataFrame([
        {
            "from": k[0],
            "to": k[1],
            **v
        }
        for k, v in performance_dfg.items()
    ])

    top3_bottlenecks = perf_df.sort_values("mean", ascending=False).head(3)
    top3_bottlenecks["mean"] = round(top3_bottlenecks["mean"] / 3600 , 2).astype(str) + " h"

    return top3_bottlenecks[["from", "to","mean"]].reset_index().T.drop("index").to_dict()