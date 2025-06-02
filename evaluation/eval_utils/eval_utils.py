
import random
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