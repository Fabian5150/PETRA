import pm4py as pm

def import_2012():
    log = pm.read_xes("/home/fabian/gitProjects/uni/ba/petra/data/BPI-Challenge-2012_1_all/BPI_Challenge_2012.xes")

    log.drop(["case:AMOUNT_REQ", "case:REG_DATE"], axis=1)

    log = log.rename(columns={
        "case:concept:name" : "case_id",
        "concept:name" : "activity_key",
        "time:timestamp" : "timestamp",
        "org:resource" : "resource",
        "lifecycle:transition" : "transition",
        "case:REG_DATE" : "case_start"
    })

    return log