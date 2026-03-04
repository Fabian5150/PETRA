# pipeline for running a prosimos simulation and extracting kpis from its output

from simulation.prosimos.run_prosimos import run_sim
from pipeline.extract_kpis import run_pipeline as extract_kpis

from app.services.state_service import load_kpis

def run_pipeline():
    sim_log = run_sim()

    print("--- Extracting Kpis ---")
    extract_kpis(sim_log)

if __name__ == "__main__":
    run_pipeline()