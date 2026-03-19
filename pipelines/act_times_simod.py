# Pipeline for approximating the start and end activity times from the raw data
# and running simod on it to get the first simulation model + agent parameters for all simulations

from pathlib import Path
from pre_processing.import_data import import_2012
from pre_processing.approx_start_end_times import approx_start_end_times
from simulation.simod.run_simod import run_my_simod
from simulation.simod.simod_to_state import simod_to_state

input_log_path = Path(__file__).parent.parent / "data" / "bpi_2012" / "bpi_2012_approx_activity_times.csv"
simod_config_path = Path(__file__).parent.parent / "simulation" / "simod" / "ahh.yaml"
simod_output_path = Path(__file__).parent.parent / "state" / "simod_out"

def run_pipeline():
    data = import_2012()
    
    data = data.pipe(
        approx_start_end_times
    )
    
    print("--- Writing dataframe with approximated activity times to csv ---")
    data.to_csv(input_log_path, index=False)

    print("--- Starting Simod ---")

    run_my_simod(
        log_path=input_log_path,
        config_path=simod_config_path,
        output_dir=simod_output_path
    )

    simod_to_state()

if __name__ == "__main__":
    run_pipeline()