# just a second file to parallelize this
from evaluation.overall_eval import run_overall_evaluation, graph_filepath, coordinates, alpha, node_closeness, \
    overall_dir

distances =  [5000, 10000]

run_overall_evaluation(distances, graph_filepath, coordinates, alpha, node_closeness,overall_dir)