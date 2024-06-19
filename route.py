import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import pandas as pd
import networkx as nx
import logging
from datetime import datetime

from city_graph import CityGraph
from utils import get_edges_from_matrix, get_distance_from_route, timeit

logger = logging.getLogger('tsp')


class Route:
    def __init__(self, city_graph: CityGraph):
        self.city_graph = city_graph
        self.routes = {}

        self._route = []
        self._distance = 1000000000

    @timeit
    def greedy(self):
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

        self._register_route("greedy", tour, total_distance)

        return

    @timeit
    def bruteforce(self):
        self._bruteforce(
            self.city_graph.city_list[1:],
            self.city_graph.city_list[0],
            [self.city_graph.city_list[0]],
            0,
            self.city_graph.distance_matrix,
            self.city_graph.city_list
        )

        self._register_route("bruteforce", self._route, self._distance)

    @timeit
    def k_nearest(self, k=3):
        self._k_nearest_neighbours(
            k,
            self.city_graph.city_list[1:],
            self.city_graph.city_list[0],
            [self.city_graph.city_list[0]],
            0,
            self.city_graph.distance_matrix,
            self.city_graph.city_list
        )

        self._register_route("k_nearest", self._route, self._distance)

    @timeit
    def nx_tsp(self):
        dict_of_edges = get_edges_from_matrix(self.city_graph.distance_matrix)

        G = nx.Graph()
        G.add_weighted_edges_from(dict_of_edges)

        tsp = nx.approximation.traveling_salesman_problem
        route = tsp(G, cycle=True)

        self._route = [self.city_graph.city_list[i] for i in route]
        self._distance = get_distance_from_route(route, self.city_graph.distance_matrix)

        self._register_route("nx_tsp", self._route, self._distance)

        return

    def _bruteforce(self, remaining, vertex, path, weight, graph, city_list):
        if not remaining:
            # Add distance of returning to initial point
            final_weight = weight + graph[city_list.index(city_list[0])][city_list.index(vertex)]
            if final_weight < self._distance:
                self._distance = final_weight
                self._route = path
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
            if final_weight < self._distance:
                self._distance = final_weight
                self._route = path
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
        _, df_for_drawing = self._reshaped_dfs()
        fig = px.line(df_for_drawing, x="latitude", y="longitude", text="city")
        fig.show()

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

        if self._route[0] != self._route[-1]:
            new_index = [self.city_graph.city_list.index(x) for x in self._route + [self.city_graph.city_list[0]]]
        else:
            new_index = [self.city_graph.city_list.index(x) for x in self._route]

        df_reordered = df.copy().reindex(new_index)
        return df, df_reordered

    def _register_route(self, name, route, distance):
        self.routes[name] = {}
        self.routes[name]["route"] = route
        self.routes[name]["distance"] = distance

        return

    def register_execution_time(self, name, exec_time):
        self.routes[name]["exec_time"] = exec_time

        return

    def create_comparison_table(self):
        rows_list = []
        for key in self.routes.keys():
            dict1 = {}
            dict1.update([
                ("algorithm_name", key),
                ("execution_time", self.routes[key]["exec_time"]),
                ("total_distance", self.routes[key]["distance"])
            ])

            rows_list.append(dict1)

        df = pd.DataFrame(rows_list)

        logger.info(f"---- Comparison table:\n {df}")

        return df

    def create_html_report(self, output_folder: str):
        # writing HTML Content
        heading = '<h1> Travelling Salesman Problem - implementations overview </h1>'
        subheading = '<h2> Author: Paweł Pitera </h3>'

        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y %H:%M:%S")
        header = '<div class="top">' + heading + subheading + '</div>'
        footer = '<div class="bottom"> <h3> This Report has been Generated on ' + current_time + ' </h3> </div> '
        content = '<div class="table"> ' + self.create_comparison_table().to_html() + ' </div> '

        # Concatenating everything to a single string
        html = header + content + footer

        # Writing the file
        with open(f"{output_folder}/report.html", "w+") as file:
            file.write(html)

