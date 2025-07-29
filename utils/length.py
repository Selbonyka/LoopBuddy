

# just a note on why length is separate from path_lengths_and_rs_prime: it makes more sense to split these into two due to the cashing mechanism used to optimize Rs,
# which is not as essential, or could be even dangerous (for example for looped paths) when used for purely legth/calculation of other attributes

def length(G, path,edges_data):
    """
    Efficiently sums the values of a particulate numerical attribute throughout the whoe path. Intended for length, however can be used with any numerical attribute.

    :param G: MultiDiGraph to be worked with
    :param path: path for which the length is to be calculaed
    :param edges_data: the length of the edges acquired through the following or similar: "nx.get_edge_attributes(G.subgraph(combinedPath), "length")"
    :return:
    """
    total_length = 0

    for i in range(len(path) - 1):  # -1 because edges and +1 on the line below, the last one is source
        u, v = path[i], path[i + 1]

        edge_length = None

        for key in G[u][v]:  # iterate over all edge keys
            if (u, v, key) in edges_data:  # we can ignore the key because the length is the same anyway
                edge_length = edges_data[(u, v, key)]
                break

        # If edge wasn't found:
        if edge_length is None:
            print(f"Warning: Edge ({u}, {v}) not found!")
            continue

        total_length += edge_length
    return total_length



def path_lengths_and_rs_prime (G, source, paths, lengths_edges_Rs, bounds_Rs_prime_traversing=[], mode =""):
    """
    Helper function to find out the true lengths of the Rs-generated paths, as well as find out the Ring S' simultaneously.
    Additionally used in Ru' due to its caching mechanism.

    :param G: MultiDiGraph to be worked on
    :param source: starting point
    :param paths: list of paths that lead to points in Rs (mode: reversed)
    :param lengths_edges_Rs: dictionary storing edges and the length values in the format {(u,v,key):length}
    :param bounds_Rs_prime_traversing: bounds used to find Rs' prime, dictated by the formula [((1-alpha)*L/4 - error),((1-alpha)*L/4 + error)]
            adapted from Gemsa et al. to support movement from node in Rs -> point_s
    :return:
    """

    length_cache = {source: 0} # since source will be always 0

    R_s_prime_options = {}

    for node in paths:  # reminder: node is the end node that djinkstra found
        path = paths[node]
        total_length = 0

        for i in range(len(path) - 1):  # -1 because edges and +1 on the line below, the last one is source
            u, v = path[i], path[i + 1]

            edge_length = None

            for key in G[u][v]:  # iterate over all edge keys
                if (u, v, key) in lengths_edges_Rs:  # we can ignore the key because the length is the same anyway
                    edge_length = lengths_edges_Rs[(u, v, key)]
                    break

            # If edge wasn't found:
            if edge_length is None:
                print(f"Warning: Edge ({u}, {v}) not found!")
                continue


            total_length += edge_length

            if mode =="Rs": # creating R's prime when running the function for Rs

                # storing the R_s'
                if (total_length > bounds_Rs_prime_traversing[0]) and (total_length < bounds_Rs_prime_traversing[1]):
                    # here we create a dictionary {u':u}, so we know to which u the u' belongs. It's important to note that
                    # the same u' can belong to several u ,as u, especially on longer distances, could be just different end turns

                    # appending to the Rs' storage:
                    if R_s_prime_options.get(v) is None:  # checking if the storage is empty
                        R_s_prime_options[v] = [node]
                    else: # if there is already a node in, we can just append to the list
                        R_s_prime_options[v].append(node)

            # if we already cached v's length, reusing it
            if v in length_cache:
                total_length += length_cache[v]
                break  # because we already know the rest of the length

        length_cache[node] = total_length


    if mode == "Rs":
        return length_cache, R_s_prime_options
    else:
        return length_cache