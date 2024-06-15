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

# TODO: Consider moving logging activities into separate class


################
# Dataframe prep
################
# TODO: Refactor
# df = pd.DataFrame({'city': city_list, 'latitude': city_latitudes, 'longitude': city_longitudes})
# # print(df)
#
# if config.best_tour[0] != config.best_tour[-1]:
#     new_index = [city_list.index(x) for x in config.best_tour + [city_list[0]]]
# else:
#     new_index = [city_list.index(x) for x in config.best_tour]
# df_reordered = df.copy().reindex(new_index)
# print(df_reordered)


##############
# Plot map
##############
# TODO: Refactor
# plot_country_tour("Germany", df, df_reordered)
# plot_simple_tour(df_reordered)
