import logging

# Add content root to your path
# import sys
# sys.path.append('C:/Users/pawel/Desktop/Learning/tsp_python/tsp_python')

####################
# Execution
####################

if __name__ == "__main__":
    from tsp_python.config.config import Config
    from tsp_python.entities.city_graph import CityGraph
    from tsp_python.pipelines.pipeline import Pipeline
    from tsp_python.loggers.tsp_logger import TSPLogger

    logger = TSPLogger(__name__, level=logging.INFO)

    config = Config()

    city_graph = CityGraph(config)

    pipeline = Pipeline(config)

    pipeline.run(city_graph)
