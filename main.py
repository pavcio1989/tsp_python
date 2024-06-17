import pandas as pd
import logging

# from archive.data_germany import city_list, city_longitudes, city_latitudes,distance_matrix
# from archive.data_48cities import city_list, city_longitudes, city_latitudes,distance_matrix

from config import Config
from city_graph import CityGraph
from pipeline import Pipeline

####################
# Execution
####################

config = Config()

city_graph = CityGraph(config)
pipeline = Pipeline(config)
pipeline.run(city_graph)

##############
# Plot map
##############
# TODO: Refactor
# plot_country_tour("Germany", df, df_reordered)
# plot_simple_tour(df_reordered)
