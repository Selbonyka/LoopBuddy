import pickle
import pprint
import time

import networkx as nx

from evaluation.eval_utils.processingresults import dash_printer, loading_full_results, saving_intermediate
from main import main
from utils.length import length


# Setting up the evaluation:
def simplification_evaluation(distance, simplification_increase,max_simplification_dist, pavement_pref, stoplight_pref, steps_pref):

    simplification_dist = 50
    results = {}
    starting_point = (16.3725042, 48.2083537)  # Historical center of Vienna - Stephansdom. Chosen due to a dense street network

    while simplification_dist <= max_simplification_dist: # just looping around the smoothing factor values, 1.1 because computational rounding error
        dashes = "".join(["-"] * 200)
        print(dashes)
        print("Analyzing simplification distance :", simplification_dist, "\nMode:", pavement_pref, stoplight_pref, steps_pref)
        print(dashes)

        # Neutral settings
        preference_dict = {"total_length": distance, "elevation_requested": 0, "elevation_error": 10000,
                           "pavement_preferences": pavement_pref,
                           "stoplights_preference": stoplight_pref, "steps_preference": steps_pref, "sharing_allowance": 0.3,
                           "node_simplification_status": "True", "allowed_distance_between_nodes": simplification_dist,
                           "stoplight_penalty_strength": 1.1, "steps_penalty_strength": 1.2,
                           "pavement_penalty_strength": 1.05, "error": 60,
                           "alpha": 0.85}
        # Loading the graph:
        # graph_filepath = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/preloadedmap/Wien.pkl"
        graph_filepath = "/home/h12227338/LoopBuddy/preloadedmap/Wien.pkl"

        # Normal execution
        print("\nLoading the graph!\n")
        with open(graph_filepath, "rb") as f:
            G = pickle.load(f)
        print("Graph loaded succesfully!\n")

        start_time = time.time()  # we need to measure time, as it's important for the user exprience

        paths, _, badness = main(starting_point, preference_dict, G) # we don't need elevation error in this case, as elevation is not considered

        end_time = time.time()
        elapsed_time = end_time - start_time
        results[simplification_dist] = {}

        results[simplification_dist]["Elapsed time"] = elapsed_time
        results[simplification_dist]["Number of paths"] = len(paths)


        if pavement_pref != "Neutral" or stoplight_pref != "Neutral" or steps_pref != "Neutral":

            # Getting the badness values:
            true_badness_sum = 0  # sum of badness values with lengths removed

            for i in range(len(paths)):  # only relevant for when preferences are in place otherwise weighted length = length
                path = paths[i]
                lengths_data = nx.get_edge_attributes(G.subgraph(path), "length")
                path_length = length(G, path, lengths_data)

                print(path_length)

                true_badness = badness[i] - path_length
                true_badness_sum += true_badness

            if len(paths) > 0:
                results[simplification_dist]["Average paths badness"] = true_badness_sum / len(paths)
            else:
                results[simplification_dist]["Average paths badness"] = 0
        simplification_dist = simplification_dist + simplification_increase

        print(dashes)

        pprint.pprint(results)
    return results


# dash_printer("*****************************************Analyzing 5k!*****************************************")
distance = 5000
simplification_increase = 5
max_simplification_dist  = 200
name_distance = "5k_simplification_" + str(simplification_increase) + "_" + str(max_simplification_dist)

state = "neutral"
name_state= name_distance + state
results_neutral = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Neutral", "Neutral", "Neutral")
saving_intermediate(results_neutral, name_state, "intermediate_" + name_distance)

state = "avoid"
name_state= name_distance + state
results_avoid = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Neutral", "Avoid", "Avoid")
saving_intermediate(results_avoid, name_state, "intermediate_" + name_distance)

state = "prefer"
name_state= name_distance + state
results_prefer = simplification_evaluation(distance, simplification_increase,max_simplification_dist,"Neutral", "Prefer", "Prefer") # skews data a lot due to rarity of stoplights and steps
saving_intermediate(results_prefer, name_state, "intermediate_" + name_distance)

state = "paved"
name_state= name_distance + state
results_paved = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Paved", "Neutral", "Neutral")
saving_intermediate(results_paved, name_state, "intermediate_" + name_distance)

loading_full_results(results_neutral, results_avoid, results_prefer, results_paved, name_distance)


dash_printer("*****************************************Analyzing 10k!*****************************************")
distance = 10000
name_distance = "10k_simplification_" + str(simplification_increase) + "_" + str(max_simplification_dist)


state = "neutral"
name_state= name_distance + state
results_neutral = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Neutral", "Neutral", "Neutral")
saving_intermediate(results_neutral, name_state, "intermediate_" + name_distance)

state = "avoid"
name_state= name_distance + state
results_avoid = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Neutral", "Avoid", "Avoid")
saving_intermediate(results_avoid, name_state, "intermediate_" + name_distance)

state = "prefer"
name_state= name_distance + state
results_prefer = simplification_evaluation(distance, simplification_increase,max_simplification_dist,"Neutral", "Prefer", "Prefer") # skews data a lot due to rarity of stoplights and steps
saving_intermediate(results_prefer, name_state, "intermediate_" + name_distance)

state = "paved"
name_state= name_distance + state
results_paved = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Paved", "Neutral", "Neutral")
saving_intermediate(results_paved, name_state, "intermediate_" + name_distance)

loading_full_results(results_neutral, results_avoid, results_prefer, results_paved, name_distance)



# dash_printer("*****************************************Analyzing 15k!*****************************************")
# distance = 15000
# name_distance = "15k_simplification_" + str(simplification_increase) + "_" + str(max_simplification_dist)
#
#
# state = "neutral"
# name_state= name_distance + state
# results_neutral = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Neutral", "Neutral", "Neutral")
# saving_intermediate(results_neutral, name_state, "intermediate_" + name_distance)
#
# state = "avoid"
# name_state= name_distance + state
# results_avoid = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Neutral", "Avoid", "Avoid")
# saving_intermediate(results_avoid, name_state, "intermediate_" + name_distance)
#
# state = "prefer"
# name_state= name_distance + state
# results_prefer = simplification_evaluation(distance, simplification_increase,max_simplification_dist,"Neutral", "Prefer", "Prefer") # skews data a lot due to rarity of stoplights and steps
# saving_intermediate(results_prefer, name_state, "intermediate_" + name_distance)
#
#
# state = "paved"
# name_state= name_distance + state
# results_paved = simplification_evaluation(distance, simplification_increase,max_simplification_dist, "Paved", "Neutral", "Neutral")
# saving_intermediate(results_paved, name_state, "intermediate_" + name_distance)
#
# loading_full_results(results_neutral, results_avoid, results_prefer, results_paved, name_distance)


