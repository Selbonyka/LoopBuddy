import networkx as nx
from finalizing.sharing_filter import sharing_filter
from utils.length import length
from tqdm import tqdm


def is_valid_path(G, path):
    return all(G.has_edge(path[i], path[i+1]) for i in range(len(path) - 1))


def finalize_path(G, m_paths_storage, paths_R_s, sharing_allowance, point_s, total_length_bounds, elevation_bounds):
    finalized_paths = []
    paths_lengths = []
    paths_elevations = []
    # filtering out the nodes that only have both u and v
    valid_m_nodes = [m[0] for m in G.nodes(data=True) if "Mm" in m[1] and len(m[1]["Mm"]) > 1]



    for m in tqdm(valid_m_nodes,desc = "Concatenating and filtering paths", total=len(valid_m_nodes)):

        # create the full path:

        u, v = list((G.nodes[m].get("Mm")).keys())  # extracting the u,v values

        # s to u:
        path_s_u = paths_R_s[u] # path_R_s has a bug when it reverses the path for some reason
        if path_s_u[0] != point_s:
            path_s_u.reverse()


        # print("path su:", path_s_u)

        # u to m:

        path_u_m = m_paths_storage[m][u][1:]
        path_u_m.reverse()
        # print("path_u_m:", path_u_m)


        # m to v:
        path_m_v = m_paths_storage[m][v]# [:-1] # no need to reverse, as it's already in this order
        # removing the last element to not cause issues again
        # print("path_m_v:", path_m_v)

        # v to s:
        path_v_s = paths_R_s[v]
        if path_v_s[0] == point_s:
            path_v_s.reverse()
        # print("path_v_s:", path_v_s)

        # print("v value:", v)

        # concatenated path:
        combinedPath = path_s_u + path_u_m + path_m_v + path_v_s

        # check if it's a valid path:
        # if is_valid_path(G, combinedPath):
        #     print('hi')

        # print(all(G.has_edge(combinedPath[i], combinedPath[i+1]) for i in range(len(combinedPath) - 1)))


        for i in range(len(combinedPath) - 1): # raises error if no path between
            if G.has_edge(combinedPath[i], combinedPath[i+1]) is False:
                print("no edge between:", combinedPath[i], combinedPath[i+1])


        # checking for sharing:
        if sharing_filter(combinedPath, sharing_allowance):
            lengths_data = nx.get_edge_attributes(G.subgraph(combinedPath), "length")
            length_path = length(G, combinedPath,lengths_data )

            if total_length_bounds[0]<=length_path <= total_length_bounds[1]: # checking if the path is in bounds

                # checking elevation:
                elevation_data = nx.get_edge_attributes(G.subgraph(combinedPath), "grade_abs")
                elevation_path = length(G, combinedPath, elevation_data)

                if elevation_bounds[0]<=elevation_path <= elevation_bounds[1]:

                    finalized_paths.append(combinedPath)
                    paths_lengths.append(length_path)
                    paths_elevations.append(elevation_path)


    return finalized_paths,paths_lengths, paths_elevations






