"""
Returns the median, standard deviation and 95th percentile
of the case's cycle times
"""
def get_cycle_time(cycle_times):
    median = str(round(cycle_times["duration"].median().total_seconds() / 3600, 1)) + " h"
    std = str(round(cycle_times["duration"].std().total_seconds() / 3600, 1)) + " h"
    p95 = str(round(cycle_times["duration"].quantile(0.95).total_seconds() / 3600, 1)) + " h"

    return {
        "median": median,
        "std": std,
        "p95": p95
    }
