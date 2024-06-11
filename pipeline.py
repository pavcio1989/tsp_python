from city_graph import CityGraph
from route import Route


class Pipeline:
    def __init__(self, config):
        self.algorithms = config.algorithms

    def run(self, city_graph: CityGraph):
        for algorithm in self.algorithms:
            if self.algorithms[algorithm]:
                print(f"TSP Algorithm: {algorithm} | In scope: YES")
                print(f"--- Initialize route:")
                route = Route(city_graph)
                print(f"------ Best route: {route.route} | Best distance: {route.distance}")
                print(f"------ Start {algorithm}")
                getattr(route, algorithm)()
                print(f"------ Best route: {route.route} | Best distance: {route.distance}")
            else:
                print(f"TSP Algorithm: {algorithm} | In scope: NO")
