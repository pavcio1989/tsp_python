import numpy as np
import pandas as pd

import time

from functions import nearest_neighbor, bruteforce, k_nearest_neighbours, plot_country_tour, plot_simple_tour

from data_germany import city_list, city_longitudes, city_latitudes,distance_matrix
# from data_48cities import city_list, city_longitudes, city_latitudes,distance_matrix

import config

####################
#   Calculations   #
####################

start = time.time()
config.best_tour, config.best_distance = nearest_neighbor(city_list, distance_matrix)
print(f"Greedy algorithm - execution time: {time.time() - start}")

print("Greedy algorithm - results:")
print(config.best_tour)
print(config.best_distance)

################

# config.reset_globals()
# print(f"After reset: best tour: {config.best_tour}, best distance: {config.best_distance}")
#
# start = time.time()
# bruteforce(
#    city_list[1:],
#    city_list[0],
#    [city_list[0]],
#    0,
#    distance_matrix,
#    city_list)
# print(f"Bruteforce algorithm - execution time: {time.time() - start}")
#
# print("Bruteforce algorithm - results:")
# print(config.best_distance)
# print(config.best_tour)
# ################
#
# ################
# config.reset_globals()
# print(f"After reset: best tour: {config.best_tour}, best distance: {config.best_distance}")
#
# start = time.time()
# k_nearest_neighbours(
#     4,
#     city_list[1:],
#     city_list[0],
#     [city_list[0]],
#     0,
#     distance_matrix,
#     city_list)
# print(f"K nearest neighbours algorithm - execution time: {time.time() - start}")
#
# print("K nearest neighbours algorithm - results:")
# print(config.best_distance)
# print(config.best_tour)

################
# Dataframe prep
################

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

plot_country_tour("Germany", df, df_reordered)
# plot_simple_tour(df_reordered)
