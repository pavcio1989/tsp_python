from city_graph import CityGraph
from route import Route


class Pipeline:
    def __init__(self, config):
        self.algorithms = config.algorithms

    def run(self, city_graph: CityGraph):

        route = Route(city_graph)

        for algorithm in self.algorithms:
            if self.algorithms[algorithm]:
                print(f"TSP Algorithm: {algorithm} | In scope: YES")
                print(f"-- Initialize route:")
                print(f"---- Start {algorithm}")
                getattr(route, algorithm)()
                print(f"---- Best route: {route.routes[algorithm]["route"]} | \
Best distance: {route.routes[algorithm]["distance"]}")
            else:
                print(f"TSP Algorithm: {algorithm} | In scope: NO")
