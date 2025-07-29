
from evaluation.eval_utils.eval_utils import generate_random_coordinates
from evaluation.eval_utils.overall_eval_functions import run_overall_evaluation, load_graph

""" 
Ok so what do we evaluate:
- Speed/badness/number of routes for diff diff preferences
- Number of stoplights
- Number of steps
- Number of pavement types
"""
# graph_filepath = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/preloadedmap/Wien.pkl"
graph_filepath = "/home/h12227338/LoopBuddy/preloadedmap/Wien.pkl"

# Settings
distances = [2000,15000]
nodes, coordinates = generate_random_coordinates(100,12345,load_graph(graph_filepath)) # changed the seed to get other data
alpha = 0.85
node_closeness = 40
overall_dir = "overall_results_no_sharing_limit"
if __name__ == "__main__": # so it doesnt run on import
    run_overall_evaluation(distances, graph_filepath, coordinates, alpha,node_closeness, overall_dir)