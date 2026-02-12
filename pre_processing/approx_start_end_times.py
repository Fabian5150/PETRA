import pandas as pd

"""
Takes a log with a lifecylce:transition column
to approximate missing start and end times for each activity
TODO: Refactor this mess
"""
def approx_start_end_times(log, start_lifecycle_name = "START", end_lifecycle_name = "COMPLETE"):
    start_entries = log[log["lifecycle:transition"] == start_lifecycle_name].sort_values(by="time:timestamp")
    end_entries = log[log["lifecycle:transition"] == end_lifecycle_name].sort_values(by="time:timestamp")

    # Get all activity types which are in end_entries, but not in start_entries or schedule_entries
    start_activity_types = set(start_entries["concept:name"].unique())
    end_activity_types = set(end_entries["concept:name"].unique())

    unmatched_activity_types = list(end_activity_types - start_activity_types)

    start_case_grouping = start_entries.groupby("case:concept:name")
    start_case_ids = list(start_case_grouping.groups.keys())

    end_case_grouping = end_entries.groupby("case:concept:name")

    start_end_log = []
    unmatched_entries = [] # unmatched start or end entries => approximate their corresponding start/end date

    # merge start and end entries into one activity with start and end timestamps
    def merge_start_end (start, end):
        event = dict()
        event["concept:name"] = start["concept:name"]
        event["org:resource"] = start["org:resource"]
        event["case:concept:name"] = start["case:concept:name"]
        event["start_date"] = start["time:timestamp"]
        event["end_date"] = end["time:timestamp"]

        return event

    for id in start_case_ids:
        case_starts = start_case_grouping.get_group(id).itertuples()
        case_ends = list(end_case_grouping.get_group(id).itertuples())

        # Find the corresponding end activiy for each start activity
        for start in case_starts:
            end = next((entry for entry in case_ends if (
                entry["concept:name"] == start["concept:name"] 
                and entry["org:resource"] == start["org:resource"] # fair to assume this, right?
                and entry["time:timestamp"] >= start["time:timestamp"]
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
    average_cycle_times = activity_cycle_times.groupby("concept:name")["cycle_time"].mean()

    # Approximate start / end times of unmatched entries with types, where an average could be determined
    # If it can't be approxiamted, assume it's an automatic activity => start time = end time
    def create_event (entry, approx_start = None, approx_end = None):
        event = dict()
        event["concept:name"] = entry["concept:name"]
        event["org:resource"] = entry["org:resource"]
        event["case:concept:name"] = entry["case:concept:name"]
        
        if(approx_start):
            event["start_date"] = approx_start
            event["end_date"] = entry["time:timestamp"]
        elif(approx_end):
            event["start_date"] = entry["time:timestamp"]
            event["end_date"] = approx_end

        return event

    start_end_log = []

    for entry in unmatched_entries:
        if(entry.transition == end_lifecycle_name): # end entry
            if(entry["concept:name"] in start_activity_types):
                start_end_log.append(
                    create_event(entry = entry, approx_start = entry["time:timestamp"] - average_cycle_times[entry["concept:name"]])
                )
            else:
                start_end_log.append(create_event(entry = entry, approx_start = entry["time:timestamp"])) # => Automatic event
        else: # start entry
            start_end_log.append(
                create_event(entry = entry, approx_end = entry["time:timestamp"] + average_cycle_times[entry["concept:name"]])
            )

    approx_log = pd.DataFrame(start_end_log)

    # Merge the finished start/end-time logs
    log = pd.concat([real_log, approx_log], axis=0)

    # Assign all entries without resource to a global orphanage resource
    log["org:resource"] = log["org:resource"].fillna("GLOBAL")

    return log