

from tqdm import tqdm

import networkx as nx


from utils.path_recreation import get_path_from_predecessor
from utils.length import path_lengths_and_rs_prime
from utils.length import length


def generate_uprime_rings(G, R_s_prime, bounds_Ru_prime_penalized, bounds_Ru_prime, pen_dist_Rs):
    """
    Generates rings around u' based on nodes (and parent nodes) and marked valid through poins by assigning them the attribute
    Mm with the u value and badness of that an option. (max amount of u values = 2)

    :param G: MultiDiGraph of the geographical area
    :param R_s_prime: dictionary of the format: {u':u}
    :param bounds_Ru_prime_penalized: distance bounds, with upper bound penalized by the max impact from user preferences
    :param bounds_Ru_prime: distance bounds
    :param pen_dist_Rs: dict of {node : distances * weight (user preferences)} for Ring S
    :return: returns m_paths_storage in format {m:{u: path to m that goes through this u}}
    """

    m_paths_storage = {} # format: {m:{u: path to m that goes through this u}}

    for u_prime ,u in tqdm(R_s_prime.items(), desc = "Generating and processing u' rings", total = len(R_s_prime)):

        # Generating rings around each u'
        predecessors_uprime, pen_dist_uprime = nx.dijkstra_predecessor_and_distance(G, u_prime, cutoff=bounds_Ru_prime_penalized[1],  weight="penalized_weight")

        R_uprime_penalized = {node for node, dist in pen_dist_uprime.items() if bounds_Ru_prime_penalized[0] <= dist <= bounds_Ru_prime_penalized[1]} # getting the nodes that are theoretically inside the error bounds
        R_uprime_paths_prelim = get_path_from_predecessor(R_uprime_penalized,predecessors_uprime) # prelim, because not sorted by length. Also not reversed for consistency's sake

        lengths_SG_Ring_u_prime = nx.get_edge_attributes(G.subgraph(predecessors_uprime), "length")  # lengths necessary to calculate true length

        length_cache_Ru_prime = path_lengths_and_rs_prime(G, u_prime, R_uprime_paths_prelim, lengths_SG_Ring_u_prime, mode ="Ru")  # true length

        R_uprime_lengthwise = {node for node, dist in length_cache_Ru_prime.items() if bounds_Ru_prime[0] <= dist <= bounds_Ru_prime[1]}  # So now we have a ring around u'
        R_u_paths = {node: path for (node, path) in R_uprime_paths_prelim.items() if node in R_uprime_lengthwise}  # sorting out the actual paths that were included in the Ru'


        # Now we process the m candidates:
        for m, m_path in R_u_paths.items(): # are you sure we aren't getting m's where the path is basically identical? because acccording to this we could be :D

            intersection = list(set(u) & set(m_path)) # finds out all the u values that are on the path to m

            if len(intersection) >0: # checking if there are any intersections

                # we need to find out the badness per possible s->m path to evaluate it.
                # We already have the s->u badness stored in the pen_dist_Rs[u], so all we have to do is get the badness
                # for u -> m (but the one generated by dijkstra is from u',  so we need to process the path)

                m_s_badness = {} # a storage of badness for the path m -> s, through  a set u in the format {u:badness}
                m_u_paths = {}

                # Going through all nodes that intersect:
                for intersection_node in intersection: # iterates through all the possible u values for this m
                    path_m_u = m_path[:m_path.index(intersection_node)] # crops the path to m_u

                    # Checking length:
                    lengths_SG_Ring_u_prime = nx.get_edge_attributes(G.subgraph(path_m_u), "length")  # lengths necessary to calculate true length
                    length_cache_Ru_prime = length(G, path_m_u, lengths_SG_Ring_u_prime)  # true length

                    # Checking penalized length:
                    pen_weight_SG_Ring_u_prime = nx.get_edge_attributes(G.subgraph(path_m_u), "penalized_weight")
                    pen_weight_cache_SG_Ring_u_prime = length(G, path_m_u, pen_weight_SG_Ring_u_prime)  # penalized weight of the path

                    # Calculating badness for path m -> u as penalized weight - actual length:
                    badness_m_u = pen_weight_cache_SG_Ring_u_prime-length_cache_Ru_prime

                    # Calculating the badness of the path m_s:
                    total_badness = badness_m_u + pen_dist_Rs[intersection_node]

                    # Assigning the value to storage:
                    m_u_paths[intersection_node] = path_m_u
                    m_s_badness[intersection_node] = total_badness

                Mm_status = G.nodes[m].get("Mm") # getting the current status of the node m

                if Mm_status is None: # the case when the node hasn't been reached before

                    best_u = min(m_s_badness, key=lambda k: m_s_badness[k]) # just taking the best u as it is, as there are no checks needed, since it's the first one

                    G.nodes[m].update({"Mm" :{best_u: m_s_badness[best_u]}})  # updating th attribute with the values

                    path_m_u = {best_u:m_u_paths[best_u]}  # geting the path m_u and storing it

                    # Activating and storing the m in the m_paths_storage
                    m_paths_storage[m] = {}
                    m_paths_storage[m].update(path_m_u)

                elif len(Mm_status )>= 1: # case when we already have 1 or 2 u's

                    if len(Mm_status) ==1 :

                        # trying to get the m and m_path out of storage for this m:
                        try:
                            stored_path = list(m_paths_storage[m].values())[0]

                        except Exception as e: # Exceptions can occur if the writing process bugged out
                            print(e)
                            print("m value:", m)
                            print("path storage state:", m_paths_storage[m])
                            continue


                        valid_u_candidates = {}

                        for candidate,badness in m_s_badness.items():
                            if list(m_paths_storage[m].keys())[0] != candidate: # checking that the u that is alredy stored for this m is not the same as the u we are at

                                if stored_path[:2] != m_u_paths[candidate][:2]: # checking if the last edge is not the same:
                                    valid_u_candidates[candidate] = badness # adding the option to candidates

                        if len(valid_u_candidates) >0: # checking if any candidates were found at all
                            best_u = min(valid_u_candidates, key=lambda k: valid_u_candidates[k]) # adding the valid candidate with the min badness
                            Mm_status[best_u] = m_s_badness[best_u]

                            path_m_u = {best_u: m_u_paths[best_u]}
                            m_paths_storage[m].update(path_m_u)  # adding this path to m path storage
                        else:
                            continue # if no valid candidates found just continue to the next m


                        # The case when we already got two nodes stored in the attribute:
                        if len(Mm_status) > 2:

                            for candidate, badness in m_s_badness.items(): # going over each candidate found before

                                stored_u, stored_v = list(Mm_status.keys())

                                # Checking if the node is better than the stored u node and doesn't share the last edge with v and isn't v
                                if badness < Mm_status[stored_u] and (m_paths_storage[m][stored_v][:2] != m_u_paths[candidate][:2]) and candidate != stored_v:

                                    # Removing the stored u:
                                    Mm_status.pop(stored_u, None)
                                    if stored_u in m_paths_storage[m]:
                                        m_paths_storage[m].pop(stored_u)

                                    # Adding the new u:
                                    Mm_status[candidate] = m_s_badness[candidate]
                                    path_m_u = {candidate: m_u_paths[candidate]}
                                    m_paths_storage[m].update(path_m_u)

                                    # Same logic for comparison with v, if the comparison with u fell through
                                elif badness < Mm_status[stored_v] and (m_paths_storage[m][stored_u][:2] != m_u_paths[candidate][:2]) and candidate != stored_u:
                                    # Removing the stored v:
                                    Mm_status.pop(stored_v, None)
                                    if stored_v in m_paths_storage[m]:
                                        m_paths_storage[m].pop(stored_v)

                                    # Adding the new v:
                                    Mm_status[candidate] = m_s_badness[candidate]
                                    path_m_u = {candidate:m_u_paths[candidate]}
                                    m_paths_storage[m].update(path_m_u)


                        G.nodes[m].update({"Mm": Mm_status})  # updating the dict at the node (for the case when 1 or more nodes stored in the attribute)

    return m_paths_storage

