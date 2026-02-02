# pipeline for cleaning, augmenting and mining a raw data set
# and extracting the kpis
# stores the obtained bpmn model and kpis in their gloabl state files

from pre_processing.clean import clean
from pre_processing.import_data import import_2012
from pre_processing.approx_start_end_times import *

from mining.mine_bpmn import get_bpmn_heuristic, get_bpmn_inductive

from app.services.state_service import store_bpmn

def run_pipeline():
    data = import_2012()
    
    data = data.pipe(
        clean
    ).pipe(
        get_bpmn_heuristic
    )
    
    store_bpmn(data)
    

if __name__ == "__main__":
    run_pipeline()