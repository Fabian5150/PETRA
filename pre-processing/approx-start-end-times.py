import pandas as pd
import pm4py as pm
import numpy as np

# TODO: Generalize this script; make path, column and entity names variable
# TODO: Refactor everythin into distinct functions

log = pm.read_xes("/home/fabian/gitProjects/uni/ba/petra/data/BPI-Challenge-2012_1_all/BPI_Challenge_2012.xes")

# Drop / Rename columns
log.drop(["case:AMOUNT_REQ", "case:REG_DATE"], axis=1)

log = log.rename(columns={
    "case:concept:name" : "case_id",
    "concept:name" : "activity_key",
    "time:timestamp" : "timestamp",
    "org:resource" : "resource",
    "lifecycle:transition" : "transition",
    "case:REG_DATE" : "case_start"
})

# Get start and end entries
start_entries = log[log["transition"] == "START"].sort_values(by="timestamp")
end_entries = log[log["transition"] == "COMPLETE"].sort_values(by="timestamp")

# Get all activity types which are in end_entries, but not in start_entries or schedule_entries
start_activity_types = set(start_entries["activity_key"].unique())
end_activity_types = set(end_entries["activity_key"].unique())

unmatched_activity_types = list(end_activity_types - start_activity_types)

start_case_grouping = start_entries.groupby("case_id")
start_case_ids = list(start_case_grouping.groups.keys())

end_case_grouping = end_entries.groupby("case_id")

start_end_log = []
unmatched_entries = [] # unmatched start or end entries => approximate their corresponding start/end date

# merge start and end entries into one activity with start and end timestamps
def merge_start_end (start, end):
    # Maybe also keep ids for start and end event?
    # This way they could be linked to their correspondece in the other log for pm
    event = dict()
    event["activity_key"] = start.activity_key
    event["resource"] = start.resource
    event["case_id"] = start.case_id
    event["start_date"] = start.timestamp
    event["end_date"] = end.timestamp

    return event

# TODO: Refactor this with vectorized pandas operations for better performance
for id in start_case_ids:
    case_starts = start_case_grouping.get_group(id).itertuples()
    case_ends = list(end_case_grouping.get_group(id).itertuples())

    # Find the corresponding end activiy for each start activity
    for start in case_starts:
        end = next((entry for entry in case_ends if (
            entry.activity_key == start.activity_key 
            and entry.resource == start.resource # fair to assume this, right?
            and entry.timestamp >= start.timestamp
        )), None)

        if(end == None):
            unmatched_entries.append(start)
        else:
            start_end_log.append(merge_start_end(start, end))
            case_ends.remove(end)
    
    unmatched_entries.extend(case_ends) # only unmatched end_entries will be left

real_log = pd.DataFrame(start_end_log)

# Aggregate average cycle times per activity type
activity_cycle_times = real_log.assign(cycle_time = lambda entry : entry["end_date"] - entry["start_date"])
average_cycle_times = activity_cycle_times.groupby("activity_key")["cycle_time"].mean()

# Approximate start / end times of unmatched entries with types, where an average could be determined
# If it can't be approxiamted, assume it's an automatic activity => start time = end time
# TODO: Improve the approximation to take averages/medians of clusters
# TODO: Approximate unmatched eventy types by (end date of previous event - average waiting time)
# instead of just assuming they're all automatic
def create_event (entry, approx_start = None, approx_end = None):
    event = dict()
    event["activity_key"] = entry.activity_key
    event["resource"] = entry.resource
    event["case_id"] = entry.case_id
    
    if(approx_start):
        event["start_date"] = approx_start
        event["end_date"] = entry.timestamp
    elif(approx_end):
        event["start_date"] = entry.timestamp
        event["end_date"] = approx_end

    return event

start_end_log = []

for entry in unmatched_entries:
    if(entry.transition == "COMPLETE"): # end entry
        if(entry.activity_key in start_activity_types):
            start_end_log.append(
                create_event(entry = entry, approx_start = entry.timestamp - average_cycle_times[entry.activity_key])
            )
        else:
            start_end_log.append(create_event(entry = entry, approx_start = entry.timestamp)) # => Automatic event
    else: # start entry
        start_end_log.append(
            create_event(entry = entry, approx_end = entry.timestamp + average_cycle_times[entry.activity_key])
        )

approx_log = pd.DataFrame(start_end_log)

# Merge the finished start/end-time logs
log_4_sim = pd.concat([real_log, approx_log], axis=0)