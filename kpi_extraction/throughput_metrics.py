import pandas as pd

"""
Returns daily throuput, mean & max wip and little's law wip estiamte for the amount of cases
"""
def get_throuput(cycle_times):
    # throuput
    total_cases = len(cycle_times)
    total_duration_days = (cycle_times['end'].max() - cycle_times['start'].min()).days
    throughput_per_day = total_cases / total_duration_days

    # wip
    timeline = pd.date_range(
        start=cycle_times['start'].min(),
        end=cycle_times['end'].max(),
        freq='D'
    )

    wip_values = []
    for t in timeline:
        active_cases = ((cycle_times['start'] <= t) & (cycle_times['end'] >= t)).sum()
        wip_values.append(active_cases)

    avg_wip = sum(wip_values) / len(wip_values)
    max_wip = max(wip_values)

    # little's law
    cycle_times_sec = (cycle_times['end'] - cycle_times['start']).dt.total_seconds()
    avg_cycle_time_days = cycle_times_sec.mean() / (3600 * 24)

    wip_estimate_little = throughput_per_day * avg_cycle_time_days

    return {
        "throughput-daily": float(round(throughput_per_day, 3)),
        "wip-mean": float(round(avg_wip, 3)),
        "wip-max": float(round(max_wip, 3)),
        "littles-law-est": float(round(wip_estimate_little, 3))
    }