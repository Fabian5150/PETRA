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
