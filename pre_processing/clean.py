import pm4py as pm
from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.algo.filtering.log.variants import variants_filter
import numpy as np

"""
Removes unfinished cases based on the lifecycle:transition column
Transition name is handled case insensitive
"""
def filter_unfinished_cases(data, transition_complete_name = "complete"):
    # determine common last activities
    ends = pm.get_end_activities(data)
    total = sum(ends.values())
    rel_freqs = {act: freq / total for act, freq in ends.items()}

    quant = np.quantile(list(rel_freqs.values()), 0.625) # q75 seemed to restricitve, median to loose
    valid_ends = [act for act, freq in rel_freqs.items() if freq >= quant]

    # compare and intersect with 'lifecycle:transition == complete'-acitivities
    if("lifecycle:transition" in data.columns):
        complete_acts = list(data[data["lifecycle:transition"].str.lower() == transition_complete_name]["concept:name"].unique())

        intersect = list(set(valid_ends) & set(complete_acts))
        valid_ends = intersect if len(intersect) != 0 else valid_ends

    filtered_data = end_activities_filter.apply(data, valid_ends)

    return pm.convert_to_dataframe(filtered_data)

"""
Removes all cases that don't cover 90% of the most frequent variants
"""
def filter_rare_variants(data, coverage = 0.9):
    variants_stats = case_statistics.get_variant_statistics(data)
    variants_stats.sort(key=lambda x: x['count'], reverse = True)

    total_cases = data["case:concept:name"].nunique()
    
    cum_count = 0
    keep_variants = []
    
    for var in variants_stats:
        cum_count += var['count']
        keep_variants.append(var['variant'])
        
        if cum_count / total_cases >= coverage:
            break

    return pm.convert_to_dataframe(variants_filter.apply(data, keep_variants))

"""
Full cleaning pipeline
"""
def clean(data): 
    return (data
        .pipe(filter_unfinished_cases)
        .pipe(filter_rare_variants)
    )