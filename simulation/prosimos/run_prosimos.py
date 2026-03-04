import subprocess
from pathlib import Path


def run_prosimos(bpmn_path: str, json_path: str, output_csv: str, num_cases: int = 200):
    bpmn_path = Path(bpmn_path).resolve()
    json_path = Path(json_path).resolve()
    output_csv = Path(output_csv).resolve()
    
    subprocess.run([
        "prosimos", "start-simulation",
        "--bpmn_path", str(bpmn_path),
        "--json_path", str(json_path),
        "--total_cases", str(num_cases),
        "--stat_out_path", str(output_csv)
    ], check=True)


if __name__ == "__main__":
    script_dir = Path(__file__).parent.parent.parent
    
    run_prosimos(
        bpmn_path=script_dir / "state/simod_out/best_result/bpi_2012_approx_activity_times.bpmn",
        json_path=script_dir / "state/simod_out/best_result/bpi_2012_approx_activity_times.json",
        output_csv=script_dir / "state/prosimos_out/simulated_log.csv",
        num_cases=200
    )