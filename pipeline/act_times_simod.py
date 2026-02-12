# Pipeline for approximating the start and end activity times from the raw data
# and running simod on it to get the first simulation model + agent parameters for all simulations

from pre_processing.import_data import import_2012
from pre_processing.approx_start_end_times import approx_start_end_times

def run_pipeline():
    data = import_2012()
    
    data = data.pipe(
        approx_start_end_times
    )

    print(data.head)

if __name__ == "__main__":
    run_pipeline()