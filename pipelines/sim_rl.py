# Pipeline for simulating a bpmn process and running the RL bottleneck enhancer on its' output

from simulation.prosimos.run_prosimos import run_sim
from rl.pre_proc_pipeline import run_pipeline as rl_preproc 

def run_pipeline():
    sim_log = run_sim()

    print("--- Preprocessing Log for RL Agents ---")
    rl_pre_log = rl_preproc(sim_log)

    
if __name__ == "__main__":
    run_pipeline()