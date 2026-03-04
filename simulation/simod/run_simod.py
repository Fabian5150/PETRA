from pathlib import Path
from simod.event_log.event_log import EventLog
from simod.settings.simod_settings import SimodSettings
from simod.simod import Simod

def run_my_simod(log_path: str, config_path: str, output_dir: str):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    settings = SimodSettings.from_path(Path(config_path))
    settings.common.train_log_path = Path(log_path)
    
    event_log = EventLog.from_path(
        log_ids=settings.common.log_ids,
        train_log_path=settings.common.train_log_path,
        test_log_path=settings.common.test_log_path,
        preprocessing_settings=settings.preprocessing,
        need_test_partition=settings.common.perform_final_evaluation,
    )
    
    simod = Simod(settings=settings, event_log=event_log, output_dir=output)
    simod.run()
    
    print(f"simod output in: {output}")