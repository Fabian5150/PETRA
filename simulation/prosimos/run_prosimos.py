import subprocess
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent.parent.parent
bpmn_path=script_dir / "state/process-model.bpmn"
json_path=script_dir / "state/sim_params.json"
""" bpmn_path=script_dir / "state/simod_out/best_result/bpi_2012_approx_activity_times.bpmn"
json_path=script_dir / "state/simod_out/best_result/bpi_2012_approx_activity_times.json" """
output_csv=script_dir / "data/temp/prosimos_log.csv"

def run_prosimos(num_cases: int = 10):
    subprocess.run([
        "prosimos", "start-simulation",
        "--bpmn_path", str(Path(bpmn_path).resolve()),
        "--json_path", str(Path(json_path).resolve()),
        "--total_cases", str(num_cases),
        "--log_out_path", str(Path(output_csv).resolve())
    ], check=True)

"""
Reads in the prosimos csv, renames the columns to match the kpi scripts
and returns it as df
"""
def convert_prosimos_csv():
    log = pd.read_csv(output_csv, parse_dates=["start_time", "end_time", "enable_time"])
    
    log["case_id"] = log["case_id"].astype(str)

    log = log.rename(columns={
        "case_id": "case:concept:name",
        "activity": "concept:name",
        "start_time": "start_timestamp",
        "end_time": "end_timestamp",
        "enable_time": "enable_timestamp"
    })

    log["time:timestamp"] = log["end_timestamp"] # for pm4py

    return log

def run_sim():
    print("--- Starting Prosimos Sim ---")
    run_prosimos()

    print("--- Convert Prosimos csv to df ---")
    return convert_prosimos_csv()