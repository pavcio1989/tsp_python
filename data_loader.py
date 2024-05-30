import pandas as pd


class DataLoader:
    def __init__(self, config):
        self.city_list_path = config.file_path['city_list']
        self.coord_path = config.file_path['coord']
        self.distance_matrix_path = config.file_path['distance_matrix']

    def get_city_list(self):
        with open(self.city_list_path) as file:
            f = file.readlines()
        city_names = [x[:-1] for x in f]
        return city_names

    def get_coord(self):
        df = pd.read_csv(self.coord_path, header=0, sep=" ")
        return list(df.lat), list(df.lon)

    def get_distance_matrix(self):
        with open(self.distance_matrix_path) as file3:
            f3 = file3.readlines()
        dist_mat = [x.replace("\n", "").split() for x in f3]
        dist_mat = [[int(y) for y in x] for x in dist_mat]
        return dist_mat
