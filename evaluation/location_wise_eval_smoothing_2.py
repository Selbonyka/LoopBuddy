from evaluation.location_wise_eval_smoothing import *

distances2 = [5000,10000]
run_smoothing_eval(distances2, graph_filepath, coordinates, alpha, smoothing_param, smoothing_dir)
