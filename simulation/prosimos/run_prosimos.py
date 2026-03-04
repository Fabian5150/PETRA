import subprocess
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent.parent.parent
bpmn_path=script_dir / "state/simod_out/best_result/bpi_2012_approx_activity_times.bpmn"
json_path=script_dir / "state/simod_out/best_result/bpi_2012_approx_activity_times.json"
output_csv=script_dir / "data/temp/prosimos_log.csv",

def run_prosimos(num_cases: int = 1000):
    bpmn_path = Path(bpmn_path).resolve()
    json_path = Path(json_path).resolve()
    output_csv = Path(output_csv).resolve()
    
    subprocess.run([
        "prosimos", "start-simulation",
        "--bpmn_path", str(bpmn_path),
        "--json_path", str(json_path),
        "--total_cases", str(num_cases),
        "--log_out_path", str(output_csv)
    ], check=True)

"""
Reads in the prosimos csv, renames the columns to match the kpi scripts
and returns it as df
"""
def convert_prosimos_csv():
    log = pd.read_csv(output_csv)
    
    log = log.rename(columns={
        "activity": "activity_key",
        "start_time": "start_date",
        "end_time": "end_date",
        "enabled_time": "enable_date"
    })
    
    print(log.columns)

    return log