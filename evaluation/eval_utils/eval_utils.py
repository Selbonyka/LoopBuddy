import pprint
import random

from evaluation.eval_utils.overall_eval_functions import load_graph


def generate_random_coordinates(number, seed, G):
    """
    Generates a list of random coordinate tuples from the given graph
    :param number: number of tuples to generate
    :param seed: seed
    :param G: graph to be processed
    :return: list of tuples
    """

    random.seed(seed)
    random_nodes = random.sample(list(G.nodes), number)
    G_sample = G.subgraph(random_nodes)
    nodes, data = zip(*G_sample.nodes(data=True))  # getting the data about the nodes

    # Getting the coords that we will test
    coords = [(float(d['x']), float(d['y'])) for d in data]
    # we need the float() here ^ cuz we get np.float as a return, usage ofwhich is discouraged from what i undestand
    return coords


def generate_random_filtered_coordinates(number, seed, G, street_count):
    """
        Generates a list of random coordinate tuples from the given graph, filtered by the required min street_count (inclusive)
        :param number: number of tuples to generate
        :param seed: seed
        :param G: graph to be processed
        :param street_count: min number of streets for the node to be acceptable, as defined by osmnx
        :return: list of tuples
        """

    selected_nodes= []

    counter = 0
    while (counter !=number):
        random_node = random.sample(list(G.nodes), 1)
        # pprint.pprint(G.nodes[random_node[0]])
        street_count = G.nodes[random_node[0]]['street_count']
        if street_count >= street_count:
            selected_nodes.append(random_node[0])
            counter += 1

    # Same as above
    G_sample = G.subgraph(selected_nodes)
    nodes, data = zip(*G_sample.nodes(data=True))  # getting the data about the nodes

    # Getting the coords that we will test
    coords = [(float(d['x']), float(d['y'])) for d in data]
    # we need the float() here ^ cuz we get np.float as a return, usage ofwhich is discouraged from what i undestand
    return coords



