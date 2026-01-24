import pm4py as pm

def get_bpmn_heuristic(data):
    net, im, fm = pm.discover_petri_net_heuristics(data)

    bpmn = pm.convert_to_bpmn(net, im, fm)

    return bpmn

def get_bpmn_inductive(data, noise_threshold = 0.0):
    bpmn = pm.discover_bpmn_inductive(
        log = data,
        noise_threshold = noise_threshold
    )

    return bpmn