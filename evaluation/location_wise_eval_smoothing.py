import os

from evaluation.eval_utils.eval_utils import generate_random_coordinates
from evaluation.eval_utils.overall_eval_functions import run_overall_evaluation, load_graph


def run_smoothing_eval(distances, graph_filepath, coordinates_list, alphalist, simplification_param, dir):
    for a in alpha:
        current_dir = os.path.join(dir, str(a*100))#multiplying by 100 just to make it more computer friendy
        run_overall_evaluation(distances, graph_filepath, coordinates_list, a, simplification_param, current_dir)


graph_filepath = "/home/h12227338/LoopBuddy/preloadedmap/Wien.pkl"
# alpha = range(50, 95,10)
# alpha = [x/100 for x in alpha]
distances = [2000,15000]
alpha = [85/100]
smoothing_dir = "smoothing_results"
nodes, coordinates = generate_random_coordinates(20,11111,load_graph(graph_filepath))
smoothing_param = 0
print(alpha)

if __name__ == "__main__": # so it doesnt run on import
    run_smoothing_eval(distances, graph_filepath, coordinates, alpha, smoothing_param, smoothing_dir)