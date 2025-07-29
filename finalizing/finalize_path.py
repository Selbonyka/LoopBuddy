import networkx as nx
from finalizing.sharing_filter import sharing_filter
from utils.length import length
from utils.elevation_calculation import compute_elevation_change
from tqdm import tqdm
from difflib import SequenceMatcher

def is_valid_path(G, path):
    return all(G.has_edge(path[i], path[i+1]) for i in range(len(path) - 1))


def concatenate_path(G, m_paths_storage, paths_R_s, sharing_allowance, point_s, total_length_bounds, elevation_bounds):
    """
    Concatenates paths and evaluates them based on sharing, length and elevation

    :param G: MultiDiGraph of the geographical area
    :param m_paths_storage: storage in the format {m:{u: path to m that goes through this u}}
    :param paths_R_s: Paths from s to u in the format: {node: path}
    :param sharing_allowance: % of (max value of how many edges can be visited more than once/total edges) expressed in bounds [0,1]
    :param point_s: starting point
    :param total_length_bounds: original length bounds adjusted for error
    :param elevation_bounds: original elevation bounds adjusted for error
    :return: finalized_paths,paths_badness, paths_lengths, paths_elevations, elevation_failure
    """

    finalized_paths = []
    paths_lengths = []
    paths_elevations = []
    paths_badness = []
    elevation_appropriate = 0
    distance_filter_passed = False

    # filtering out the nodes that only have both u and v:
    valid_m_nodes = [m[0] for m in G.nodes(data=True) if "Mm" in m[1] and len(m[1]["Mm"]) > 1]

    for m in tqdm(valid_m_nodes,desc = "Concatenating and filtering paths", total=len(valid_m_nodes)):
        # create the full path:
        u, v = list((G.nodes[m].get("Mm")).keys())  # extracting the u,v values

        # s to u:
        path_s_u = paths_R_s[u] # path_R_s has a bug when it reverses the path for some reason
        if path_s_u[0] != point_s:
            path_s_u.reverse()

        # u to m:
        path_u_m = m_paths_storage[m][u][1:]
        path_u_m.reverse()

        # m to v:
        path_m_v = m_paths_storage[m][v]# [:-1] # no need to reverse, as it's already in this order
        # removing the last element to not cause issues again

        # v to s:
        path_v_s = paths_R_s[v]
        if path_v_s[0] == point_s:
            path_v_s.reverse()


        # concatenated path:
        combinedPath = path_s_u + path_u_m + path_m_v + path_v_s

        for i in range(len(combinedPath) - 1): # raises error if no path between
            if G.has_edge(combinedPath[i], combinedPath[i+1]) is False:
                print("no edge between:", combinedPath[i], combinedPath[i+1])

        # checking for sharing:
        if sharing_filter(combinedPath, sharing_allowance):
            lengths_data = nx.get_edge_attributes(G.subgraph(combinedPath), "length")
            length_path = length(G, combinedPath,lengths_data )

            if total_length_bounds[0]<=length_path <= total_length_bounds[1]: # checking if the path is in bounds
                distance_filter_passed = True


                # checking elevation changes
                pos_change, neg_change = compute_elevation_change(G, combinedPath)
                elevation_appropriate += 1 # this needs to be placed here, otherwise paths that don't count based on length will still count as appropriate
                if elevation_bounds[0]<=pos_change<=elevation_bounds[1]: # based on the logic that since it's a looped route if you come up you must come down
                    badness_data = nx.get_edge_attributes(G.subgraph(combinedPath), "penalized_weight")
                    badness_path = length(G, combinedPath, badness_data)

                    finalized_paths.append(combinedPath)
                    paths_lengths.append(length_path)
                    paths_elevations.append([pos_change, neg_change])
                    paths_badness.append(badness_path)
                else:
                    elevation_appropriate -=1 # the path did not path the elevation condition

    # this is needed for the appropriate error statement
    if elevation_appropriate == 0 & distance_filter_passed == True:
        elevation_failure = True
    else:
        elevation_failure = False


    return finalized_paths,paths_badness, paths_lengths, paths_elevations, elevation_failure


def select_paths (finalized_paths,paths_badness, similiarity_threshold):
    """
    Selects the best paths to display to the user removing those that are worse than the similar ones
    :param finalized_paths: list of lists containing all finalized paths
    :param paths_badness: list of integers containing the badnesses of the respective paths
    :param similiarity_threshold: how similar to each other the paths could be
    :return: a list of lists containing paths that are different enough
    """
    selected_paths = []
    badness_selected = []

    for i in tqdm(range(len(finalized_paths)), desc= "Selecting the best paths", total = len(finalized_paths)): # iterating over the paths we generated
        path = finalized_paths[i]
        badness = paths_badness[i]
        unique = True

        for j in range(len(selected_paths)): # iterating over all the paths we stored
            # returns false if there are no paths like this, so this path is added to selected_paths:
            if SequenceMatcher(None,selected_paths[j], path).ratio()>=similiarity_threshold:  #threshold can be modified to change how similar the paths can be
                unique = False
                if badness < badness_selected[j]:
                    # removing the path and the badness that are worse that the path we are currently analyzing:
                    selected_paths.pop(j)
                    badness_selected.pop(j)

                    # adding the better path
                    selected_paths.append(path)
                    badness_selected.append(badness)
                    break

        if unique:
            selected_paths.append(path)
            badness_selected.append(badness)

    print(f"Removed {len(finalized_paths) - len(selected_paths)} redundant paths \n")

    return selected_paths, badness_selected # badness_selected necessary for evaluation purposes only
