import logging
from datetime import datetime
import os

from tsp_python.entities.city_graph import CityGraph
from tsp_python.entities.route import Route
from tsp_python.utils.utils import create_comparison_table, create_plots_to_html


logger = logging.getLogger('tsp')


class Pipeline:
    def __init__(self, config):
        self.algorithms = config.algorithms
        self.routes = {}
        self._output_folder = config.output_folder
        self._generate_report = config.generate_report

    def run(self, city_graph: CityGraph):

        for algorithm in self.algorithms:
            if self.algorithms[algorithm]:
                route = Route(city_graph)

                logger.info(f"TSP Algorithm: {algorithm} | In scope: YES")
                logger.info(f"---- Start {algorithm}")

                _, algo_exec_time = getattr(route, algorithm)()

                logger.info(f"---- Best route: {route.route} | \
Best distance: {route.distance}")

                self._register_route(algorithm, route)
                self._register_execution_time(algorithm, algo_exec_time)
            else:
                logger.info(f"TSP Algorithm: {algorithm} | In scope: NO")

        if self._generate_report:
            self._create_html_report()
            logger.info(f"HTML report created in {os.getcwd()}/{self._output_folder} directory")
        else:
            logger.info(f"No HTML report generated.")

    def _register_route(self, name, route: Route):
        self.routes[name] = {}
        self.routes[name]["object"] = route
        self.routes[name]["route"] = route.route
        self.routes[name]["distance"] = route.distance

        return

    def _register_execution_time(self, name, exec_time):
        self.routes[name]["exec_time"] = exec_time

        return

    def _create_html_report(self):
        # writing HTML Content
        heading = '<h1> Travelling Salesman Problem - implementation overview </h1>'
        subheading = '<h2> Author: Paweł Pitera </h3>'

        now = datetime.now()
        print(now)
        current_time_html = now.strftime("%m/%d/%Y %H:%M:%S")
        current_time_filename = now.strftime("%m%d%Y_%H%M%S")

        header = '<div class="top">' + heading + subheading + '</div>'
        footer = '<div class="bottom"> <h3> This Report has been Generated on ' + current_time_html + ' </h3> </div> '
        content_table = '<div class="table"> ' + create_comparison_table(self.routes).to_html() + ' </div> '
        content_plots = create_plots_to_html(self.routes, self._output_folder)

        # Concatenating everything to a single string
        html = header + content_table + content_plots + footer

        # Writing the file
        with open(f"{self._output_folder}/{current_time_filename}_report.html", "w+") as file:
            file.write(html)
