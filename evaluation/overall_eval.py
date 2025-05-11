import os
import pickle
import pprint
import time

import pandas as pd

import networkx as nx

from main import main
from utils.collect_attribute import attribute_collector
from utils.length import length
""" 

Ok so what do we evaluate:
- Speed/badness/number of routes for diff diff preferences
- Number of stoplights
- Number of steps
- Number of pavement types

Note: decide which simplification you are using and smoothing ;D

"""


# Setting up the evaluation:
def overall_evaluation(pavement_pref, stoplight_pref, steps_pref):

    distance = 0
    results = {}
    starting_point = (16.3725042, 48.2083537)  # Historical center of Vienna - Stephansdom. Chosen due to a dense street network
    # distance = 1000
    distances = [2000, 5000, 7000, 10000, 15000, 20000]

    for distance in distances: # just looping around the smoothing factor values, 1.1 because computational rounding error

        # For clarity when analyzing:
        dashes = "".join(["-"] * 200)
        print(dashes)
        print("Analyzing simplification distance :", distance, "\nMode:", pavement_pref, stoplight_pref, steps_pref)
        print(dashes)

        # Neutral settings
        preference_dict = {"total_length": distance, "elevation_requested": 0, "elevation_error": 1000,
                           "pavement_preferences": pavement_pref,
                           "stoplights_preference": stoplight_pref, "steps_preference": steps_pref, "sharing_allowance": 0.3,
                           "node_simplification_status": "True", "allowed_distance_between_nodes": 5,
                           "stoplight_penalty_strength": 1.1, "steps_penalty_strength": 1.2,
                           "pavement_penalty_strength": 1.05, "error": 60,
                           "alpha": 0.8}
        # Loading the graph:
        graph_filepath = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/preloadedmap/Wien.pkl"

        # Normal execution
        print("\nLoading the graph!\n")
        with open(graph_filepath, "rb") as f:
            G = pickle.load(f)
        print("Graph loaded succesfully!\n")
        start_time = time.time()  # we need to measure time, as it's important for the user exprience

        paths, _, badness = main(starting_point, preference_dict,G)  # we don't need elevation error in this case, as elevation is not considered

        end_time = time.time()
        elapsed_time = end_time - start_time

        results[distance] = {}
        results[distance]["Elapsed time"] = elapsed_time
        results[distance]["Number of paths"] = len(paths)

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
            print("stoplights_list list")
            print(stoplights_list)

            if pavement_pref != "Neutral" or stoplight_pref != "Neutral" or steps_pref != "Neutral":

                lengths_data = nx.get_edge_attributes(G.subgraph(path), "length")
                path_length = length(G, path, lengths_data)

                print(path_length)

                true_badness = badness[i] - path_length
                true_badness_sum += true_badness

        if len(paths) > 0:
            results[distance]["Average paths badness"] = true_badness_sum / len(paths)

            results[distance]["Avg. number of stoplights"] = sum(stoplights_list) / len(paths)
            results[distance]["Avg. number of steps"] = sum(steps_list) / len(paths)
            results[distance]["Avg. number of paved edges"] = pavement_types_list.count("paved") / len(paths)
            results[distance]["Avg. number of unpaved edges"] = pavement_types_list.count("unpaved") / len(paths)
            results[distance]["Avg. number of edges with unknown surface"] = (len(pavement_types_list) - pavement_types_list.count(
                                                                                     "paved") - pavement_types_list.count(
                                                                                     "unpaved")) / len(paths)


        else:
            results[distance]["Average paths badness"] = 0
            results[distance]["Avg. number of stoplights"] = 0
            results[distance]["Avg. number of steps"] = 0
            results[distance]["Avg. number of paved edges"] = 0
            results[distance]["Avg. number of unpaved edges"] = 0
            results[distance]["Avg. number of edges with unknown surface"] = 0

        # Processing the attributes:



        print(dashes)

        pprint.pprint(results)
    return results


results_neutral = overall_evaluation("Neutral", "Neutral", "Neutral")
results_avoid = overall_evaluation("Neutral", "Avoid", "Avoid")
results_prefer = overall_evaluation("Neutral", "Prefer", "Prefer") # skews data a lot due to rarity of stoplights and steps
results_paved = overall_evaluation("Paved", "Neutral", "Neutral")

# print("Neutral results:")
# pprint.pprint(results_neutral)
# print("Avoid results:")
# pprint.pprint(results_avoid)
# print("Preferred results:")
# pprint.pprint(results_prefer)
# print("Paved results:")
# pprint.pprint(results_paved)

#  Data processing:

neutral = pd.DataFrame.from_dict(results_neutral)
avoid = pd.DataFrame.from_dict(results_avoid)
preferred = pd.DataFrame.from_dict(results_prefer)
paved = pd.DataFrame.from_dict(results_paved)

# Printing:
print("Neutral results:")
print(neutral.to_string())
print("\n\n")

print("Avoiding steps and stoplights results:")
print(avoid.to_string())
print("\n\n")

print("Preferring steps and stoplights results:")
print(preferred.to_string())
print("\n\n")

print("Looking for paved surfaces results:")
print(paved.to_string())
print("\n\n")


# getting the average:

elapsed_time = pd.DataFrame({
    "Neutral": avoid.loc["Elapsed time"],
    "Avoid": avoid.loc["Elapsed time"],
    # "Preferred": preferred.loc["Elapsed time"], # skews data a lot
    "Paved": paved.loc["Elapsed time"]
})

elapsed_time['Mean'] = elapsed_time.mean(axis=1)
elapsed_time['Mean Change'] = elapsed_time[["Mean"]].diff()

print("Elapsed time results:")

print(elapsed_time.to_string())


# Number of paths analysis:

path_number = pd.DataFrame({
    "Neutral": avoid.loc["Number of paths"],
    "Avoid": avoid.loc["Number of paths"],
    # "Preferred": preferred.loc["Number of paths"], # skews data a low
    "Paved": paved.loc["Number of paths"]
})

path_number['Mean'] = path_number.mean(axis=1)
path_number['Mean Change'] = path_number[["Mean"]].diff()

print("\n Number of Paths:")
print(path_number.to_string())

# Badness

badness = pd.DataFrame({
    "Avoid": avoid.loc["Average paths badness"],
    # "Preferred": preferred.loc["Average paths badness"],
    "Paved": paved.loc["Average paths badness"]
})

print("\n Badness results:")
print(badness.to_string())

name = "overall_evaluation"

os.makedirs(name, exist_ok=True)
neutral.to_csv(os.path.join(name, "neutral.csv"))
avoid.to_csv(os.path.join(name, "avoid.csv"))
preferred.to_csv(os.path.join(name, "preferred.csv"))
paved.to_csv(os.path.join(name, "paved.csv"))
elapsed_time.to_csv(os.path.join(name, "elapsed_time.csv"))
path_number.to_csv(os.path.join(name, "path_number.csv"))
badness.to_csv(os.path.join(name, "badness.csv"))