# Because the RL Pathfinder uses the event log, it's output might not exactly match the later mined bpmn model
# So the output path must be adjusted to get an actual start to end path in the bpmn model

from collections import deque

def match_rl_path_to_bpmn(bpmn_graph, rl_path):
    name_to_node = {}
    for node in bpmn_graph.get_nodes():
        name = node.get_name()
        if name:
            name_to_node[name] = node
    
    full_path = []
    
    for i in range(len(rl_path) - 1):
        from_name = rl_path[i]
        to_name = rl_path[i + 1]
        
        if from_name not in name_to_node or to_name not in name_to_node:
            print(f"Node not found: {from_name} or {to_name}")
            continue
        
        from_node = name_to_node[from_name]
        to_node = name_to_node[to_name]
        
        sub_path = find_shortest_path_bpmn(bpmn_graph, from_node, to_node)
        
        if sub_path:
            if i == 0:
                full_path.extend(sub_path)
            else:
                full_path.extend(sub_path[1:])  # skip duplicate
    
    return full_path


def find_shortest_path_bpmn(bpmn_graph, start_node, end_node):
    queue = deque([[start_node]])
    visited = set()
    
    while queue:
        path = queue.popleft()
        current = path[-1]
        
        if current.get_id() == end_node.get_id():
            return [
                node.get_name() 
                for node in path 
                if node.get_name() # skip gateways
            ]
        
        if current.get_id() in visited:
            continue
        visited.add(current.get_id())
        
        for flow in bpmn_graph.get_flows():
            if flow.get_source() == current:
                next_node = flow.get_target()
                if next_node.get_id() not in visited:
                    queue.append(path + [next_node])
    
    return None