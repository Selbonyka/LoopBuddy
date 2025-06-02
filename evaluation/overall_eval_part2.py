# just a second file to parallelize this
from evaluation.overall_eval import run_overall_evaluation, graph_filepath, coordinates, alpha,node_closeness

distances =  [10000, 15000]

run_overall_evaluation(distances, graph_filepath, coordinates, alpha, node_closeness)