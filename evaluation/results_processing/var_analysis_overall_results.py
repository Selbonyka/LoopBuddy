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

        # Read and transpose the DataFrame
        df = pd.read_csv(current_file_dir, index_col=0).T

        # Number of paths analysis
        values_np = df['Number of paths'].dropna()
        success_np = values_np[values_np > 0]

        row_paths = {
            'Distance': numerical_distance,
            'State': setting_mode,
            'Var': values_np.var(),
            'Sd': values_np.std(),
            'Mean': values_np.mean(),
            'CV': values_np.std() / values_np.mean() if values_np.mean() != 0 else None,
            'Success Mean': success_np.mean() if not success_np.empty else None,
            'Success CV': success_np.std() / success_np.mean() if not success_np.empty and success_np.mean() != 0 else None,
            'Failure Rate': (values_np == 0).sum() / len(values_np) if len(values_np) > 0 else None
        }
        variance_data_nPaths = pd.concat([variance_data_nPaths, pd.DataFrame([row_paths])], ignore_index=True)

        # Elapsed time analysis
        values_et = df['Elapsed time'].dropna()
        success_et = values_et[values_et > 0]

        row_time = {
            'Distance': numerical_distance,
            'State': setting_mode,
            'Var': values_et.var(),
            'Sd': values_et.std(),
            'Mean': values_et.mean(),
            'CV': values_et.std() / values_et.mean() if values_et.mean() != 0 else None,
            'Success Mean': success_et.mean() if not success_et.empty else None,
            'Success CV': success_et.std() / success_et.mean() if not success_et.empty and success_et.mean() != 0 else None,
            'Failure Rate': row_paths['Failure Rate']
        }
        variance_data_time = pd.concat([variance_data_time, pd.DataFrame([row_time])], ignore_index=True)


variance_data_nPaths['Distance'] = variance_data_nPaths['Distance'].astype(int)
variance_data_time['Distance'] = variance_data_time['Distance'].astype(int)

variance_data_nPaths.sort_values(by=['Distance', 'State'], inplace=True, ascending=True)
variance_data_nPaths.reset_index(drop=True, inplace=True)

variance_data_time.sort_values(by=['Distance', 'State'], inplace=True, ascending=True)
variance_data_time.reset_index(drop=True, inplace=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print('elapsed time:')
display(variance_data_time)

print('number of paths:')
display(variance_data_nPaths)

save_path = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/evaluation/results/variance_overall"

variance_data_nPaths.to_csv(save_path+'/Var_Num_Paths.csv', index=False)
variance_data_time.to_csv(save_path+'/Var_Elapsed_Time.csv', index=False)

