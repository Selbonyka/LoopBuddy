
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from itertools import islice
import pickle
import copy

from finalizing.finalize_path import concatenate_path,select_paths
from utils.penalizing import edge_penalizing
from rings.s_and_s_prime import ring_s_and_sprime_handling
from rings.uprime_rings import generate_uprime_rings


"""
Note space
- node closeness not imported, as simplification is still not decided upon

"""


def main(start_point, preferences, graph_filepath):

    """

    :param start_point: starting point, as (longitude, latitude)
    :param preferences: contains the dictionary containing the following user preferences:
        total_length
        elevation_requested: target elevation
        elevation_error: acceptable elevation deviation from target
        pavement_preference: one from: paved, neutral, unpaved
        stoplights_preference: one from: avoid, neutral, prefer
        steps_preference: one from: avoid, neutral, prefer
        sharing_allowance: [0-1] - amount of sharing acceptable
        allowed_distance_between_nodes: limits how close via-vertices could be to each other
        stoplight_penalty_strength: bounds: [1:]
        steps_penalty_strength: bounds: [1:]
        pavement_penalty_strength: bounds: [1:]
        error: error term for length calculations
        alpha: smoothing factor
    :param graph_filepath: path to the file containing the pre-processed graph

    :return: returns a list of lists with path options
    """

    # <editor-fold desc="Setup">


    ### loading in the pre-generated graph that already has stoplights, elevation, pavement data:
    print("\nLoading the graph!\n")
    with open(graph_filepath, "rb") as f:
        G = pickle.load(f)
    print("Graph loaded succesfully!\n")


    # starting point:
    point_s = ox.distance.nearest_nodes(G,start_point[0], start_point[1])

    # loading in the preferences:
    ### preferences that later become a weight:
    pavement_preference = preferences['pavement_preferences']
    stoplights_preference = preferences['stoplights_preference']
    steps_preference = preferences['steps_preference']

    ### and their weights:
    stoplight_penalty_strength = preferences['stoplight_penalty_strength']
    steps_penalty_strength = preferences['steps_penalty_strength']
    pavement_penalty_strength = preferences['pavement_penalty_strength']

    ## length module:
    total_length = preferences['total_length']
    error = preferences['error']

    # used as a cutoff point when running penalized djinkstra
    length_adjustment = stoplight_penalty_strength * steps_penalty_strength * pavement_penalty_strength

    total_length_bounds = [total_length - error, total_length + error]
    quarter_length = total_length / 4

    ### bounds generation

    bounds_Rs = [quarter_length - error, quarter_length + error]

    bounds_Rs_penalized = [bounds_Rs[0], bounds_Rs[
        1] * length_adjustment]  # we are penalizing the upper bound because it could be higher, but keeping the lower one the same

    # For Ring R_s_prime
    alpha = preferences['alpha']  # scaling parameter, values should be between [0.5,1]
    bounds_Rs_prime = [(alpha * quarter_length) - error, (alpha * quarter_length) + error]

    # from Gemsa et al., modified to work in reverse (so from node in Rs to point_s)
    bounds_Rs_prime_traversing = [((1 - alpha) * quarter_length) - error, ((1 - alpha) * quarter_length) + error]


    bounds_Rs_prime_penalized = [bounds_Rs_prime[0], bounds_Rs_prime[
        1] * length_adjustment]  # same logic as for R_s penalized # actually could be possible that we don't need it

    # For Ring R_u_prime
    bounds_Ru_prime = [((2 - alpha) * quarter_length) - error, ((2 - alpha) * quarter_length) + error]
    # print(bounds_Ru_prime)

    bounds_Ru_prime_penalized = [bounds_Ru_prime[0], bounds_Ru_prime[1] * length_adjustment]

    # elevation module
    elevation_requested = preferences['elevation_requested']
    elevation_error = preferences['elevation_error']
    elevation_bounds = [elevation_requested-elevation_error, elevation_requested+elevation_error]

    # tweaks
    # space for node closeness if decided to be imported
    allowed_distance_between_nodes = preferences['allowed_distance_between_nodes']
    sharing_allowance = preferences['sharing_allowance']


    # </editor-fold>

    # <editor-fold desc="Setup">

    # adds the penalties to the edges based on user's inputs and the edge status

    G = edge_penalizing(G, stoplights_preference, steps_preference,pavement_preference,stoplight_penalty_strength, steps_penalty_strength, pavement_penalty_strength)

    # ring_s_and_sprime_handling(G, point_s, bounds_Rs_penalized, bounds_Rs_prime_traversing, bounds_Rs)

    # Generate Rings S and S':
    print("\nGenerating the Rs and Rs' prime")
    R_s, R_s_prime, pen_dist_Rs,paths_R_s = ring_s_and_sprime_handling(G, point_s,bounds_Rs_penalized, bounds_Rs_prime_traversing, bounds_Rs)
    print("\nGeneration of Rs and R's prime complete!\n")


    # Generate ring uprime and append to nodes the Mm data

    print("Starting to generate rings around u' and processing possible m nodes\n")
    m_paths_storage = generate_uprime_rings(G, R_s_prime, bounds_Ru_prime_penalized, bounds_Ru_prime, pen_dist_Rs)
    print("\nCompleted m generation and processing! \n")


    finalized_paths,paths_badness,path_lengths, paths_elevation = concatenate_path(G, m_paths_storage, paths_R_s, sharing_allowance, point_s, total_length_bounds, elevation_bounds)

    print(len(finalized_paths))
    print(finalized_paths)
    selected_paths = select_paths(finalized_paths,paths_badness)


    print(len(selected_paths))
    return selected_paths
    # return finalized_paths




# <editor-fold desc="Test Runs">

# sample call:
# </editor-fold>
preference_dict_sample = {"total_length":10000, "elevation_requested":0,"elevation_error":10,"pavement_preferences":"Paved",
                          "stoplights_preference":"Avoid", "steps_preference":"Avoid","sharing_allowance":0.3,
                          "allowed_distance_between_nodes": 300, "stoplight_penalty_strength": 1.1,"steps_penalty_strength":1.2,"pavement_penalty_strength":1.05, "error":70, "alpha":0.6}
graph_filepath= "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/GraphSaves/Weighted1_8.pkl"
finalized_Paths = main((16.3731269,48.2084923),preference_dict_sample, graph_filepath)

print(finalized_Paths)
