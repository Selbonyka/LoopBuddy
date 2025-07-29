from tqdm import tqdm

# Function below handles stoplights and stairs
def feature_penalizing(feature_handling, feature_status, feature_penalty_strength):
    """
    Helper function to penalize edges in relation to the feature's presence (currently used for stoplights and steps)

    :param feature_handling: user inputted preference (avoid or neutral or prefer)
    :param feature_status: status of the edge
    :param feature_penalty_strength: user inputted strength of penalty
    :return: returns by how much the specific edge was penalized due to presence/absence of a feature
    """
    if feature_handling == 'Neutral':  # no stoplight/stairs penalty
        feature_penalty = 1
    elif feature_handling == 'Avoid':
        # since feature_status is represented by 1 and 0 (True or False) we can use that instead of an if/else block

        feature_penalty = ((feature_status * feature_penalty_strength) + (feature_status * (-1))) + 1
    else:  # case when we prefer the feature
        if feature_status:  # case when the feature is preferred: we penalize when the feature is set to false
            # (logic being that having min weight coefficient of 1 allows for cleaner lower bound calculations)
            feature_penalty = 1
        else:
            feature_penalty = feature_penalty_strength

    return feature_penalty

# Pavement penalizing
def pavement_type_penalizing(pavement_handling, pavement_status, pavement_penalty_strength):
    """
    Helper function to penalize edges in relation to the pavement's state

    :param pavement_handling:  user inputted preference
    :param pavement_status: status of the edge
    :param pavement_penalty_strength:  user input strength of penalty
    :return:  returns by how much the specific edge was penalized due to pavement type
    """

    if pavement_handling == 'Neutral':  # no pavement penalty
        pavement_penalty = 1

    elif pavement_handling == 'Paved':

        if pavement_status == 'paved':
            pavement_penalty = 1
        elif pavement_status == 'unpaved':
            pavement_penalty = pavement_penalty_strength
        else:  # handling unknown/Null
            pavement_penalty = 1 + ( pavement_penalty_strength - 1) * 0.5  # since we don't know what is the state, we apply half the penalty to discourage use of unlabelled roads

    else:  # handling when we prefer unpaved routes
        if pavement_status == 'unpaved':
            pavement_penalty = 1
        elif pavement_status == 'paved':
            pavement_penalty = pavement_penalty_strength
        else:
            pavement_penalty = 1 + (pavement_penalty_strength - 1) * 0.5  # since we don't know what is the state, we apply half the penalty to discourage use of unlabelled roads

    return pavement_penalty

def edge_penalizing(G, stoplights_preference, steps_preference,pavement_preference,stoplight_penalty_strength, steps_penalty_strength, pavement_penalty_strength):
    """
    adds the penalized weight to the graph's edges, based on the outputs by the above functions
    :return: returns graph G
    """
    for _, _, _, data in tqdm(G.edges(keys=True, data=True), desc = "Adding penalized weight to edges", total = len(G.edges())):
        stoplights_penalty = feature_penalizing(stoplights_preference, data["stoplights"], stoplight_penalty_strength)
        steps_penalty = feature_penalizing(steps_preference, data["steps"], steps_penalty_strength)
        pavement_penalty = pavement_type_penalizing(pavement_preference, data["surface"], pavement_penalty_strength)
        length = data['length']

        data["penalized_weight"] = length * stoplights_penalty * steps_penalty * pavement_penalty

    return G