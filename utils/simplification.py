import osmnx as ox

def node_simplification(G, nodes_to_simplify, node_closeness):


    simplification_subgraph = G.subgraph(nodes_to_simplify) # Generating the subgraph of the nodes to be simplified

    nodes, data = zip(*simplification_subgraph.nodes(data=True))# getting the data about the nodes

    # Extracting x (longitude) and y (latitude) separately
    x_coords, y_coords = zip(*[(d['x'], d['y']) for d in data])

    removal = list()
    for i in range(0,len(nodes)-1):
        # Comparing the node i with the rest of the nodes

        if i < len(nodes): # ensuring we don't get out of the list

            # Basically what happens here is that we compare all the nodes i with all the nodes that come after them
            lat1 = y_coords[i]
            lon1 = x_coords[i]
            lat2 = y_coords[i+1:]
            lon2 = x_coords[i+1:]

            dist_between_nodes = ox.distance.great_circle(lat1, lon1, lat2, lon2, earth_radius=6371009)

            for m in range(0, len(dist_between_nodes)):
                if dist_between_nodes[m] < node_closeness:
                    removal.append(nodes[i+m+1]) # this allows us to get the index of the node that i is being compared to. The reason why we don't remove it immediately is because indexing then get's messed up.

    R_s_simplified = [x for x in nodes if x not in removal]
    return R_s_simplified