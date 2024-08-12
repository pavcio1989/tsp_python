from typing import List
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

from tsp_python import config

import plotly.io as pio
pio.renderers.default = "browser"


def run_algorithm(k, city_list, distance_matrix):
    config.reset_globals()

    if k == "greedy":
        config.best_tour, config.best_distance = nearest_neighbor(city_list, distance_matrix)
    elif k == "k_nearest":
        k_nearest_neighbours(
            3,
            city_list[1:],
            city_list[0],
            [city_list[0]],
            0,
            distance_matrix,
            city_list)
    elif k == "bruteforce":
        bruteforce(
           city_list[1:],
           city_list[0],
           [city_list[0]],
           0,
           distance_matrix,
           city_list)
    else:
        print("No algorithm executed.")

    return config.best_tour, config.best_distance


def nearest_neighbor(cities: List[str], distances: List[List[int]]) -> (List[str],int):
    unvisited = set(cities)
    current = cities[0]
    unvisited.remove(current)
    tour = [current]
    total_distance = 0
    while unvisited:
        next_city = min(unvisited, key=lambda city: distances[cities.index(current)][cities.index(city)])
        tour.append(next_city)
        unvisited.remove(next_city)
        total_distance = total_distance + distances[cities.index(current)][cities.index(next_city)]
        current = next_city
    # returning to first city
    tour.append(cities[0])
    total_distance = total_distance + distances[cities.index(current)][cities.index(cities[0])]

    return tour, total_distance


def bruteforce(remaining, vertex, path, weight, graph, city_list):

    if not remaining:
        # Add distance of returning to initial point
        final_weight = weight + graph[city_list.index(city_list[0])][city_list.index(vertex)]
        if final_weight < config.best_distance:
            config.best_distance = final_weight
            config.best_tour = path
    else:
        for i in remaining:
            new_path = path + [i]
            bruteforce([x for x in remaining if x != i],
                       i,
                       new_path,
                       weight + graph[city_list.index(vertex)][city_list.index(i)],
                       graph,
                       city_list)

    return


def k_nearest_neighbours(k,remaining, vertex, path, weight, graph, city_list):

    if not remaining:
        # Add distance of returning to initial point
        final_weight = weight + graph[city_list.index(city_list[0])][city_list.index(vertex)]
        if final_weight < config.best_distance:
            config.best_distance = final_weight
            config.best_tour = path
    else:

        iter_remaining = remaining

        if len(iter_remaining) > k:
            vertex_distances = graph[city_list.index(vertex)]
            sorted_index_list = sorted(range(len(vertex_distances)), key=lambda m: vertex_distances[m])
            iter_remaining = [city_list[x] for x in sorted_index_list if city_list[x] in iter_remaining][0:k]

        for i in iter_remaining:
            new_path = path + [i]
            k_nearest_neighbours(k,
                                 [x for x in remaining if x != i],
                                 i,
                                 new_path,
                                 weight + graph[city_list.index(vertex)][city_list.index(i)],
                                 graph,
                                 city_list)

    return


def plot_country_tour(country_name, df1, df2):
    fig, ax = plt.subplots(figsize=(8, 6))
    # plot map on axis
    countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    countries[countries["name"] == country_name].plot(color="lightgrey", ax=ax)
    # plot points
    df1.plot(x="longitude", y="latitude", kind="scatter", colormap="YlOrRd",
             title="", ax=ax)
    df2.plot(x="longitude", y="latitude", kind="line", colormap="YlOrRd",
             title="", ax=ax)
    # add grid
    plt.show()


def plot_simple_tour(df):
    fig = px.line(df, x="latitude", y="longitude", text="city")
    fig.show()
