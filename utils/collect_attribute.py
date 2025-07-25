
def attribute_collector(G, path,edges_data):
    """
    Gets the values of an attribute in a list attribute throughout the whoe path.

    :param G: MultiDiGraph to be worked with
    :param path: path for which the attribute values are to be gather
    :param edges_data: the values of the edges' attributes acquired through the following or similar: "nx.get_edge_attributes(G.subgraph(combinedPath), "length")"
    :return:
    """
    attribute_values = []

    for i in range(len(path) - 1):  # -1 because edges and +1 on the line below, the last one is source
        u, v = path[i], path[i + 1]

        edge_length = None

        for key in G[u][v]:  # iterate over all edge keys
            if (u, v, key) in edges_data:  # we can ignore the key because the length is the same anyway
                value = edges_data[(u, v, key)]
                # print(value)
                break

       # If no value for this edge:
        if value is None: # is this happens for pavement: nothing to worry about :D Just osm lacking data
            continue


        attribute_values.append(value)

    return attribute_values