from evaluation.location_wise_eval_simplification import *
simplification_list = range(20,151,10)
distances2 = [5000, 10000]
run_simplification_eval(distances2, graph_filepath, coordinates, alpha, simplification_list, simplifications_dir)
