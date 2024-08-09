import logging
from functools import wraps
import time
import pandas as pd
from typing import Dict

logger = logging.getLogger('tsp')


def get_edges_from_matrix(distance_matrix):
    """
    Transforms distance matrix into a list of tuples where each tuple represents a single edge info.

    :param distance_matrix: List of lists containing distances between nodes/cities (symmetrical)
    :return: List of tuples
    """

    return [(i, j, distance_matrix[i][j]) for i in range(len(distance_matrix)) for j in range(len(distance_matrix)) if i < j]


def get_distance_from_route(route, distance_matrix):
    """
    Calculates total distance of input route to cover.

    :param route: List of integers being IDs of each city (starting from 0)
    :param distance_matrix: A list of lists containing distances between nodes/cities (symmetrical)
    :return: Integer representing total distance of input route
    """

    dist = 0
    for x in range((len(route) - 1)):
        dist += distance_matrix[route[x]][route[x + 1]]
    return dist


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(f'---- Function {func.__name__} Took {total_time:.4f} seconds')

        return result, total_time
    return timeit_wrapper


def create_comparison_table(routes: Dict):
    """
    Render routes information into Pandas dataframe format to be added into HTML report

    :param routes: Dictionary containing routes parameter content from Pipeline class
    :return: Pandas dataframe
    """
    rows_list = []
    for key in routes.keys():
        dict1 = {}
        dict1.update([
            ("algorithm_name", key),
            ("execution_time", routes[key]["exec_time"]),
            ("total_distance", routes[key]["distance"])
        ])
        rows_list.append(dict1)
    df = pd.DataFrame(rows_list)
    logger.info(f"---- Comparison table:\n {df}")

    return df


def create_plots_to_html(routes: Dict, output_folder: str):
    """
    Visualize routes on chart and render them into HTML format to be added to the report.

    :param routes: Dictionary containing routes parameter content from Pipeline class
    :param output_folder: path to store outputs
    :return: HTML-formatted references to routes maps
    """
    image_html = ''

    for route_name, route_dict in routes.items():
        fig = route_dict["object"].draw_route()
        fig.write_image(f"{output_folder}/images/fig_{route_name}.png")

        image_tag = '<img src="images/fig_' + route_name + '.png"> '
        image_title = '<h4> Route algorithm: ' + route_name + ' </h4> '
        image_content = '<div class="map">' + image_tag + '</div> '

        image_html = image_html + image_title + image_content

    return image_html
