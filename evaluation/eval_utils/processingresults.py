import os

import pandas as pd

def processing_smoothing_and_simplifying_results (neutral, avoid, preferred,paved, name):

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

    print("Number of paths results:")
    print(path_number.to_string())

    # Badness:
    badness = pd.DataFrame({
        "Avoid": avoid.loc["Average paths badness"],
        # "Preferred": preferred.loc["Average paths badness"],
        "Paved": paved.loc["Average paths badness"]
    })

    print("Badness results:")
    print(badness.to_string())

    # Making CSVs:
    os.makedirs(name, exist_ok=True)
    neutral.to_csv(os.path.join(name, "neutral.csv"))
    avoid.to_csv(os.path.join(name, "avoid.csv"))
    preferred.to_csv(os.path.join(name, "preferred.csv"))
    paved.to_csv(os.path.join(name, "paved.csv"))
    elapsed_time.to_csv(os.path.join(name, "elapsed_time.csv"))
    path_number.to_csv(os.path.join(name, "path_number.csv"))
    badness.to_csv(os.path.join(name, "badness.csv"))


def loading_full_results(results_neutral, results_avoid, results_prefer, results_paved, name):
    """
    Facilitates loading full results when everything went smoothly and no necessity for loading partial resuls from csv has arisen.
    Used for smoothing and simplifying evaluation. Passes the results onto the procesing pipeline.
    """

    neutral = pd.DataFrame.from_dict(results_neutral)
    avoid = pd.DataFrame.from_dict(results_avoid)
    preferred = pd.DataFrame.from_dict(results_prefer)
    paved = pd.DataFrame.from_dict(results_paved)
    processing_smoothing_and_simplifying_results(neutral, avoid, preferred, paved, name)


def loading_csv_results(file_path_neutral, file_path_avoid, file_path_prefer, file_path_paved, name):
    """
    Used for smoothing and simplifying result processing in case that raw results have to be loaded from csv files.
    """
    neutral = pd.read_csv(file_path_neutral, index_col=0)
    avoid = pd.read_csv(file_path_avoid, index_col=0)
    preferred = pd.read_csv(file_path_prefer, index_col=0)
    paved = pd.read_csv(file_path_paved, index_col=0)

    processing_smoothing_and_simplifying_results(neutral, avoid, preferred, paved, name)    


def dash_printer(text):
    dashes = "".join(["-"] * 200)
    print("\n\n",dashes)
    print(text)
    print("\n\n",dashes)

def saving_intermediate(result,name, savedir):
    os.makedirs(savedir, exist_ok=True)
    result = pd.DataFrame.from_dict(result)
    result.to_csv(os.path.join(savedir, name + ".csv"))

def individual_overall_results(result, neutral=False):
    means = pd.DataFrame({
        "Elapsed time": [result.loc["Elapsed time"].mean()],
        "N Paths": [result.loc["Number of paths"].mean()],
        "N stoplights": [result.loc["Avg. number of stoplights"].mean()],
        "N steps": [result.loc["Avg. number of steps"].mean()],
        "N paved edges": [result.loc["Avg. number of paved edges"].mean()],
        "N unpaved edges": [result.loc["Avg. number of unpaved edges"].mean()],
        "N unknown edge surfaces": [result.loc["Avg. number of edges with unknown surface"].mean()]
    })

    if not neutral:
        means["Path badness"] = result.loc["Average paths badness"].mean()

    no_paths = (result.loc["Number of paths"] == 0).sum() / result.shape[1] # number of 0s divided by columns because of result shape
    return means, no_paths

def processing_overall(results_neutral, results_avoid,results_prefer, results_paved, name_distance, dir):
    """
    Processes the results from the overall evaluation function into several csv files that contain the following information:
    - means for each setting state
    - number of failures per state
    - differences in number of stoplight and steps betweene the following combinations: "neutral & avoid" and "prefer & avoid"
    """


    # Loading in here because I don't want to mess up that pipeline:
    neutral = pd.DataFrame.from_dict(results_neutral)
    prefer = pd.DataFrame.from_dict(results_prefer)
    avoid = pd.DataFrame.from_dict(results_avoid)
    paved = pd.DataFrame.from_dict(results_paved)

    # Making the save dir:
    os.makedirs(name_distance, exist_ok=True)

    # Computing individual stats:
    means_neutral, no_paths_neutral = individual_overall_results(neutral, True)
    means_neutral.to_csv(os.path.join(name_distance, "means_neutral.csv"))

    means_avoid, no_paths_avoid = individual_overall_results(avoid)
    means_avoid.to_csv(os.path.join(name_distance, "means_avoid.csv"))

    means_prefer, no_paths_prefer = individual_overall_results(prefer)
    means_prefer.to_csv(os.path.join(name_distance, "means_prefer.csv"))

    means_paved, no_paths_paved = individual_overall_results(paved)
    means_paved.to_csv(os.path.join(name_distance, "means_paved.csv"))

    # How many failed to get paths
    failed = pd.DataFrame({
        "Neutral": [no_paths_neutral],
        "Avoid": [no_paths_avoid],
        "Prefer":[no_paths_prefer],
        "Paved": [no_paths_paved]
    })

    failed.to_csv(os.path.join(name_distance, "failed.csv"))

    # And counting the difference between neutral and avoid

    pref_diff_neutral_avoid = pd.DataFrame({
        "stoplights_diff": [means_neutral["N stoplights"].iloc[0] - means_avoid["N stoplights"].iloc[0]],
        "steps_diff": [means_neutral["N steps"].iloc[0] - means_avoid["N steps"].iloc[0]]
    })

    pref_diff_neutral_avoid.to_csv(os.path.join(name_distance, "pref_diff_neutral_avoid.csv"))

    pref_diff_prefer_avoid = pd.DataFrame({
        "stoplights_diff": [means_prefer["N stoplights"].iloc[0] - means_avoid["N stoplights"].iloc[0]],
        "steps_diff": [means_prefer["N steps"].iloc[0] - means_avoid["N steps"].iloc[0]]
    })

    pref_diff_prefer_avoid.to_csv(os.path.join(name_distance, "pref_diff_prefer_avoid.csv"))









