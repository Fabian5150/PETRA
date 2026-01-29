import pm4py as pm

def import_2012():
    log = pm.read_xes("/home/fabian/gitProjects/uni/ba/petra/data/BPI-Challenge-2012_1_all/BPI_Challenge_2012.xes")

    log.drop(["case:AMOUNT_REQ", "case:REG_DATE"], axis=1)

    return log