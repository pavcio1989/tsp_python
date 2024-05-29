import pandas as pd
import yaml
import time

from functions import plot_simple_tour, run_algorithm

# from archive.data_germany import city_list, city_longitudes, city_latitudes,distance_matrix
from archive.data_48cities import city_list, city_longitudes, city_latitudes,distance_matrix

import config

####################
# Setup
####################
# TODO: Refactor designing pipelines
with open('pipeline.yml', 'r') as file:
    pipeline_jobs = yaml.safe_load(file)

print(pipeline_jobs['algorithms'])

####################
#   Calculations   #
####################
# TODO: Refactor
for k, v in pipeline_jobs['algorithms'].items():
    if v:
        start = time.time()
        print(f"Starting {k} algorithm...")
        best_tour, best_distance = run_algorithm(k, city_list, distance_matrix)
        exec_time = time.time() - start
        print(f"Finishing {k} algorithm...")
        print(f"{k} algorithm - execution time: {exec_time}")
        print(f"{k} algorithm - results:")
        print(f"Best tour: {best_tour}")
        print(f"Best distance: {best_distance}")


################
# Dataframe prep
################
# TODO: Refactor
df = pd.DataFrame({'city': city_list, 'latitude': city_latitudes, 'longitude': city_longitudes})
# print(df)

if config.best_tour[0] != config.best_tour[-1]:
    new_index = [city_list.index(x) for x in config.best_tour + [city_list[0]]]
else:
    new_index = [city_list.index(x) for x in config.best_tour]
df_reordered = df.copy().reindex(new_index)
# print(df_reordered)


##############
# Plot map
##############
# TODO: Refactor
# plot_country_tour("Germany", df, df_reordered)
plot_simple_tour(df_reordered)
