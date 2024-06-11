from typing import List

from city_graph import CityGraph


class Route:
    def __init__(self, city_graph: CityGraph):
        self.name = "Cities without route"
        self.route = []
        self.distance = 1000000000
        self.city_graph = city_graph

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

        self.name = "Greedy"
        self.route = tour
        self.distance = total_distance

        return

    def bruteforce(self):
        self.name = "bruteforce"
        self._bruteforce(
            self.city_graph.city_list[1:],
            self.city_graph.city_list[0],
            [self.city_graph.city_list[0]],
            0,
            self.city_graph.distance_matrix,
            self.city_graph.city_list
        )

    def k_nearest(self, k=4):
        self.name = "k_nearest_neighbours"
        self._k_nearest_neighbours(
            k,
            self.city_graph.city_list[1:],
            self.city_graph.city_list[0],
            [self.city_graph.city_list[0]],
            0,
            self.city_graph.distance_matrix,
            self.city_graph.city_list
        )

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
