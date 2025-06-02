import pickle
import time

import networkx as nx

from main import main
from utils.length import length
from evaluation.eval_utils.processingresults import saving_intermediate, loading_csv_results
from evaluation.eval_utils.processingresults import dash_printer

"""
To do:
- analyze 10000
- analyze 15000
- reanalyze 5000

"""


def preferenced_smoothing_eval(distance, smoothing_increase, pavement_pref, stoplight_pref, steps_pref):

    smoothing_factor = 0.5
    results = {}
    starting_point = (16.3725042, 48.2083537)  # Historical center of Vienna - Stephansdom. Chosen due to a dense street network
    while smoothing_factor <= 1.01: # 1.1 because computational rounding error

        if smoothing_factor > 1:
            smoothing_factor = 1 # to fix the rounding error thing
        # For clarity when analyzing:
        dashes = "".join(["-"] * 200)
        print(dashes)
        print("Analyzing smoothing factor ", smoothing_factor, "For preferences:", pavement_pref, stoplight_pref, steps_pref )
        print(dashes)

        # Preference dict that's dependent on the function call:
        preference_dict = {"total_length": distance, "elevation_requested": 0, "elevation_error": 10000, # high elevation error because it's not the point of the test
                           "pavement_preferences": pavement_pref,
                           "stoplights_preference": stoplight_pref, "steps_preference": steps_pref, "sharing_allowance": 0.3,
                           "node_simplification_status": "False", "allowed_distance_between_nodes": 25,
                           "stoplight_penalty_strength": 1.1, "steps_penalty_strength": 1.2,
                           "pavement_penalty_strength": 1.05, "error": 60,
                           "alpha": smoothing_factor}

        # Loading the graph:
        graph_filepath = "/home/h12227338/LoopBuddy/preloadedmap/Wien.pkl"
        # graph_filepath = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/preloadedmap/Wien.pkl"

        # Normal execution:
        print("\nLoading the graph!\n")
        with open(graph_filepath, "rb") as f:
            G = pickle.load(f)
        print("Graph loaded succesfully!\n")
        print(f"Graph has {len(G.nodes)} nodes and {len(G.edges)} edges.")

        start_time = time.time()  # we need to measure time, as it's important for the user exprience

        paths, _, badness = main(starting_point, preference_dict,G)  # we don't need elevation error in this case, as elevation is not considered

        end_time = time.time()
        elapsed_time = end_time - start_time
        results[smoothing_factor] = {}

        results[smoothing_factor]["Elapsed time"] = elapsed_time
        results[smoothing_factor]["Number of paths"] = len(paths)

        # Here this function deviates from the one above:
        if pavement_pref != "Neutral" or stoplight_pref != "Neutral" or steps_pref != "Neutral":

            # Getting the badness values:
            true_badness_sum = 0  # sum of badness values with lengths removed

            for i in range(len(paths)): # only relevant for when preferences are in place otherwise weighted length = length
                path = paths[i]
                lengths_data = nx.get_edge_attributes(G.subgraph(path), "length")
                path_length = length(G, path, lengths_data)

                print(path_length)


                true_badness = badness[i]-path_length
                true_badness_sum+=true_badness

            if len(paths)>0:
                results[smoothing_factor]["Average paths badness"] = true_badness_sum/len(paths)
            else:
                results[smoothing_factor]["Average paths badness"] = 0

        smoothing_factor = smoothing_factor + smoothing_increase
        print(dashes)

    return results



# dash_printer("*****************************************Analyzing 5k!*****************************************")
# distance = 5000
# smoothing_increase = 0.05
# results_neutral5k = preferenced_smoothing_eval(distance, smoothing_increase, "Neutral", "Neutral", "Neutral")
# results_avoid5k = preferenced_smoothing_eval(distance,smoothing_increase, "Neutral", "Avoid", "Avoid")
# results_prefer5k = preferenced_smoothing_eval(distance,smoothing_increase,"Neutral", "Prefer", "Prefer") # skews data a lot due to rarity of stoplights and steps
# results_paved5k = preferenced_smoothing_eval(distance,smoothing_increase,"Paved", "Neutral", "Neutral")
#
# dash_printer("*****************************************Results 5k!*****************************************")
# name = "5ksmoothing005"
# processing_smoothing_and_simplification_eval(results_neutral5k, results_avoid5k, results_prefer5k, results_paved5k, name)
#
#
# dash_printer("*****************************************Analyzing 10k!*****************************************")
# distance = 10000
# smoothing_increase = 0.05
#
# results_neutral10k = preferenced_smoothing_eval(distance, smoothing_increase, "Neutral", "Neutral", "Neutral")
# saving_intermediate(results_neutral10k, "neutral_10k", "intermediate_10k")
#
# results_avoid10k = preferenced_smoothing_eval(distance,smoothing_increase, "Neutral", "Avoid", "Avoid")
# saving_intermediate(results_neutral10k, "avoid_10k", "intermediate_10k")
#
# results_prefer10k = preferenced_smoothing_eval(distance,smoothing_increase,"Neutral", "Prefer", "Prefer") # skews data a lot due to rarity of stoplights and steps
# saving_intermediate(results_prefer10k, "prefer_10k", "intermediate_10k")
#
#
# results_paved10k = preferenced_smoothing_eval(distance,smoothing_increase,"Paved", "Neutral", "Neutral")
# saving_intermediate(results_prefer10k, "paved_10k", "intermediate_10k")
#
#
# dash_printer("*****************************************Results 10k!*****************************************")
# name = "10ksmoothing005"
# processing_smoothing_and_simplification_eval(results_neutral10k, results_avoid10k, results_prefer10k, results_paved10k,name)
#
# dash_printer("*****************************************Analyzing 15k!*****************************************")
distance = 15000
smoothing_increase = 0.05
# # results_neutral15k = preferenced_smoothing_eval(distance, smoothing_increase, "Neutral", "Neutral", "Neutral")
# # saving_intermediate(results_neutral15k, "neutral_15k", "intermediate_15k")
# #
# # results_avoid15k = preferenced_smoothing_eval(distance,smoothing_increase, "Neutral", "Avoid", "Avoid")
# # saving_intermediate(results_avoid15k, "avoid_15k", "intermediate_15k")
# #
# results_prefer15k = preferenced_smoothing_eval(distance,smoothing_increase,"Neutral", "Prefer", "Prefer") # skews data a lot due to rarity of stoplights and steps
# saving_intermediate(results_prefer15k, "prefer_15k", "intermediate_15k")
#
results_paved15k = preferenced_smoothing_eval(distance,smoothing_increase,"Paved", "Neutral", "Neutral")
saving_intermediate(results_paved15k, "paved_15k", "intermediate_15k")


dash_printer("*****************************************Results 15k!*****************************************")

file_path_neutral = "/home/h12227338/LoopBuddy/intermediate_15k/neutral_15k.csv"
file_path_avoid = "/home/h12227338/LoopBuddy/intermediate_15k/avoid_15k.csv"
file_path_prefer = "/home/h12227338/LoopBuddy/intermediate_15k/prefer_15k.csv"
file_path_paved = "/home/h12227338/LoopBuddy/intermediate_15k/paved_15k.csv"

# file_path_avoid = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/intermediate_15k/avoid_15k.csv"
# file_path_neutral = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/intermediate_15k/neutral_15k.csv"
# file_path_paved = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/intermediate_15k/paved_15k.csv"
# file_path_prefer = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/intermediate_15k/prefer_15k.csv"

# # reading in the files that were completed:
# with open(file_path_neutral, mode='r', encoding='utf-8') as file:
#     reader = csv.DictReader(file)
#     results_neutral15k = list(reader)
#
#
# with open(file_path_avoid, mode='r', encoding='utf-8') as file:
#     reader = csv.DictReader(file)
#     results_avoid15k = list(reader)
# #
# #
# neutral = pd.DataFrame.from_dict(results_neutral15k)
# # avoid = pd.DataFrame.from_dict(results_avoid15k)
#

#
# neutral = pandas.read_csv(file_path_neutral)

#
# # Printing:
# print("Neutral results:")
# print(neutral.to_string())
# print("\n\n")
#
# print("Avoiding steps and stoplights results:")
# print(avoid.to_string())
# print("\n\n")
#
# #
name = "15ksmoothing005"
# loading_full_results(results_neutral15k, results_avoid15k, results_prefer15k, results_paved15k, name)
#
loading_csv_results(file_path_neutral,file_path_avoid,file_path_prefer,file_path_paved,name)