import pickle
import os
import pickle
import pprint
import time

import numpy as np

import networkx as nx
from evaluation.eval_utils.processingresults import saving_intermediate, processing_overall
from main import main
from utils.collect_attribute import attribute_collector
from utils.length import length

def load_graph(graph_filepath):
    print("\nLoading the graph!\n")
    with open(graph_filepath, "rb") as f:
        G = pickle.load(f)
    print("Graph loaded succesfully!\n")
    return G

def coordinate_wise_evaluation(pavement_pref, stoplight_pref, steps_pref, graph_filepath, distance, coordinates_list, alpha, simplfication_param):

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
                           "stoplights_preference": stoplight_pref, "steps_preference": steps_pref, "sharing_allowance": 1,
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
            # If no paths, all of the values should be set to NaN, so the means are calculated cleanly
            results[coordinate]["Average paths badness"] = np.nan
            results[coordinate]["Avg. number of stoplights"] = np.nan
            results[coordinate]["Avg. number of steps"] = np.nan
            results[coordinate]["Avg. number of paved edges"] = np.nan
            results[coordinate]["Avg. number of unpaved edges"] = np.nan
            results[coordinate]["Avg. number of edges with unknown surface"] = np.nan

        print(dashes)
        pprint.pprint(results)
    return results




def run_overall_evaluation(distances, graph_filepath, coordinates_list, alpha, simplification_param, dir):
    for distance in distances:
        name_distance = "overall_" + str(distance)
        state = "neutral"
        name_state = name_distance + "_"+state
        results_neutral = coordinate_wise_evaluation("Neutral", "Neutral", "Neutral", graph_filepath, distance,
                                                     coordinates_list, alpha, simplification_param)
        saving_intermediate(results_neutral, name_state, os.path.join(dir, os.path.join("intermediate_", name_distance))) # messed up here, but i didn't wanna re-run or change the whole structure when I caught it, so it made sense to keep it this way

        state = "avoid"
        name_state = name_distance + "_"+ state
        results_avoid = coordinate_wise_evaluation("Neutral", "Avoid", "Avoid", graph_filepath, distance,
                                                   coordinates_list, alpha, simplification_param)
        saving_intermediate(results_avoid, name_state, os.path.join(dir, os.path.join("intermediate_", name_distance)))

        state = "prefer"
        name_state = name_distance +"_"+ state
        results_prefer = coordinate_wise_evaluation("Neutral", "Prefer", "Prefer", graph_filepath, distance,
                                                    coordinates_list, alpha,
                                                    simplification_param)  # skews data a lot due to rarity of stoplights and steps
        saving_intermediate(results_prefer, name_state, os.path.join(dir, os.path.join("intermediate_", name_distance)))

        state = "paved"
        name_state = name_distance + "_"+ state
        results_paved = coordinate_wise_evaluation("Paved", "Neutral", "Neutral", graph_filepath, distance,
                                                   coordinates_list, alpha, simplification_param)
        saving_intermediate(results_paved, name_state, os.path.join(dir, os.path.join("intermediate_", name_distance)))

        processing_overall(results_neutral, results_avoid,results_prefer, results_paved, name_distance, dir)
