# Pipeline for approximating the start and end activity times from the raw data
# and running simod on it to get the first simulation model + agent parameters for all simulations

from pathlib import Path
from pre_processing.import_data import import_2012
from pre_processing.approx_start_end_times import approx_start_end_times

def run_pipeline():
    data = import_2012()
    
    data = data.pipe(
        approx_start_end_times
    )
    
    print("--- Writing dataframe with approximated activity times to csv ---")
    data.to_csv(Path(__file__).parent / ".." / "data" / "bpi_2012" / "bpi_2012_approx_activity_times.csv", index=False)
    

if __name__ == "__main__":
    run_pipeline()