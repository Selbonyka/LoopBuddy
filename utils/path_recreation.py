def get_path_from_predecessor(target_nodes, predecessors, reversal = False):  # outputs in format {node: path to node}
    """
    Robust generation of a path, based on the predecessor list. Targeted to be used with the predecessors dict outputted
    by nx.dijkstra_predecessor_and_distance.
    It is important to note that the path generated is reversed in a sense when reversal is set to False,
    as we go in direction of the predecessors dict, so it is important to reverse the path when necessary

    :param target_nodes: list of nodes for which paths need to be created
    :param predecessors: dict of predecessors in format node:[predecessor]
    :param reversal: dictates if the path should be reversed at the output, set to False by default
    :return: return a dictionary in format {node: [path from node to start]}
    """

    paths_dict = {}
    # Find out the paths for each of the nodes in the target dict:
    for node in target_nodes:

        current_node = node

        paths_dict[node] = [node]  # initializing list for this node and adding the first node itself

        while len(predecessors[current_node]) > 0:
            parent = predecessors[current_node][0]

            paths_dict[node].append(parent)

            current_node = parent

        if reversal:
            paths_dict[node].reverse()


    return paths_dict
