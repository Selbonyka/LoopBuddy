def get_pen_weight_and_length(G, path):
    penalized_weight = 0
    length = 0
    for u, v in zip(path[:-1], path[1:]):
        edge_data = G.get_edge_data(u, v, default={})
        # If multiple edges (like for multigraph), pick first
        if isinstance(edge_data, dict) and 0 in edge_data:
            edge_data = edge_data[0]
        penalized_weight += edge_data.get("penalized_weight", 0)
        length += edge_data.get("length", 0)
    return penalized_weight, length
