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

    return log