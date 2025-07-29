from utils.path_recreation import get_path_from_predecessor
from utils.length import path_lengths_and_rs_prime
import networkx as nx
import osmnx as ox

def ring_s_and_sprime_handling(G, point_s,bounds_Rs_penalized, bounds_Rs_prime_traversing, bounds_Rs):
    """
    Generates Ring S and calculates Ring S'

    :param G: MultiDiGraph with loaded in user preferences
    :param point_s: starting point
    :param bounds_Rs_penalized: bounds for the quarter distance (with error) that take into account the max to which user preferences can skew distance
    :param bounds_Rs_prime_traversing: actual distance bounds for Rs'
    :param bounds_Rs: actual distance bounds for Rs
    :return: returns R_s_lengthwise, R_s_prime, penalized_distances, paths_R_s
    """

    # Generating a ring of paths from s until the cutoff
    predecessors, penalized_distances = nx.dijkstra_predecessor_and_distance(G, point_s,cutoff=(bounds_Rs_penalized[1]),weight="penalized_weight")
    # reminder: the cutoff point is the length limit * length_adjustment from weights being applied to not cutoff too early

    # getting out the preliminary Ring S: the nodes in distances inside the penalizined error bounds.
    # Needs to be done, as the function above outputs the whole list of nodes instead of just the Rs
    R_s_penalized = {node for node, dist in penalized_distances.items() if bounds_Rs_penalized[0] <= dist <= bounds_Rs_penalized[1]}

    paths_R_s = get_path_from_predecessor(R_s_penalized, predecessors)  # stores in the format {node: path}

    # Getting true lengths and generating Rs' (combined to increase computational efficiency)
    rings_s_SG = G.subgraph(predecessors) # generating a subgraph of all the edges we need
    lengths_edges_Rs = nx.get_edge_attributes(rings_s_SG, "length") # getting the edges out of the subgraph with respective lengths
    length_cache_Rs, R_s_prime_options = path_lengths_and_rs_prime(G, point_s, paths_R_s, lengths_edges_Rs,bounds_Rs_prime_traversing, mode="Rs")

    # Rs nodes in the length boundaries
    R_s_lengthwise = {node for node, dist in length_cache_Rs.items() if bounds_Rs[0] <= dist <= bounds_Rs[1]}  # getting out the Ring S, which is the nodes in distances inside the error bounds

    # Now we need to filter out the Rs' options (u') for which u was not taken into R_s

    R_s_prime = {}

    for uprime, list_of_u in R_s_prime_options.items():# iterating through the u'
        for u in list_of_u: # iterating through the list of u's
            if u in R_s_lengthwise:
                # Checking if the entry already exists in the dictionary or not:
                if R_s_prime.get(uprime) is None:  # here we create a dictionary {u':u}, so we know to which u the u' belongs.
                    R_s_prime[uprime] = [u]
                else:
                    R_s_prime[uprime].append(u)

    return  R_s_lengthwise, R_s_prime, penalized_distances,paths_R_s