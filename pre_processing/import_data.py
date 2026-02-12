from pathlib import Path
import pandas as pd

def import_2012():
    log = pd.read_csv(Path(__file__).parent / ".." / "data" / "bpi_2012" / "bpi_2012_translated.csv")

    return log.drop(["case:AMOUNT_REQ", "case:REG_DATE"], axis=1)