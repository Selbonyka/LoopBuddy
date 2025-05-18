import os

import pandas as pd

#  Data processing:
def processing_smoothing_and_simplification_eval(results_neutral, results_avoid, results_prefer, results_paved, name):



    neutral = pd.DataFrame.from_dict(results_neutral)
    neutral.set_index(neutral.columns[0], inplace=True) # for reading in existing files
    avoid = pd.DataFrame.from_dict(results_avoid)
    avoid.set_index(avoid.columns[0], inplace=True)  # for reading in existing files
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

    print("Number of paths results:")
    print(path_number.to_string())

    # Badness

    badness = pd.DataFrame({
        "Avoid": avoid.loc["Average paths badness"],
        # "Preferred": preferred.loc["Average paths badness"],
        "Paved": paved.loc["Average paths badness"]
    })

    print("Badness results:")
    print(badness.to_string())

    os.makedirs(name, exist_ok=True)
    neutral.to_csv(os.path.join(name, "neutral.csv"))
    avoid.to_csv(os.path.join(name, "avoid.csv"))
    preferred.to_csv(os.path.join(name, "preferred.csv"))
    paved.to_csv(os.path.join(name, "paved.csv"))
    elapsed_time.to_csv(os.path.join(name, "elapsed_time.csv"))
    path_number.to_csv(os.path.join(name, "path_number.csv"))
    badness.to_csv(os.path.join(name, "badness.csv"))




def dash_printer(text):
    dashes = "".join(["-"] * 200)
    print("\n\n",dashes)
    print(text)
    print("\n\n",dashes)

def saving_intermediate(result,name, savedir):
    os.makedirs(savedir, exist_ok=True)
    result = pd.DataFrame.from_dict(result)
    result.to_csv(os.path.join(savedir, name + ".csv"))
