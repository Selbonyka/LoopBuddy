import os
import pickle
import pprint
import time
import pandas as pd

import networkx as nx
from scipy.stats import alpha

from evaluation.processingresults import saving_intermediate, processing_overall
from main import main
from utils.collect_attribute import attribute_collector
from utils.length import length
import random
""" 
Ok so what do we evaluate:
- Speed/badness/number of routes for diff diff preferences
- Number of stoplights
- Number of steps
- Number of pavement types
"""
graph_filepath = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/preloadedmap/Wien.pkl"

def load_graph(graph_filepath):
    # Normal execution
    print("\nLoading the graph!\n")
    with open(graph_filepath, "rb") as f:
        G = pickle.load(f)
    print("Graph loaded succesfully!\n")
    return G

# Setting up the evaluation:
# def overall_evaluation(pavement_pref, stoplight_pref, steps_pref, graph_filepath):
#
#     distance = 0
#     results = {}
#     starting_point = (16.3725042, 48.2083537)  # Historical center of Vienna - Stephansdom. Chosen due to a dense street network
#     # distance = 1000
#     distances = [2000, 5000, 7000, 10000, 15000, 20000]
#
#     for distance in distances: # just looping around the smoothing factor values, 1.1 because computational rounding error
#
#
#         # For clarity when analyzing:
#         dashes = "".join(["-"] * 200)
#         print(dashes)
#         print("Analyzing simplification distance :", distance, "\nMode:", pavement_pref, stoplight_pref, steps_pref)
#         print(dashes)
#
#         # Neutral settings
#         preference_dict = {"total_length": distance, "elevation_requested": 0, "elevation_error": 1000,
#                            "pavement_preferences": pavement_pref,
#                            "stoplights_preference": stoplight_pref, "steps_preference": steps_pref, "sharing_allowance": 0.3,
#                            "node_simplification_status": "True", "allowed_distance_between_nodes": 5,
#                            "stoplight_penalty_strength": 1.1, "steps_penalty_strength": 1.2,
#                            "pavement_penalty_strength": 1.05, "error": 60,
#                            "alpha": 0.8}
#         # Loading the graph:
#         G = load_graph(graph_filepath)
#
#         start_time = time.time()  # we need to measure time, as it's important for the user exprience
#         paths, _, badness = main(starting_point, preference_dict,G)  # we don't need elevation error in this case, as elevation is not considered
#
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#
#         results[distance] = {}
#         results[distance]["Elapsed time"] = elapsed_time
#         results[distance]["Number of paths"] = len(paths)
#
#         # Getting the badness values:
#         true_badness_sum = 0  # sum of badness values with lengths removed. Note: only relecant for when settings not neutral
#
#         stoplights_list = []
#         steps_list = []
#
#         stoplight_counter = 0
#         steps_counter = 0
#         pavement_types_list = []
#
#         for i in range(len(paths)):
#             path = paths[i]
#
#             # gathering additional info:
#             stoplight_data = nx.get_edge_attributes(G.subgraph(path), "stoplights")
#             stoplights_list=stoplights_list+attribute_collector(G, path, stoplight_data)
#             step_data = nx.get_edge_attributes(G.subgraph(path), "steps")
#             steps_list= steps_list+attribute_collector(G, path, step_data)
#             pavement_data = nx.get_edge_attributes(G.subgraph(path), "surface")
#             pavement_types_list = pavement_types_list+attribute_collector(G, path, pavement_data)
#             print("stoplights_list list")
#             print(stoplights_list)
#
#             if pavement_pref != "Neutral" or stoplight_pref != "Neutral" or steps_pref != "Neutral":
#                 lengths_data = nx.get_edge_attributes(G.subgraph(path), "length")
#                 path_length = length(G, path, lengths_data)
#                 true_badness = badness[i] - path_length
#                 true_badness_sum += true_badness
#
#         if len(paths) > 0:
#             results[distance]["Average paths badness"] = true_badness_sum / len(paths)
#
#             results[distance]["Avg. number of stoplights"] = sum(stoplights_list) / len(paths)
#             results[distance]["Avg. number of steps"] = sum(steps_list) / len(paths)
#             results[distance]["Avg. number of paved edges"] = pavement_types_list.count("paved") / len(paths)
#             results[distance]["Avg. number of unpaved edges"] = pavement_types_list.count("unpaved") / len(paths)
#             results[distance]["Avg. number of edges with unknown surface"] = (len(pavement_types_list) - pavement_types_list.count(
#                                                                                      "paved") - pavement_types_list.count(
#                                                                                      "unpaved")) / len(paths)
#         else:
#             results[distance]["Average paths badness"] = 0
#             results[distance]["Avg. number of stoplights"] = 0
#             results[distance]["Avg. number of steps"] = 0
#             results[distance]["Avg. number of paved edges"] = 0
#             results[distance]["Avg. number of unpaved edges"] = 0
#             results[distance]["Avg. number of edges with unknown surface"] = 0
#
#         print(dashes)
#         pprint.pprint(results)
#     return results
def overall_evaluation(pavement_pref, stoplight_pref, steps_pref, graph_filepath, distance, coordinates_list, alpha, simplfication_param):

    results = {}

    for coordinate in coordinates_list: # just looping around the smoothing factor values, 1.1 because computational rounding error

        # For clarity when analyzing:
        dashes = "".join(["-"] * 200)
        print(dashes)
        print("Analyzing simplification coordinate :", coordinate, "\nMode:", pavement_pref, stoplight_pref, steps_pref)
        print("For distance " + str(distance))
        print(dashes)

        # Neutral settings
        preference_dict = {"total_length": distance, "elevation_requested": 0, "elevation_error": 10000,
                           "pavement_preferences": pavement_pref,
                           "stoplights_preference": stoplight_pref, "steps_preference": steps_pref, "sharing_allowance": 0.3,
                           "node_simplification_status": "True", "allowed_distance_between_nodes": simplfication_param,
                           "stoplight_penalty_strength": 1.1, "steps_penalty_strength": 1.2,
                           "pavement_penalty_strength": 1.05, "error": 60,
                           "alpha": alpha}
        # Loading the graph:
        G = load_graph(graph_filepath)

        start_time = time.time()  # we need to measure time, as it's important for the user exprience
        paths, _, badness = main(coordinate, preference_dict,G)  # we don't need elevation error in this case, as elevation is not considered

        end_time = time.time()
        elapsed_time = end_time - start_time

        coordinate = str(coordinate) # so we get no issues later on with the formatting

        results[coordinate] = {}
        results[coordinate]["Elapsed time"] = elapsed_time
        results[coordinate]["Number of paths"] = len(paths)

        # Getting the badness values:
        true_badness_sum = 0  # sum of badness values with lengths removed. Note: only relecant for when settings not neutral

        stoplights_list = []
        steps_list = []

        stoplight_counter = 0
        steps_counter = 0
        pavement_types_list = []

        for i in range(len(paths)):
            path = paths[i]
            # gathering additional info:
            stoplight_data = nx.get_edge_attributes(G.subgraph(path), "stoplights")
            stoplights_list=stoplights_list+attribute_collector(G, path, stoplight_data)
            step_data = nx.get_edge_attributes(G.subgraph(path), "steps")
            steps_list= steps_list+attribute_collector(G, path, step_data)
            pavement_data = nx.get_edge_attributes(G.subgraph(path), "surface")
            pavement_types_list = pavement_types_list+attribute_collector(G, path, pavement_data)
            # print("stoplights_list list")
            # print(stoplights_list)

            if pavement_pref != "Neutral" or stoplight_pref != "Neutral" or steps_pref != "Neutral":
                lengths_data = nx.get_edge_attributes(G.subgraph(path), "length")
                path_length = length(G, path, lengths_data)
                true_badness = badness[i] - path_length
                true_badness_sum += true_badness

        if len(paths) > 0:
            results[coordinate]["Average paths badness"] = true_badness_sum / len(paths)
            results[coordinate]["Avg. number of stoplights"] = sum(stoplights_list) / len(paths)
            results[coordinate]["Avg. number of steps"] = sum(steps_list) / len(paths)
            results[coordinate]["Avg. number of paved edges"] = pavement_types_list.count("paved") / len(paths)
            results[coordinate]["Avg. number of unpaved edges"] = pavement_types_list.count("unpaved") / len(paths)
            results[coordinate]["Avg. number of edges with unknown surface"] = (len(pavement_types_list) - pavement_types_list.count(
                                                                                     "paved") - pavement_types_list.count(
                                                                                     "unpaved")) / len(paths)
        else:
            results[coordinate]["Average paths badness"] = 0
            results[coordinate]["Avg. number of stoplights"] = 0
            results[coordinate]["Avg. number of steps"] = 0
            results[coordinate]["Avg. number of paved edges"] = 0
            results[coordinate]["Avg. number of unpaved edges"] = 0
            results[coordinate]["Avg. number of edges with unknown surface"] = 0

        print(dashes)
        pprint.pprint(results)
    return results

def generate_random_coordinates(number, seed, G):
    """
    Generates a list of random coordinate tuples from the given graph
    :param number: number of tuples to generate
    :param seed: seed
    :param G: graph to be processed
    :return: list of tuples
    """

    random.seed(seed)
    random_nodes = random.sample(list(G.nodes), number)
    G_sample = G.subgraph(random_nodes)
    nodes, data = zip(*G_sample.nodes(data=True))  # getting the data about the nodes

    # Getting the coords that we will test
    coords = [(float(d['x']), float(d['y'])) for d in data]
    # we need the float() here ^ cuz we get np.float as a return, usage ofwhich is discouraged from what i undestand
    return coords






def run_evaluation(distances, graph_filepath, coordinates_list, alpha, simplification_param):
    for distance in distances:
        name_distance = "overall_" + str(distance)
        state = "neutral"
        name_state = name_distance + "_"+state
        results_neutral = overall_evaluation("Neutral","Neutral", "Neutral", graph_filepath, distance, coordinates_list, alpha, simplification_param)
        saving_intermediate(results_neutral, name_state, "intermediate_" + name_distance)

        state = "avoid"
        name_state = name_distance + "_"+ state
        results_avoid = overall_evaluation("Neutral","Avoid", "Avoid", graph_filepath, distance, coordinates_list, alpha, simplification_param)
        saving_intermediate(results_avoid, name_state, "intermediate_" + name_distance)

        state = "prefer"
        name_state = name_distance + state
        results_prefer = overall_evaluation("Neutral","Prefer","Prefer", graph_filepath, distance, coordinates_list, alpha, simplification_param)  # skews data a lot due to rarity of stoplights and steps
        saving_intermediate(results_prefer, name_state, "intermediate_" + name_distance)

        state = "paved"
        name_state = name_distance + "_"+ state
        results_paved = overall_evaluation("Paved","Neutral", "Neutral", graph_filepath, distance, coordinates_list, alpha, simplification_param)
        saving_intermediate(results_paved, name_state, "intermediate_" + name_distance)

        processing_overall(results_neutral, results_avoid,results_prefer, results_paved, name_distance)


# Settings
distances = [2000, 5000, 20000]
coordinates = generate_random_coordinates(20,11111,load_graph(graph_filepath))
alpha = 0.85
node_closeness = 65
if __name__ == "__main__": # so it doesnt run on import
    run_evaluation(distances, graph_filepath, coordinates, alpha, node_closeness)