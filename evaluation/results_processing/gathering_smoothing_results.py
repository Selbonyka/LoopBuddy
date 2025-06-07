
import pandas as pd
import numpy as np
import os

distances = [2000,5000,10000,15000]#distance analyzed

result_dir = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/evaluation/results/smoothing_results"

factor_folders = os.listdir(result_dir) # getting the upper layer of results
print(os.listdir(result_dir))

# Creating the data frames for each of the distances:
column_names = ['State', 'Factor', 'N paths', 'Time','Badness', 'Stoplights', 'Steps', 'Paved', 'Unpaved', 'Unknown', 'Failed']
# all_2000 = pd.DataFrame(columns= column_names)
# all_5000 = pd.DataFrame(columns= column_names)
# all_10000 = pd.DataFrame(columns= column_names)
# all_15000 = pd.DataFrame(columns= column_names)

distance_dfs = {
    '2000': pd.DataFrame(columns=column_names),
    '5000': pd.DataFrame(columns=column_names),
    '10000': pd.DataFrame(columns=column_names),
    '15000': pd.DataFrame(columns=column_names),
}

for factor in factor_folders: # list the factor folders
    current_factor_dir = os.path.join(os.path.join(result_dir, factor),'intermediate_') # the intermediate thing is cuz i messed up when creating oops

    distances_folders = os.listdir(current_factor_dir)

    for dist in distances_folders: #now list the distance folders
        numerical_distance = dist.split('_')[1]

        files = os.listdir(os.path.join(current_factor_dir, dist))
        files_dir = os.path.join(current_factor_dir, dist)
        for file in files: # now we get to individual files
            setting_mode = (file.split('.')[0]).split('_')[2]
            print(factor,numerical_distance , setting_mode)
            current_file_dir = os.path.join(files_dir, file)

            # creating a row that we will later append
            row = {'State': setting_mode, 'Factor': factor, 'N paths': 0, 'Time': 0,'Badness':0,
                   'Stoplights': 0, 'Steps': 0, 'Paved': 0, 'Unpaved': 0, 'Unknown': 0, 'Failed': 0}

            # processing the data
            df = pd.read_csv(current_file_dir, index_col=0)
            row['Time'] = df.loc['Elapsed time'].mean()
            row['N paths'] = df.loc['Number of paths'].mean()
            row['Badness'] = df.loc['Average paths badness'].mean()
            row['Stoplights'] = df.loc['Avg. number of stoplights'].mean()
            row['Steps'] = df.loc['Avg. number of steps'].mean()
            row['Paved'] = df.loc['Avg. number of paved edges'].mean()
            row['Unpaved'] = df.loc['Avg. number of unpaved edges'].mean()
            row['Unknown'] = df.loc['Avg. number of edges with unknown surface'].mean()
            row['Failed'] = (df.loc['Number of paths']==0).sum()

            ## Adding it to the df:
            distance_dfs[numerical_distance] = pd.concat(
                [distance_dfs[numerical_distance], pd.DataFrame([row])],
                ignore_index=True
            )





print(distance_dfs["2000"])










