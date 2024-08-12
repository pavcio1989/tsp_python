import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import pandas as pd
import networkx as nx
import logging

from tsp_python.entities.city_graph import CityGraph
from tsp_python.utils.utils import get_edges_from_matrix, get_distance_from_route, timeit

logger = logging.getLogger('tsp')


class Route:
    def __init__(self, city_graph: CityGraph):
        self.city_graph = city_graph
        # self.routes = {}

        self.route = []
        self.distance = 1000000000

    @timeit
    def greedy(self):
        """
        Implementation of greedy algorithm of finding best route.

        Greedy algorithm is based on the following logic:
        1. Start from the first city on the list as origin city (and first city on the route)
        2. From the rest of available cities, identify city with smallest distance to origin city
        3. Define it as next city on the route and remove it from list of available cities
        4. Set it as new origin city
        5. Repeat points 2-4 until all cities are added to the route

        :return: None
        """
        cities = self.city_graph.city_list
        distances = self.city_graph.distance_matrix

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

        self.route = tour
        self.distance = total_distance

        return

    @timeit
    def bruteforce(self):
        """
        Implementation of bruteforce algorithm of finding best route.

        Bruteforce algorithm calculates routes of all permutations of available cities and defines best route \
        as the one with the smallest total distance (with the first city on the list as the first city of the route).

        :return: None
        """
        self._bruteforce(
            self.city_graph.city_list[1:],
            self.city_graph.city_list[0],
            [self.city_graph.city_list[0]],
            0,
            self.city_graph.distance_matrix,
            self.city_graph.city_list
        )

    @timeit
    def k_nearest(self, k=3):
        """
        Implementation of K nearest neighbours' algorithm of finding best route.

        K nearest algorithm is a combination of greedy and bruteforce algorithms. It has similar graph-based \
        implementation as bruteforce algorithm where only up to K closest cities to current origin city are considered \
        as candidate for best route at each iteration.

        :param k: Number of neighbour cities to analyze at each iteration
        :return: None
        """
        self._k_nearest_neighbours(
            k,
            self.city_graph.city_list[1:],
            self.city_graph.city_list[0],
            [self.city_graph.city_list[0]],
            0,
            self.city_graph.distance_matrix,
            self.city_graph.city_list
        )

    @timeit
    def nx_tsp(self):
        """
        NetworkX's implementation of algorithm solving TSP problem and finding best route.

        :return: None
        """
        dict_of_edges = get_edges_from_matrix(self.city_graph.distance_matrix)

        G = nx.Graph()
        G.add_weighted_edges_from(dict_of_edges)

        tsp = nx.approximation.traveling_salesman_problem
        route = tsp(G, cycle=True)

        self.route = [self.city_graph.city_list[i] for i in route]
        self.distance = get_distance_from_route(route, self.city_graph.distance_matrix)

        return

    def _bruteforce(self, remaining, vertex, path, weight, graph, city_list):
        if not remaining:
            # Add distance of returning to initial point
            final_weight = weight + graph[city_list.index(city_list[0])][city_list.index(vertex)]
            if final_weight < self.distance:
                self.distance = final_weight
                self.route = path
        else:
            for i in remaining:
                new_path = path + [i]
                self._bruteforce([x for x in remaining if x != i],
                                 i,
                                 new_path,
                                 weight + graph[city_list.index(vertex)][city_list.index(i)],
                                 graph,
                                 city_list)

        return

    def _k_nearest_neighbours(self, k, remaining, vertex, path, weight, graph, city_list):

        if not remaining:
            # Add distance of returning to initial point
            final_weight = weight + graph[city_list.index(city_list[0])][city_list.index(vertex)]
            if final_weight < self.distance:
                self.distance = final_weight
                self.route = path
        else:

            iter_remaining = remaining

            if len(iter_remaining) > k:
                vertex_distances = graph[city_list.index(vertex)]
                sorted_index_list = sorted(range(len(vertex_distances)), key=lambda m: vertex_distances[m])
                iter_remaining = [city_list[x] for x in sorted_index_list if city_list[x] in iter_remaining][0:k]

            for i in iter_remaining:
                new_path = path + [i]
                self._k_nearest_neighbours(k,
                                           [x for x in remaining if x != i],
                                           i,
                                           new_path,
                                           weight + graph[city_list.index(vertex)][city_list.index(i)],
                                           graph,
                                           city_list)

        return

    def draw_route(self):
        """
        Visualize route as line graph on XY axis chart.

        :return: Plotly Express figure object
        """
        _, df_for_drawing = self._reshaped_dfs()
        fig = px.line(df_for_drawing, x="latitude", y="longitude", text="city")
        # fig.show()
        return fig

    # TODO: Geopandas version
    def draw_route_gpd(self, country_name):
        df_original, df_for_drawing = self._reshaped_dfs()
        fig, ax = plt.subplots(figsize=(8, 6))
        # plot map on axis
        countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        countries[countries["name"] == country_name].plot(color="lightgrey", ax=ax)
        # plot points
        df_original.plot(x="longitude", y="latitude", kind="scatter", colormap="YlOrRd",
                 title="", ax=ax)
        df_for_drawing.plot(x="longitude", y="latitude", kind="line", colormap="YlOrRd",
                 title="", ax=ax)
        # add grid
        plt.show()

    def _reshaped_dfs(self):
        df = pd.DataFrame({
            'city': self.city_graph.city_list,
            'latitude': self.city_graph.city_latitudes,
            'longitude': self.city_graph.city_longitudes}
        )

        if self.route[0] != self.route[-1]:
            new_index = [self.city_graph.city_list.index(x) for x in self.route + [self.city_graph.city_list[0]]]
        else:
            new_index = [self.city_graph.city_list.index(x) for x in self.route]

        df_reordered = df.copy().reindex(new_index)
        return df, df_reordered
