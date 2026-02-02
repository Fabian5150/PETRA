import pm4py as pm

def import_2012():
    log = pm.read_xes("/home/fabian/gitProjects/uni/ba/petra/data/BPI-Challenge-2012_1_all/BPI_Challenge_2012.xes")

    # translation of dutch activity names
    activity_names = list(log["concept:name"].unique())
    translated_names = ["A_SUBMITTED", "A_PARTLYSUBMITTED", "A_PREACCEPTED", "W_Complete_application", "A_ACCEPTED", "O_SELECTED", "A_FINALIZED", "O_CREATED", "O_SENT", "W_Follow_up_quotations", "O_SENT_BACK", "W_Validate_application", "A_REGISTERED", "A_APPROVED", "O_ACCEPTED", "A_ACTIVATED", "O_CANCELLED", "W_Change_contract_details", "A_DECLINED", "A_CANCELLED", "W_Process_leads", "O_DECLINED", "W_Follow_up_incomplete_files", "W_Assess_fraud"]

    translations = dict(zip(activity_names, translated_names))

    log["concept:name"] = log["concept:name"].map(lambda name : translations[name])

    log.drop(["case:AMOUNT_REQ", "case:REG_DATE"], axis=1)

    return log