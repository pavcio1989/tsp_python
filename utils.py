def get_edges_from_matrix(distance_matrix):
    """Transforms distance matrix into a list of tuples where each tuple represents a single edge info.

    Args:
        distance_matrix: A list of lists containing distances between nodes/cities (symmetrical).

    Returns:
        A list of tuples.

    """
    return [(i, j, distance_matrix[i][j]) for i in range(len(distance_matrix)) for j in range(len(distance_matrix)) if i < j]


def get_distance_from_route(route, distance_matrix):
    """Calculates total distance of input route to cover.

    Args:
        route: A list of integers being IDs of each city (starting from 0)
        distance_matrix: A list of lists containing distances between nodes/cities (symmetrical).

    Returns:
        Integer representing total distance of input route

    """
    dist = 0
    for x in range((len(route) - 1)):
        dist += distance_matrix[route[x]][route[x + 1]]
    return dist
