from collections import Counter

def sharing_filter(path, sharing_allowance):

    # this checks for sharing:

    sharing_counter = Counter(path)

    total_visits = sum(sharing_counter.values())  # total number of node visits (including repetitions)

    repeated_visits = sum(count for node, count in sharing_counter.items() if count > 1)

    sharing_percentage = repeated_visits / total_visits

    if sharing_percentage < sharing_allowance:
        return True