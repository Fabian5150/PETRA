from pathlib import Path
import pandas as pd

def import_2012():
    log = pd.read_csv(Path(__file__).parent / ".." / "data" / "bpi_2012" / "bpi_2012_translated.csv")

    log = log.drop(["case:AMOUNT_REQ", "case:REG_DATE"], axis=1)

    log = log.rename(columns={
        "case:concept:name" : "case_id",
        "concept:name" : "activity_key",
        "time:timestamp" : "timestamp",
        "org:resource" : "resource",
        "lifecycle:transition" : "transition"
    })

    log["resource"] = log["resource"].astype(str)
    log["case_id"] = log["case_id"].astype(str)

    return log

# utility function for importing the prosimos output log
def import_prosimos():
    log = pd.read_csv((Path(__file__).parent / ".." / "data" / "temp" / "prosimos_log.csv"), parse_dates=["start_time", "end_time", "enable_time"])

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