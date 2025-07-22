import os

from evaluation.eval_utils.eval_utils import generate_random_coordinates
from evaluation.eval_utils.overall_eval_functions import run_overall_evaluation, load_graph

def run_simplification_eval(distances, graph_filepath, coordinates_list, alpha, simplification_list, dir):
    for s in simplification_list:
        current_dir = os.path.join(dir, str(s))#multiplying by 100 just to make it more computer friendy
        run_overall_evaluation(distances, graph_filepath, coordinates_list, alpha, s, current_dir)

graph_filepath = "/home/h12227338/LoopBuddy/preloadedmap/Wien.pkl"

simplification_list = [150]
distances = [2000,15000]
alpha = 0.85
simplifications_dir = "simplification_results"
nodes, coordinates = generate_random_coordinates(20,11111,load_graph(graph_filepath))
smoothing_param = 0

if __name__ == "__main__": # so it doesnt run on import
    run_simplification_eval(distances, graph_filepath, coordinates, alpha, simplification_list, simplifications_dir)
