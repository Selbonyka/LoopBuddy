
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from IPython.core.display_functions import display


result_dir = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/evaluation/results/smoothing_results"

factor_folders = os.listdir(result_dir) # getting the upper layer of results

print(os.listdir(result_dir))


column_names = ['State', 'Alpha', 'N paths', 'Time','Badness', 'Stoplights', 'Steps', 'Paved', 'Unpaved', 'Unknown', 'Failed']

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
            current_file_dir = os.path.join(files_dir, file)

            # creating a row that we will later append
            row = {'State': setting_mode, 'Alpha': float(factor) / 100, 'N paths': 0, 'Time': 0,'Badness':0,
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


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

averaged_results = {} # just stuck with the dict format for some reason
combined_averaged_df = []

# Creating the average values dfs (i did create the dict one first but then also createn one with a list to export to csv easier)

for key in distance_dfs:

    distance_dfs[key].sort_values(by=['Alpha', 'State'], inplace=True)
    distance_dfs[key].reset_index(drop=True, inplace=True)
    print("\n\n\n\n")
    print(key)
    display(distance_dfs[key])

    ## Adding the average values:
    averaged_df = distance_dfs[key]
    averaged_df.drop(columns = ['State'], inplace = True)
    averaged_df = averaged_df.groupby(by=['Alpha']).mean()

    averaged_results[key] = averaged_df

    # Creating a list of dfs so we can then concatenate it into one with avg values:
    averaged_df_with_dist = averaged_df.copy()
    averaged_df_with_dist['Distance'] = int(key)
    combined_averaged_df.append(averaged_df_with_dist.reset_index())

# Just displaying the avg values
for key in averaged_results:
    print("\n\n\n\n")
    print(key)
    display(averaged_results[key])


# Plot the values for each alpha for each dist separately:
all_factors = sorted(list(set().union(*[df.index for df in averaged_results.values()])))

x = np.arange(len(all_factors))  # numeric x positions for factors
bar_width = 0.15

plt.figure(figsize=(12, 6), dpi = 300)
ax1 = plt.gca()
ax2 = ax1.twinx()

colors = plt.cm.viridis(np.linspace(0, 1, len(averaged_results)))

for i, (distance, df) in enumerate(averaged_results.items()):
    df = df.reindex(all_factors)

    line = ax1.plot(x, df['N paths'], label=f'$n_P$: {distance}m', color=colors[i], marker='o')
    for xi, yi in zip(x, df['N paths']):
        ax1.annotate(f'{yi:.1f}', (xi, yi), textcoords="offset points", xytext=(0, 4), ha='center', fontsize=8)

    offset = (i - len(averaged_results) / 2) * bar_width
    bars = ax2.bar(x + offset, df['Time'], width=bar_width, alpha=0.5, label=f'$T$: {distance}', color=colors[i])

    # ax1.plot(x, df['N paths'], label=f' $n_P$: {distance}m', color=colors[i], marker='o')
    #
    # offset = (i - len(averaged_results) / 2) * bar_width
    # ax2.bar(x + offset, df['Time'], width=bar_width, alpha=0.5, label=f'$T$: {distance}m', color=colors[i])

ax1.set_xticks(x)
ax1.set_xticklabels(all_factors, rotation=45)
ax1.set_xlabel('$\\alpha$')
ax1.set_ylabel('Number of paths - $n_P$')
ax2.set_ylabel('Time - $T$ (s)')

plt.title('$n_P$ (line) and $T$ (bar) per $\\alpha$ and $d$')
lines_labels, lines_handles = ax1.get_legend_handles_labels()
bars_labels, bars_handles = ax2.get_legend_handles_labels()
plt.legend(lines_labels + bars_labels, lines_handles + bars_handles, loc='upper left')


plt.tight_layout()
plt.grid(True, axis='y', linestyle='--', alpha=0.4)
plt.show()


final_combined_df = pd.concat(combined_averaged_df, ignore_index=True)
display(final_combined_df)


# Let's add some averaging over the distance as well:
factor_avg = final_combined_df.groupby('Alpha')[['N paths', 'Time']].mean().reset_index()

x = np.arange(len(factor_avg['Alpha']))

fig, ax1 = plt.subplots(figsize=(10, 6), dpi = 300)

# Number of paths:
ax1.plot(x, factor_avg['N paths'], color='#00008B', marker='o', label='Avg. N paths')
for xi, yi in zip(x, factor_avg['N paths']):
    ax1.annotate(f'{yi:.1f}', (xi, yi), textcoords="offset points", xytext=(0, 12),
                 ha='center', va='top', fontsize=8)
ax1.set_ylabel('Number of paths - $n_P$')
ax1.tick_params(axis='y')

# Time:
ax2 = ax1.twinx()
ax2.bar(x, factor_avg['Time'], alpha=0.5, color='tab:green', label='Avg. Time', width=0.4)
ax2.set_ylabel('Time - $T$ (s)')
ax1.set_xlabel('$\\alpha$')
ax2.tick_params(axis='y')
ax1.grid(True, axis='y', linestyle='--', alpha=0.4)  # <- Enable grid with same style


# Plot:
# plt.grid(True, axis='x', linestyle='--', alpha=0.4)
plt.xticks(x, factor_avg['Alpha'], rotation=45)
plt.title('Avg. $n_P$ (line) and $T$ (bar) per $\\alpha$')
fig.tight_layout()
plt.show()
