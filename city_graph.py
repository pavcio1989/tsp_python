from data_loader import DataLoader
from config import Config


class CityGraph:
    def __init__(self, config: Config):
        data_loader = DataLoader(config)

        self.city_list = data_loader.get_city_list()
        self.city_latitudes, self.city_longitudes = data_loader.get_coord()
        self.distance_matrix = data_loader.get_distance_matrix()
