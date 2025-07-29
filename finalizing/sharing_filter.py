from collections import Counter

def sharing_filter(path, sharing_allowance):
    """
    Returns true if a path inputted does not exceed the sharing allowance
    :param path: a list containing the nodes that make up a specific path
    :param sharing_allowance: [0,1] limit on the amount of sharing
    """

    # this checks for sharing:

    sharing_counter = Counter(path)

    total_visits = sum(sharing_counter.values())  # total number of node visits (including repetitions)

    repeated_visits = sum(count for node, count in sharing_counter.items() if count > 1)

    sharing_percentage = repeated_visits / total_visits

    if sharing_percentage < sharing_allowance:
        return True