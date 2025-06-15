import os

import numpy as np
import pandas as pd
from IPython.core.display_functions import display


base_dir = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/evaluation/results/overall_results_intermediate/intermediate_"

results_folders = os.listdir(base_dir)
print(results_folders)

variance_data_time = pd.DataFrame(columns = ['Distance', 'State','Var', 'Sd', 'Mean', 'CV']) # CV is for coefficient of variation
variance_data_nPaths = pd.DataFrame(columns = ['Distance', 'State','Var', 'Sd', 'Mean', 'CV']) # CV is for coefficient of variation

for folder in results_folders:
    current_folder = os.path.join(base_dir, folder)
    numerical_distance = folder.split('_')[1]
    print(numerical_distance)
    files = os.listdir(os.path.join(current_folder))
    for file in files:
        setting_mode = (file.split('.')[0]).split('_')[2]
        current_file_dir = os.path.join(current_folder, file)

        # row that we will append later:
        row_time = {'Distance':numerical_distance, 'State':setting_mode,'Var':0, 'Sd':0, 'Mean':0, 'CV':0}
        row_paths = {'Distance':numerical_distance, 'State':setting_mode,'Var':0, 'Sd':0, 'Mean':0, 'CV':0}
        #
        # # processing the data for time:
        # df = pd.read_csv(current_file_dir, index_col=0)
        # row_time['Var'] = df.loc['Elapsed time'].var()
        # row_time['Sd'] = df.loc['Elapsed time'].std()
        # row_time['Mean'] = df.loc['Elapsed time'].mean()
        # row_time['CV'] = row_time['Sd']/row_time['Mean']
        #
        # variance_data_time = pd.concat([variance_data_time, pd.DataFrame([row_time])], ignore_index=True)

        # df = pd.read_csv(current_file_dir, index_col=0).T
        #
        # row_paths['Var'] = df['Number of paths'].var()
        # row_paths['Sd'] = df['Number of paths'].std()
        # row_paths['Mean'] = df['Number of paths'].mean()
        # row_paths['CV'] = row_paths['Sd'] / row_paths['Mean'] if row_paths['Mean'] != 0 else None

        # # now for number of paths
        # row_paths['Var'] = df.loc['Number of paths'].var()
        # row_paths['Sd'] = df.loc['Number of paths'].std()
        # row_paths['Mean'] = df.loc['Number of paths'].mean()
        # row_paths['CV'] = row_paths['Sd'] / row_paths['Mean']
        #
        # variance_data_nPaths = pd.concat([variance_data_nPaths, pd.DataFrame([row_paths])], ignore_index=True)

        # Read and transpose the DataFrame
        df = pd.read_csv(current_file_dir, index_col=0).T

        values = df['Number of paths'].dropna()
        success_values = values[values > 0]

        row = {
            'Distance': numerical_distance,
            'State': setting_mode,
            'Var': values.var(),
            'Sd': values.std(),
            'Mean': values.mean(),
            'CV': values.std() / values.mean() if values.mean() != 0 else None,
            'Success Mean': success_values.mean() if not success_values.empty else None,
            'Success CV': success_values.std() / success_values.mean() if not success_values.empty and success_values.mean() != 0 else None,
            'Failure Rate': (values == 0).sum() / len(values) if len(values) > 0 else None
        }

        variance_data_nPaths = pd.concat([variance_data_nPaths, pd.DataFrame([row])], ignore_index=True)

variance_data_nPaths.sort_values(by=['Distance', 'State'], inplace=True)
variance_data_nPaths.reset_index(drop=True, inplace=True)

variance_data_time.sort_values(by=['Distance', 'State'], inplace=True)
variance_data_time.reset_index(drop=True, inplace=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print('elapsed time:')
display(variance_data_time)

print('number of paths:')
display(variance_data_nPaths)