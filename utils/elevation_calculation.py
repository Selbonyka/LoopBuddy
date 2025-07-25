
def compute_elevation_change(G, path):
    """
    Computes the positive and negative elevation changes in the path provided
    :param G: Graph which containes the nodes with the path and elevation data
    :param path: Path to be analyzed
    """
    elevations = [G.nodes[n]["elevation"] for n in path]

    pos_change = 0
    neg_change = 0
    for i in range(len(elevations) - 1):
        diff = elevations[i+1] - elevations[i]
        if diff > 0:
            pos_change += diff
        else:
            neg_change += diff
    return pos_change, neg_change