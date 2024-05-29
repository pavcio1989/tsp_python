import pandas as pd


def read_city_names():
    with open("../data/brazil/city_names.txt") as file:
        f = file.readlines()
    city_names = [x[:-1] for x in f]
    return city_names


city_list = read_city_names()


def read_lat_lon():
    df = pd.read_csv("../data/brazil/coord.txt", header=0, sep=" ")
    return list(df.lat), list(df.lon)


city_latitudes, city_longitudes = read_lat_lon()


def read_distance_matrix():
    with open("../data/brazil/distance_matrix.txt") as file3:
        f3 = file3.readlines()
    dist_mat = [x.replace("\n", "").split() for x in f3]
    dist_mat = [[int(y) for y in x] for x in dist_mat]
    return dist_mat


distance_matrix = read_distance_matrix()
