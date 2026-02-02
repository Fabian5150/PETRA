"""
TODO: ggf. Refactor to just use time:timestamp instead of start and end times
"""
def get_grouped_cycle_time_df(data, isStartEndLog = True):
    if(isStartEndLog):
        cycle_times = data.groupby("case:concept:name").agg(
            start=("start_timestamp", "min"),
            end=("end_timestamp", "max")
        )
    else:
        cycle_times = data.groupby("case:concept:name").agg(
            start=("start_timestamp", "min"),
            end=("end_timestamp", "max")
        )


    cycle_times["duration"] = cycle_times["end"] - cycle_times["start"]

    return cycle_times