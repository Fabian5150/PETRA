import pm4py as pm

"""
Mines a log with the heuristic miner and returns the bpmn model
Either as pm4py bpmn type or as bpmn 2.0 xml string
"""
def get_bpmn_heuristic(data, as_xml_string = True):
    net, im, fm = pm.discover_petri_net_heuristics(data)

    bpmn = pm.convert_to_bpmn(net, im, fm)

    if(as_xml_string):
        return get_xml_string(bpmn)
    else:
        return bpmn

"""
Mines a log with the inductive miner and returns the bpmn model
Either as pm4py bpmn type or as bpmn 2.0 xml string
"""
def get_bpmn_inductive(data, noise_threshold = 0.0, as_xml_string = True):
    bpmn = pm.discover_bpmn_inductive(
        log = data,
        noise_threshold = noise_threshold
    )

    if(as_xml_string):
        return get_xml_string(bpmn)
    else:
        return bpmn

"""
Serializes a bpmn pm4py bpmn type model into a standard bpmn 2.0 xml string
that bpmn-js can directly read
"""
def get_xml_string(bpmn_model):
    _, xml_bytes = pm.serialize(bpmn_model)  
    return xml_bytes.decode('utf-8')