import logging

from city_graph import CityGraph
from route import Route

logger = logging.getLogger('tsp')


class Pipeline:
    def __init__(self, config):
        self.algorithms = config.algorithms
        self.output_folder = config.output_folder

    def run(self, city_graph: CityGraph):

        route = Route(city_graph)

        for algorithm in self.algorithms:
            if self.algorithms[algorithm]:
                logger.info(f"TSP Algorithm: {algorithm} | In scope: YES")
                logger.info(f"---- Start {algorithm}")
                _, algo_exec_time = getattr(route, algorithm)()
                logger.info(f"---- Best route: {route.routes[algorithm]["route"]} | \
Best distance: {route.routes[algorithm]["distance"]}")
                route.register_execution_time(algorithm, algo_exec_time)
            else:
                logger.info(f"TSP Algorithm: {algorithm} | In scope: NO")

        route.create_html_report(self.output_folder)
