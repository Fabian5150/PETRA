# pipeline for extracting all kpis and storing them in one dict

from kpi_extraction.helpers import *
from kpi_extraction.bottleneck_metrics import *
from kpi_extraction.cycle_time_metrics import *
from kpi_extraction.rework_metrics import *
from kpi_extraction.stabililty_metrics import *
from kpi_extraction.throughput_metrics import *

from pre_processing.import_data import import_2012

from app.services.state_service import store_kpis

def run_pipeline():
    data = import_2012()

    cycle_times = get_grouped_cycle_time_df(data, False)

    cycle_time_metrics = get_cycle_time(cycle_times)
    throughput_metrics = get_throuput(cycle_times)
    # rework_metrics = get_reworkrate(data) # need event log with start and end times

    performance_dfg = get_performance_dfg(data)
    bottleneck_metrics = get_bottlnecks(performance_dfg)

    ct_stability = get_ct_stability(cycle_times)
    # at_stability = get_activity_time_stability(data) # need event log with start and end times
    path_stability = get_path_stability(data)

    kpi_dict = {
        "Cycle Time": cycle_time_metrics,
        "Throughput": throughput_metrics,
        "Reworks": "tbd", # rework_metrics
        "Bottlenecks": bottleneck_metrics,
        "Stability": {
            "Cycle Time Stability": ct_stability,
            "Activity Time Stability": "tbd", # at_stability
            "Path Stability": path_stability
        }    
    }

    print("\n\n", kpi_dict, "\n\n")

    store_kpis(kpi_dict)

if __name__ == "__main__":
    run_pipeline()